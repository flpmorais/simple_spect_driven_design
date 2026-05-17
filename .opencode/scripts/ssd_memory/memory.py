#!/usr/bin/env python3
# /// script
# /// requires-python = ">=3.10"
# /// dependencies = ["graphqlite", "pyyaml"]
# ///
"""Generic SSD memory semantic command interface backed by GraphQLite."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

import yaml

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


REFERENCE_DATA_DIR = Path(".opencode/shared/reference-data")


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


def read_yaml_file(path_text: str) -> dict[str, Any]:
    path = Path(path_text)
    if not path.is_file():
        raise ValueError(f"Expected YAML file: {path_text}")
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("reference seed must be a YAML object")
    return data


def default_reference_seed_path(list_key: str) -> Path:
    return REFERENCE_DATA_DIR / f"{slug(list_key)}.yaml"


def get_reference_list(graph: Any, list_key: str) -> dict[str, Any] | None:
    normalized_key = slug(list_key)
    rows = graph.query("MATCH (l:ReferenceList) RETURN l")
    matches: list[dict[str, Any]] = []
    for row in rows:
        props = row["l"].get("properties", {})
        if props.get("list_key") == normalized_key:
            matches.append(props)
    if len(matches) > 1:
        raise ValueError(f"Multiple ReferenceLists exist for list_key: {normalized_key}")
    return matches[0] if matches else None


def reference_items(graph: Any, list_id: str) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for edge in graph.get_edges_from(list_id):
        if edge.get("r", {}).get("type") != "HAS_ITEM":
            continue
        props = node_props(graph.get_node(edge["target"]))
        if props:
            items.append(props)
    return sorted(items, key=lambda item: item.get("position", 0))


def validate_reference_seed(raw: dict[str, Any]) -> dict[str, Any]:
    list_key = raw.get("list_key")
    title = raw.get("title")
    items = raw.get("items")
    if not isinstance(list_key, str) or not list_key.strip():
        raise ValueError("reference seed requires list_key")
    if not isinstance(title, str) or not title.strip():
        raise ValueError("reference seed requires title")
    if not isinstance(items, list) or not items:
        raise ValueError("reference seed requires non-empty items")

    normalized_items: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Reference item #{index} must be an object")
        item_key = item.get("item_key")
        name = item.get("name")
        if not isinstance(item_key, str) or not item_key.strip():
            raise ValueError(f"Reference item #{index} requires item_key")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"Reference item #{index} requires name")
        normalized_key = slug(item_key)
        if normalized_key in seen:
            raise ValueError(f"Duplicate reference item_key: {item_key}")
        seen.add(normalized_key)
        normalized = dict(item)
        normalized["item_key"] = normalized_key
        normalized["name"] = name.strip()
        normalized["title"] = item.get("title") or name.strip()
        normalized["status"] = item.get("status") or "active"
        normalized["position"] = item.get("position", index)
        normalized_items.append(normalized)

    return {
        "list_key": slug(list_key),
        "title": title.strip(),
        "description": raw.get("description") or "",
        "seed_version": raw.get("seed_version", 1),
        "items": normalized_items,
    }


def upsert_reference_list(graph: Any, seed: dict[str, Any]) -> dict[str, Any]:
    timestamp = now_iso()
    existing = get_reference_list(graph, seed["list_key"])
    list_id = (existing or {}).get("id") or new_id()
    list_props = {
        "id": list_id,
        "list_key": seed["list_key"],
        "title": seed["title"],
        "description": seed["description"],
        "seed_version": seed["seed_version"],
        "status": "active",
        "created_at": (existing or {}).get("created_at", timestamp),
        "updated_at": timestamp,
    }
    graph.upsert_node(list_id, list_props, label="ReferenceList")

    existing_items = {item["item_key"]: item for item in reference_items(graph, list_id)}
    seed_keys = {item["item_key"] for item in seed["items"]}
    item_ids: list[str] = []
    created = 0
    updated = 0
    deprecated = 0

    for item in seed["items"]:
        current = existing_items.get(item["item_key"])
        item_id = (current or {}).get("id") or new_id()
        props = dict(item)
        props.update(
            {
                "id": item_id,
                "list_key": seed["list_key"],
                "category": item.get("category") or "",
                "seed_version": seed["seed_version"],
                "created_at": (current or {}).get("created_at", timestamp),
                "updated_at": timestamp,
            }
        )
        graph.upsert_node(item_id, props, label="ReferenceItem")
        graph.upsert_edge(list_id, item_id, {"type": "HAS_ITEM"}, rel_type="HAS_ITEM")
        item_ids.append(item_id)
        if current is None:
            created += 1
        else:
            updated += 1

    for item_key, item in existing_items.items():
        if item_key in seed_keys or item.get("status") == "deprecated":
            continue
        props = dict(item)
        props["status"] = "deprecated"
        props["updated_at"] = timestamp
        graph.upsert_node(props["id"], props, label="ReferenceItem")
        deprecated += 1

    graph.reload_graph()
    return {
        "list_id": list_id,
        "item_ids": item_ids,
        "created": created,
        "updated": updated,
        "deprecated": deprecated,
    }


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


def cmd_reference_bootstrap(args: argparse.Namespace) -> int:
    seed_path = Path(args.seed_yaml) if args.seed_yaml else default_reference_seed_path(args.list_key)
    seed = validate_reference_seed(read_yaml_file(str(seed_path)))
    if seed["list_key"] != slug(args.list_key):
        raise ValueError(f"Seed list_key does not match requested list_key: {args.list_key}")
    graph = open_graph()
    try:
        result = upsert_reference_list(graph, seed)
    finally:
        graph.close()
    output({"status": "ok", "list_key": seed["list_key"], **result})
    return 0


def cmd_reference_get(args: argparse.Namespace) -> int:
    graph = open_graph()
    try:
        reference_list = get_reference_list(graph, args.list_key)
        if reference_list is None:
            raise ValueError(f"ReferenceList does not exist: {slug(args.list_key)}")
        items = reference_items(graph, reference_list["id"])
        if not args.include_deprecated:
            items = [item for item in items if item.get("status") != "deprecated"]
    finally:
        graph.close()
    output({"status": "ok", "reference_list": reference_list, "items": items})
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

    reference = subparsers.add_parser("reference")
    reference_sub = reference.add_subparsers(dest="reference_command", required=True)

    reference_bootstrap = reference_sub.add_parser("bootstrap")
    reference_bootstrap.add_argument("--list-key", required=True)
    reference_bootstrap.add_argument("--seed-yaml")
    reference_bootstrap.set_defaults(func=cmd_reference_bootstrap)

    reference_get = reference_sub.add_parser("get")
    reference_get.add_argument("--list-key", required=True)
    reference_get.add_argument("--include-deprecated", action="store_true")
    reference_get.set_defaults(func=cmd_reference_get)

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
