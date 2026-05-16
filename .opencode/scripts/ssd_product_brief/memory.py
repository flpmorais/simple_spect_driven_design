#!/usr/bin/env python3
# /// script
# /// requires-python = ">=3.10"
# /// dependencies = ["graphqlite"]
# ///
"""ssd-product-brief memory adapter backed by GraphQLite."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ssd_memory.kernel import fail, open_graph, output, read_json_file  # noqa: E402
from ssd_memory.memory import (  # noqa: E402
    current_sections,
    get_artifact_by_kind,
    upsert_artifact,
    validate_sections,
)


KIND = "product-brief"
TITLE = "Product Brief"
REQUIRED_SECTIONS = [
    ("why-this-exists", "Why This Exists"),
    ("product-definition", "Product Definition"),
    ("problem", "Problem"),
    ("high-level-solution", "High-Level Solution"),
    ("audience", "Audience"),
    ("necessity-and-differentiation", "Necessity And Differentiation"),
    ("positioning", "Positioning"),
    ("practical-constraints", "Practical Constraints"),
    ("assumptions", "Assumptions"),
    ("open-questions", "Open Questions"),
]
REQUIRED_KEYS = [key for key, _ in REQUIRED_SECTIONS]
HEADING_BY_KEY = dict(REQUIRED_SECTIONS)


def read_payload(path_text: str | None) -> dict[str, Any]:
    if path_text:
        raw = read_json_file(path_text)
    else:
        raw = json.loads(sys.stdin.read())
    if not isinstance(raw, dict):
        raise ValueError("payload must be a JSON object")
    return raw


def normalize_refs(raw: Any, field_name: str) -> list[str]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise ValueError(f"{field_name} must be an array")
    refs: list[str] = []
    for index, item in enumerate(raw, start=1):
        if not isinstance(item, str) or not item.strip():
            raise ValueError(f"{field_name}[{index}] must be a non-empty string")
        refs.append(item.strip())
    return refs


def normalize_sections(raw: Any) -> list[dict[str, Any]]:
    if isinstance(raw, dict):
        missing = [key for key in REQUIRED_KEYS if key not in raw]
        if missing:
            raise ValueError(f"Product Brief missing required sections: {', '.join(missing)}")
        sections = [
            {
                "section_key": key,
                "heading": HEADING_BY_KEY[key],
                "canonical_text": raw.get(key, ""),
                "position": index,
            }
            for index, key in enumerate(REQUIRED_KEYS, start=1)
        ]
    else:
        sections = raw

    normalized = validate_sections(sections)
    by_key = {section["section_key"]: section for section in normalized}
    missing = [key for key in REQUIRED_KEYS if key not in by_key]
    if missing:
        raise ValueError(f"Product Brief missing required sections: {', '.join(missing)}")

    ordered: list[dict[str, Any]] = []
    for index, key in enumerate(REQUIRED_KEYS, start=1):
        section = dict(by_key[key])
        if not isinstance(section["canonical_text"], str):
            raise ValueError(f"Section {key} requires canonical_text")
        section["heading"] = HEADING_BY_KEY[key]
        section["position"] = index
        ordered.append(section)
    return ordered


def cypher_string(value: str) -> str:
    return json.dumps(value)


def payload_to_memory_inputs(
    payload: dict[str, Any],
    *,
    default_cited_brainstorm_ids: list[str] | None = None,
    default_cited_idea_ids: list[str] | None = None,
) -> dict[str, Any]:
    sections = normalize_sections(payload.get("sections"))
    cited_brainstorm_ids = normalize_refs(
        payload.get("cited_brainstorm_ids", default_cited_brainstorm_ids),
        "cited_brainstorm_ids",
    )
    cited_idea_ids = normalize_refs(
        payload.get("cited_idea_ids", default_cited_idea_ids),
        "cited_idea_ids",
    )

    return {
        "sections": sections,
        "change_summary": payload.get("change_summary") or "Update Product Brief",
        "cited_brainstorm_ids": cited_brainstorm_ids,
        "cited_idea_ids": cited_idea_ids,
    }


def add_provenance_edges(
    graph: Any,
    *,
    artifact_id: str,
    cited_brainstorm_ids: list[str],
    cited_idea_ids: list[str],
) -> None:
    for edge in list(graph.get_edges_from(artifact_id)):
        rel_type = edge.get("r", {}).get("type")
        if rel_type in {"DERIVED_FROM", "CITES"}:
            graph.delete_edge(artifact_id, edge["target"], rel_type=rel_type)
    for brainstorm_id in cited_brainstorm_ids:
        graph.upsert_edge(artifact_id, brainstorm_id, {"type": "DERIVED_FROM"}, rel_type="DERIVED_FROM")
    for idea_id in cited_idea_ids:
        graph.upsert_edge(artifact_id, idea_id, {"type": "CITES"}, rel_type="CITES")


def current_provenance_refs(graph: Any, artifact_id: str) -> tuple[list[str], list[str]]:
    cited_brainstorm_ids: list[str] = []
    cited_idea_ids: list[str] = []
    for edge in graph.get_edges_from(artifact_id):
        rel_type = edge.get("r", {}).get("type")
        if rel_type == "DERIVED_FROM":
            cited_brainstorm_ids.append(edge["target"])
        elif rel_type == "CITES":
            cited_idea_ids.append(edge["target"])
    return cited_brainstorm_ids, cited_idea_ids


def current_product_brief(graph: Any) -> dict[str, Any]:
    artifact = get_artifact_by_kind(graph, KIND)
    if artifact is None:
        raise ValueError("Product Brief does not exist")
    cited_brainstorm_ids, cited_idea_ids = current_provenance_refs(graph, artifact["id"])
    return {
        "status": "ok",
        "artifact": artifact,
        "sections": current_sections(graph, KIND),
        "cited_brainstorm_ids": cited_brainstorm_ids,
        "cited_idea_ids": cited_idea_ids,
    }


def cmd_create(args: argparse.Namespace) -> int:
    graph = open_graph()
    try:
        payload = read_payload(args.payload_json)
        memory_inputs = payload_to_memory_inputs(payload)
        result = upsert_artifact(
            graph,
            kind=KIND,
            title=TITLE,
            sections=memory_inputs["sections"],
            change_summary=memory_inputs["change_summary"],
            is_create=True,
        )
        add_provenance_edges(
            graph,
            artifact_id=result["artifact_id"],
            cited_brainstorm_ids=memory_inputs["cited_brainstorm_ids"],
            cited_idea_ids=memory_inputs["cited_idea_ids"],
        )
        graph.reload_graph()
    finally:
        graph.close()
    output({"status": "ok", "artifact_kind": KIND, **result})
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    graph = open_graph()
    try:
        artifact = get_artifact_by_kind(graph, KIND)
        if artifact is None:
            raise ValueError("Product Brief does not exist")
        payload = read_payload(args.payload_json)
        cited_brainstorm_ids, cited_idea_ids = current_provenance_refs(graph, artifact["id"])
        memory_inputs = payload_to_memory_inputs(
            payload,
            default_cited_brainstorm_ids=cited_brainstorm_ids,
            default_cited_idea_ids=cited_idea_ids,
        )
        result = upsert_artifact(
            graph,
            kind=KIND,
            title=None,
            sections=memory_inputs["sections"],
            change_summary=memory_inputs["change_summary"],
            is_create=False,
        )
        add_provenance_edges(
            graph,
            artifact_id=result["artifact_id"],
            cited_brainstorm_ids=memory_inputs["cited_brainstorm_ids"],
            cited_idea_ids=memory_inputs["cited_idea_ids"],
        )
        graph.reload_graph()
    finally:
        graph.close()
    output({"status": "ok", "artifact_kind": KIND, **result})
    return 0


def cmd_get(_: argparse.Namespace) -> int:
    graph = open_graph()
    try:
        result = current_product_brief(graph)
    finally:
        graph.close()
    output(result)
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    if args.confirm != args.artifact_id:
        raise ValueError("Confirmation does not match artifact_id")

    graph = open_graph()
    try:
        artifact = get_artifact_by_kind(graph, KIND)
        if artifact is None or artifact.get("id") != args.artifact_id:
            raise ValueError(f"Product Brief does not exist: {args.artifact_id}")
        artifact_id = cypher_string(args.artifact_id)
        rows = graph.query(
            f"MATCH (n) WHERE n.id = {artifact_id} OR n.artifact_id = {artifact_id} RETURN n"
        )
        graph.query(
            f"MATCH (n) WHERE n.id = {artifact_id} OR n.artifact_id = {artifact_id} DETACH DELETE n"
        )
        graph.reload_graph()
    finally:
        graph.close()
    output(
        {
            "status": "ok",
            "deleted": {
                "artifact_id": args.artifact_id,
                "artifact_kind": KIND,
                "nodes": len(rows),
            },
        }
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create")
    create.add_argument("--payload-json", help="JSON payload file. Reads stdin when omitted.")
    create.set_defaults(func=cmd_create)

    update = subparsers.add_parser("update")
    update.add_argument("--payload-json", help="JSON payload file. Reads stdin when omitted.")
    update.set_defaults(func=cmd_update)

    get = subparsers.add_parser("get")
    get.set_defaults(func=cmd_get)

    delete = subparsers.add_parser("delete")
    delete.add_argument("--artifact-id", required=True)
    delete.add_argument("--confirm", required=True)
    delete.set_defaults(func=cmd_delete)

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
