#!/usr/bin/env python3
# /// script
# /// requires-python = ">=3.10"
# /// dependencies = ["graphqlite"]
# ///
"""ssd-project-setup read-only memory adapter backed by GraphQLite."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ssd_memory.kernel import fail, open_graph, output  # noqa: E402


SETUP_ARTIFACTS = [
    {
        "kind": "product-brief",
        "title": "Product Brief",
        "required": True,
        "implemented": True,
        "skill": "ssd-product-brief-create",
        "depends_on": [],
    },
    {
        "kind": "product-blueprint",
        "title": "Product Blueprint",
        "required": True,
        "implemented": True,
        "skill": "ssd-product-blueprint-create",
        "depends_on": ["product-brief"],
    },
    {
        "kind": "architecture-blueprint",
        "title": "Architecture Blueprint",
        "required": True,
        "implemented": True,
        "skill": "ssd-architecture-blueprint-create",
        "depends_on": ["product-blueprint"],
    },
]

ROOT_SCOPE = {
    "scope_id": "root",
    "scope_type": "project",
    "name": "root",
}


def resolve_scope(scope: str) -> dict[str, str]:
    if scope not in {"auto", "root"}:
        raise ValueError("Only root setup scope is supported right now")
    return dict(ROOT_SCOPE)


def artifact_scope_id(_: dict[str, Any]) -> str:
    # Existing Artifact memory is project-scoped. Future scoped artifacts can store scope_id.
    return "root"


def current_artifacts(graph: Any) -> list[dict[str, Any]]:
    rows = graph.query("MATCH (a:Artifact) RETURN a ORDER BY a.kind")
    artifacts: list[dict[str, Any]] = []
    for row in rows:
        props = row["a"].get("properties", {})
        artifacts.append(props)
    return artifacts


def index_artifacts(artifacts: list[dict[str, Any]], scope_id: str) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    duplicates: set[str] = set()
    setup_kinds = {definition["kind"] for definition in SETUP_ARTIFACTS}

    for artifact in artifacts:
        kind = artifact.get("kind")
        if kind not in setup_kinds or artifact_scope_id(artifact) != scope_id:
            continue
        if kind in indexed:
            duplicates.add(kind)
        indexed[kind] = artifact

    if duplicates:
        duplicate = sorted(duplicates)[0]
        raise ValueError(f"Multiple Artifacts exist for kind: {duplicate}")
    return indexed


def display_artifact(artifact: dict[str, Any]) -> dict[str, Any]:
    return {
        "artifact_id": artifact.get("id"),
        "kind": artifact.get("kind"),
        "title": artifact.get("title"),
        "scope_id": artifact_scope_id(artifact),
    }


def build_status(*, scope: dict[str, str], artifacts: list[dict[str, Any]]) -> dict[str, Any]:
    try:
        indexed = index_artifacts(artifacts, scope["scope_id"])
    except ValueError as exc:
        return {
            "status": "blocked",
            "scope": scope,
            "artifacts": [],
            "all_artifacts": [display_artifact(artifact) for artifact in artifacts],
            "available_next_steps": [],
            "blocked_steps": [],
            "must_do": [],
            "blocked_reason": str(exc),
        }

    artifact_states: list[dict[str, Any]] = []
    available_next_steps: list[dict[str, Any]] = []
    blocked_steps: list[dict[str, Any]] = []

    for definition in SETUP_ARTIFACTS:
        kind = definition["kind"]
        artifact = indexed.get(kind)
        dependency_kinds = definition["depends_on"]
        missing_dependencies = [dependency for dependency in dependency_kinds if dependency not in indexed]

        state = {
            "kind": kind,
            "title": definition["title"],
            "scope_id": scope["scope_id"],
            "required": definition["required"],
            "implemented": definition["implemented"],
            "skill": definition["skill"],
            "depends_on": dependency_kinds,
            "complete": artifact is not None,
            "state": "complete",
            "blocked_by": [],
        }

        if artifact is not None:
            state["artifact_id"] = artifact.get("id")
        elif missing_dependencies:
            state["state"] = "blocked"
            state["blocked_by"] = missing_dependencies
            blocked_steps.append(
                {
                    "artifact_kind": kind,
                    "skill": definition["skill"],
                    "blocked_by": missing_dependencies,
                    "reason": f"{definition['title']} is missing but prerequisites are incomplete.",
                }
            )
        elif not definition["implemented"]:
            state["state"] = "not_implemented"
            blocked_steps.append(
                {
                    "artifact_kind": kind,
                    "skill": definition["skill"],
                    "blocked_by": [],
                    "reason": f"{definition['title']} setup is not implemented yet.",
                }
            )
        else:
            state["state"] = "available"
            available_next_steps.append(
                {
                    "artifact_kind": kind,
                    "skill": definition["skill"],
                    "reason": f"{definition['title']} is missing and all prerequisites are complete.",
                }
            )

        artifact_states.append(state)

    status = "complete"
    if available_next_steps or blocked_steps:
        status = "incomplete"

    return {
        "status": status,
        "scope": scope,
        "artifacts": artifact_states,
        "all_artifacts": [display_artifact(artifact) for artifact in artifacts],
        "available_next_steps": available_next_steps,
        "blocked_steps": blocked_steps,
        "must_do": available_next_steps,
    }


def cmd_status(args: argparse.Namespace) -> int:
    scope = resolve_scope(args.scope)
    graph = open_graph()
    try:
        artifacts = current_artifacts(graph)
    finally:
        graph.close()
    output(build_status(scope=scope, artifacts=artifacts))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    status = subparsers.add_parser("status")
    status.add_argument("--scope", default="auto", choices=["auto", "root"])
    status.set_defaults(func=cmd_status)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.func(args)
    except (ValueError, json.JSONDecodeError) as exc:
        return fail(str(exc))


if __name__ == "__main__":
    raise SystemExit(main())
