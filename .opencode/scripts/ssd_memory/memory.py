#!/usr/bin/env python3
# /// script
# /// requires-python = ">=3.10"
# /// dependencies = ["graphqlite"]
# ///
"""Generic SSD memory semantic command interface backed by GraphQLite."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ssd_memory.kernel import (  # noqa: E402
    DB_PATH,
    GRAPH_NAMESPACE,
    fail,
    new_id,
    node_props,
    now_iso,
    open_graph,
    output,
    read_json_file,
    slug,
)


def get_artifact_by_kind(graph: Any, kind: str) -> dict[str, Any] | None:
    normalized_kind = slug(kind)
    rows = graph.query("MATCH (a:Artifact) RETURN a")
    matches: list[dict[str, Any]] = []
    for row in rows:
        props = row["a"].get("properties", {})
        if props.get("kind") == normalized_kind:
            matches.append(props)
    if len(matches) > 1:
        raise ValueError(f"Multiple Artifacts exist for kind: {normalized_kind}")
    return matches[0] if matches else None


def validate_sections(raw: Any) -> list[dict[str, Any]]:
    if not isinstance(raw, list) or not raw:
        raise ValueError("sections-json must contain a non-empty array")

    sections: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Section #{index} must be an object")

        section_key = item.get("section_key")
        heading = item.get("heading")
        canonical_text = item.get("canonical_text")
        if not isinstance(section_key, str) or not section_key.strip():
            raise ValueError(f"Section #{index} requires section_key")
        if not isinstance(heading, str) or not heading.strip():
            raise ValueError(f"Section #{index} requires heading")
        if not isinstance(canonical_text, str):
            raise ValueError(f"Section #{index} requires canonical_text")

        key = slug(section_key)
        if key in seen:
            raise ValueError(f"Duplicate section_key: {section_key}")
        seen.add(key)

        sections.append(
            {
                "section_key": key,
                "heading": heading.strip(),
                "canonical_text": canonical_text,
                "position": item.get("position", index),
            }
        )
    return sections


def current_sections(graph: Any, kind: str) -> list[dict[str, Any]]:
    artifact = get_artifact_by_kind(graph, kind)
    if artifact is None:
        return []
    sections: list[dict[str, Any]] = []
    for edge in graph.get_edges_from(artifact["id"]):
        if edge.get("r", {}).get("type") != "HAS_CURRENT_SECTION":
            continue
        props = node_props(graph.get_node(edge["target"]))
        if props:
            sections.append(props)
    return sorted(sections, key=lambda item: item.get("position", 0))


def upsert_artifact(
    graph: Any,
    *,
    kind: str,
    title: str | None,
    sections: list[dict[str, Any]],
    change_summary: str,
    is_create: bool,
) -> dict[str, Any]:
    timestamp = now_iso()
    existing = get_artifact_by_kind(graph, kind)

    if is_create and existing is not None:
        raise ValueError(f"Artifact already exists: {kind}")
    if not is_create and existing is None:
        raise ValueError(f"Artifact does not exist: {kind}")

    aid = (existing or {}).get("id") or new_id()
    artifact_title = title or (existing or {}).get("title") or slug(kind)

    artifact_props = {
        "id": aid,
        "kind": slug(kind),
        "title": artifact_title,
        "status": (existing or {}).get("status", "accepted"),
        "change_summary": change_summary,
        "created_at": (existing or {}).get("created_at", timestamp),
        "updated_at": timestamp,
    }
    graph.upsert_node(aid, artifact_props, label="Artifact")

    for edge in graph.get_edges_from(aid):
        if edge.get("r", {}).get("type") == "HAS_CURRENT_SECTION":
            graph.delete_edge(aid, edge["target"], rel_type="HAS_CURRENT_SECTION")
            graph.delete_node(edge["target"])

    section_ids: list[str] = []
    for section in sections:
        sid = new_id()
        section_props = {
            "id": sid,
            "artifact_id": aid,
            "kind": slug(kind),
            "title": f"{artifact_title}: {section['heading']}",
            "section_key": section["section_key"],
            "heading": section["heading"],
            "canonical_text": section["canonical_text"],
            "position": section["position"],
            "updated_at": timestamp,
        }
        graph.upsert_node(sid, section_props, label="ArtifactSection")
        graph.upsert_edge(aid, sid, {"type": "HAS_CURRENT_SECTION"}, rel_type="HAS_CURRENT_SECTION")
        section_ids.append(sid)

    graph.reload_graph()
    return {
        "artifact_id": aid,
        "section_ids": section_ids,
    }


def cmd_init(_: argparse.Namespace) -> int:
    graph = open_graph()
    try:
        stats = graph.stats()
    finally:
        graph.close()
    output({"status": "ok", "database": str(DB_PATH), "namespace": GRAPH_NAMESPACE, "stats": stats})
    return 0


def cmd_artifact_create(args: argparse.Namespace) -> int:
    graph = open_graph()
    try:
        sections = validate_sections(read_json_file(args.sections_json))
        result = upsert_artifact(
            graph,
            kind=args.kind,
            title=args.title,
            sections=sections,
            change_summary=args.change_summary,
            is_create=True,
        )
    finally:
        graph.close()
    output({"status": "ok", **result})
    return 0


def cmd_artifact_update(args: argparse.Namespace) -> int:
    graph = open_graph()
    try:
        artifact = get_artifact_by_kind(graph, args.kind)
        if artifact is None:
            raise ValueError(f"Artifact does not exist: {args.kind}")
        sections = validate_sections(read_json_file(args.sections_json))
        result = upsert_artifact(
            graph,
            kind=args.kind,
            title=None,
            sections=sections,
            change_summary=args.change_summary,
            is_create=False,
        )
    finally:
        graph.close()
    output({"status": "ok", **result})
    return 0


def cmd_artifact_get(args: argparse.Namespace) -> int:
    graph = open_graph()
    try:
        artifact = get_artifact_by_kind(graph, args.kind)
        if artifact is None:
            raise ValueError(f"Artifact does not exist: {args.kind}")
        output(
            {
                "status": "ok",
                "artifact": artifact,
                "sections": current_sections(graph, args.kind),
            }
        )
    finally:
        graph.close()
    return 0


def cmd_artifact_list(_: argparse.Namespace) -> int:
    graph = open_graph()
    try:
        rows = graph.query("MATCH (a:Artifact) RETURN a ORDER BY a.kind")
        artifacts = [row["a"]["properties"] for row in rows]
    finally:
        graph.close()
    output({"status": "ok", "artifacts": artifacts})
    return 0


def cmd_graph_query(args: argparse.Namespace) -> int:
    lowered = args.cypher.strip().lower()
    write_words = ("create", "merge", "set", "delete", "remove", "drop")
    if not args.unsafe_write and any(word in lowered for word in write_words):
        raise ValueError("graph query is read-only unless --unsafe-write is supplied")
    graph = open_graph()
    try:
        rows = graph.query(args.cypher)
    finally:
        graph.close()
    output({"status": "ok", "rows": rows})
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init")
    init_parser.set_defaults(func=cmd_init)

    artifact = subparsers.add_parser("artifact")
    artifact_sub = artifact.add_subparsers(dest="artifact_command", required=True)

    create = artifact_sub.add_parser("create")
    create.add_argument("--kind", required=True)
    create.add_argument("--title", required=True)
    create.add_argument("--sections-json", required=True)
    create.add_argument("--change-summary", required=True)
    create.set_defaults(func=cmd_artifact_create)

    update = artifact_sub.add_parser("update")
    update.add_argument("--kind", required=True)
    update.add_argument("--sections-json", required=True)
    update.add_argument("--change-summary", required=True)
    update.set_defaults(func=cmd_artifact_update)

    get = artifact_sub.add_parser("get")
    get.add_argument("--kind", required=True)
    get.set_defaults(func=cmd_artifact_get)

    artifact_list = artifact_sub.add_parser("list")
    artifact_list.set_defaults(func=cmd_artifact_list)

    graph_query = subparsers.add_parser("graph")
    graph_sub = graph_query.add_subparsers(dest="graph_command", required=True)
    query = graph_sub.add_parser("query")
    query.add_argument("--cypher", required=True)
    query.add_argument("--unsafe-write", action="store_true")
    query.set_defaults(func=cmd_graph_query)

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
