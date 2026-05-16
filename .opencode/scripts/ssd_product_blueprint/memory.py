#!/usr/bin/env python3
# /// script
# /// requires-python = ">=3.10"
# /// dependencies = ["graphqlite"]
# ///
"""ssd-product-blueprint memory adapter backed by GraphQLite."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

import ssd_memory.kernel as memory_kernel  # noqa: E402
from ssd_memory.kernel import fail, new_id, now_iso, open_graph, output, read_json_file  # noqa: E402
from ssd_memory.memory import (  # noqa: E402
    current_sections,
    get_artifact_by_kind,
    upsert_artifact,
    validate_sections,
)


KIND = "product-blueprint"
TITLE = "Product Blueprint"
REQUIRED_SECTIONS = [
    ("product-definition", "Product Definition"),
    ("in-scope", "In Scope"),
    ("out-of-scope", "Out Of Scope"),
    ("major-capabilities", "Major Capabilities"),
    ("product-principles", "Product Principles"),
    ("cross-cutting-concerns", "Cross-Cutting Concerns"),
    ("assumptions", "Assumptions"),
    ("major-unknowns", "Major Unknowns"),
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


def normalize_source_brainstorms(raw: Any) -> list[dict[str, Any]]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise ValueError("source_brainstorms must be an array")
    source_brainstorms: list[dict[str, Any]] = []
    for index, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"source_brainstorms[{index}] must be an object")
        brainstorm_id = item.get("brainstorm_id")
        role = item.get("role", "supplemental")
        if not isinstance(brainstorm_id, str) or not brainstorm_id.strip():
            raise ValueError(f"source_brainstorms[{index}] requires brainstorm_id")
        if not isinstance(role, str) or not role.strip():
            raise ValueError(f"source_brainstorms[{index}] requires role")
        handoff_command = item.get("handoff_command", [])
        if handoff_command is None:
            handoff_command = []
        if not isinstance(handoff_command, list):
            raise ValueError(f"source_brainstorms[{index}].handoff_command must be an array")
        source_brainstorms.append(
            {
                "brainstorm_id": brainstorm_id.strip(),
                "role": role.strip(),
                "handoff_command": handoff_command,
            }
        )
    return source_brainstorms


def normalize_source_artifacts(raw: Any) -> list[dict[str, Any]]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise ValueError("source_artifacts must be an array")
    source_artifacts: list[dict[str, Any]] = []
    for index, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"source_artifacts[{index}] must be an object")
        artifact_id = item.get("artifact_id")
        kind = item.get("kind")
        role = item.get("role", "extra_source")
        if not isinstance(artifact_id, str) or not artifact_id.strip():
            raise ValueError(f"source_artifacts[{index}] requires artifact_id")
        if not isinstance(kind, str) or not kind.strip():
            raise ValueError(f"source_artifacts[{index}] requires kind")
        if not isinstance(role, str) or not role.strip():
            raise ValueError(f"source_artifacts[{index}] requires role")
        source_artifacts.append(
            {"artifact_id": artifact_id.strip(), "kind": kind.strip(), "role": role.strip()}
        )
    return source_artifacts


def normalize_source_files(raw: Any) -> list[dict[str, Any]]:
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise ValueError("source_files must be an array")
    source_files: list[dict[str, Any]] = []
    for index, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"source_files[{index}] must be an object")
        path = item.get("path")
        title = item.get("title")
        role = item.get("role", "extra_source")
        if not isinstance(path, str) or not path.strip():
            raise ValueError(f"source_files[{index}] requires path")
        if title is not None and (not isinstance(title, str) or not title.strip()):
            raise ValueError(f"source_files[{index}].title must be a non-empty string")
        if not isinstance(role, str) or not role.strip():
            raise ValueError(f"source_files[{index}] requires role")
        source_files.append(
            {
                "path": path.strip(),
                "title": title.strip() if isinstance(title, str) else None,
                "role": role.strip(),
            }
        )
    return source_files


def normalize_sections(raw: Any) -> list[dict[str, Any]]:
    if isinstance(raw, dict):
        missing = [key for key in REQUIRED_KEYS if key not in raw]
        if missing:
            raise ValueError(f"Product Blueprint missing required sections: {', '.join(missing)}")
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
        raise ValueError(f"Product Blueprint missing required sections: {', '.join(missing)}")

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


def payload_to_memory_inputs(payload: dict[str, Any]) -> dict[str, Any]:
    product_brief_artifact_id = payload.get("product_brief_artifact_id")
    if not isinstance(product_brief_artifact_id, str) or not product_brief_artifact_id.strip():
        raise ValueError("product_brief_artifact_id is required")

    sections = normalize_sections(payload.get("sections"))
    source_brainstorms = normalize_source_brainstorms(payload.get("source_brainstorms"))
    source_artifacts = normalize_source_artifacts(payload.get("source_artifacts"))
    source_files = normalize_source_files(payload.get("source_files"))
    cited_idea_ids = normalize_refs(payload.get("cited_idea_ids"), "cited_idea_ids")

    return {
        "sections": sections,
        "change_summary": payload.get("change_summary") or "Create Product Blueprint",
        "product_brief_artifact_id": product_brief_artifact_id.strip(),
        "source_brainstorms": source_brainstorms,
        "source_artifacts": source_artifacts,
        "source_files": source_files,
        "cited_idea_ids": cited_idea_ids,
    }


def safe_basename(path: Path) -> str:
    name = re.sub(r"[^A-Za-z0-9._-]+", "-", path.name).strip("-._")
    return name or "source-file"


def workspace_relative(path: Path) -> str:
    resolved = path.resolve()
    cwd = Path.cwd().resolve()
    try:
        return str(resolved.relative_to(cwd))
    except ValueError as exc:
        raise ValueError(f"source file must be inside the workspace: {path}") from exc


def snapshot_source_file(graph: Any, source: dict[str, Any]) -> dict[str, Any]:
    original = Path(source["path"])
    if not original.is_file():
        raise ValueError(f"source file does not exist: {source['path']}")
    original_path = workspace_relative(original)
    content = original.read_bytes()
    digest = hashlib.sha256(content).hexdigest()
    basename = safe_basename(original)
    snapshot_dir = memory_kernel.MEMORY_DIR / "files"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    snapshot = snapshot_dir / f"{digest}-{basename}"
    if not snapshot.exists():
        shutil.copyfile(original, snapshot)
    snapshot_path = str(snapshot)

    rows = graph.query("MATCH (f:SourceFile) RETURN f")
    for row in rows:
        props = row["f"].get("properties", {})
        if props.get("snapshot_path") == snapshot_path:
            return {**props, "role": source["role"]}

    file_id = new_id()
    props = {
        "id": file_id,
        "kind": "source-file",
        "title": source["title"] or basename,
        "original_path": original_path,
        "snapshot_path": snapshot_path,
        "content_sha256": digest,
        "size_bytes": len(content),
        "created_at": now_iso(),
    }
    graph.upsert_node(file_id, props, label="SourceFile")
    return {**props, "role": source["role"]}


def add_provenance_edges(
    graph: Any,
    *,
    artifact_id: str,
    product_brief_artifact_id: str,
    source_brainstorms: list[dict[str, Any]],
    source_artifacts: list[dict[str, Any]],
    source_files: list[dict[str, Any]],
    cited_idea_ids: list[str],
) -> None:
    graph.upsert_edge(artifact_id, product_brief_artifact_id, {"type": "DERIVED_FROM"}, rel_type="DERIVED_FROM")
    for source in source_brainstorms:
        graph.upsert_edge(
            artifact_id,
            source["brainstorm_id"],
            {"type": "DERIVED_FROM", "role": source["role"]},
            rel_type="DERIVED_FROM",
        )
    for source in source_artifacts:
        graph.upsert_edge(
            artifact_id,
            source["artifact_id"],
            {"type": "DERIVED_FROM", "role": source["role"], "kind": source["kind"]},
            rel_type="DERIVED_FROM",
        )
    for source in source_files:
        file_node = snapshot_source_file(graph, source)
        graph.upsert_edge(
            artifact_id,
            file_node["id"],
            {"type": "DERIVED_FROM", "role": source["role"]},
            rel_type="DERIVED_FROM",
        )
    for idea_id in cited_idea_ids:
        graph.upsert_edge(artifact_id, idea_id, {"type": "CITES"}, rel_type="CITES")


def current_product_blueprint(graph: Any) -> dict[str, Any]:
    artifact = get_artifact_by_kind(graph, KIND)
    if artifact is None:
        raise ValueError("Product Blueprint does not exist")
    return {
        "status": "ok",
        "artifact": artifact,
        "sections": current_sections(graph, KIND),
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
            product_brief_artifact_id=memory_inputs["product_brief_artifact_id"],
            source_brainstorms=memory_inputs["source_brainstorms"],
            source_artifacts=memory_inputs["source_artifacts"],
            source_files=memory_inputs["source_files"],
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
        result = current_product_blueprint(graph)
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
            raise ValueError(f"Product Blueprint does not exist: {args.artifact_id}")
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
