#!/usr/bin/env python3
# /// script
# /// requires-python = ">=3.10"
# /// dependencies = ["graphqlite"]
# ///
"""ssd-brainstorming memory adapter backed by GraphQLite."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

SCRIPT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPT_ROOT))

from ssd_memory.kernel import (  # noqa: E402
    fail,
    json_text,
    maybe_json,
    new_id,
    node_props,
    now_iso,
    open_graph,
    output,
    read_json_file,
)


def decoded_brainstorm(props: dict[str, Any]) -> dict[str, Any]:
    decoded = dict(props)
    for key in ("constraints", "techniques"):
        if key in decoded:
            decoded[key] = maybe_json(decoded[key])
    return decoded


def get_brainstorm(graph: Any, brainstorm_id: str) -> dict[str, Any]:
    node = graph.get_node(brainstorm_id)
    brainstorm = node_props(node)
    if brainstorm is None or "Brainstorm" not in node.get("labels", []):
        raise ValueError(f"Brainstorm does not exist: {brainstorm_id}")
    return brainstorm


def require_active_brainstorm(graph: Any, brainstorm_id: str) -> dict[str, Any]:
    brainstorm = get_brainstorm(graph, brainstorm_id)
    if brainstorm.get("status") != "active":
        raise ValueError(f"Brainstorm is not active: {brainstorm_id}")
    return brainstorm


def brainstorm_ideas(graph: Any, brainstorm_id: str, *, include_superseded: bool = False) -> list[dict[str, Any]]:
    ideas: list[dict[str, Any]] = []
    for edge in graph.get_edges_from(brainstorm_id):
        if edge.get("r", {}).get("type") != "HAS_IDEA":
            continue
        props = node_props(graph.get_node(edge["target"]))
        if props and (include_superseded or not props.get("superseded", False)):
            normalized = dict(props)
            normalized["superseded"] = bool(normalized.get("superseded", False))
            ideas.append(normalized)
    return sorted(ideas, key=lambda item: (item.get("number", 0), item.get("revision", 1)))


def existing_idea_numbers(graph: Any, brainstorm_id: str) -> dict[int, str]:
    result: dict[int, str] = {}
    for idea in brainstorm_ideas(graph, brainstorm_id):
        number = idea.get("number")
        if isinstance(number, int):
            result[number] = idea["id"]
    return result


def current_idea_by_number(graph: Any, brainstorm_id: str, number: int) -> dict[str, Any] | None:
    for idea in brainstorm_ideas(graph, brainstorm_id):
        if idea.get("number") == number:
            return idea
    return None


def cypher_string(value: str) -> str:
    return json.dumps(value)


def validate_ideas(raw: Any, *, start_number: int) -> list[dict[str, Any]]:
    if not isinstance(raw, list) or not raw:
        raise ValueError("ideas-json must contain a non-empty array")
    ideas: list[dict[str, Any]] = []
    seen: set[int] = set()
    for index, item in enumerate(raw, start=0):
        if not isinstance(item, dict):
            raise ValueError(f"Idea #{index + 1} must be an object")
        number = item.get("number", start_number + index)
        if not isinstance(number, int) or number <= 0:
            raise ValueError(f"Idea #{index + 1} requires a positive integer number")
        if number in seen:
            raise ValueError(f"Duplicate idea number in input: {number}")
        seen.add(number)

        title = item.get("title")
        concept = item.get("concept")
        rationale = item.get("rationale", item.get("why_it_might_work"))
        hidden_assumption = item.get("hidden_assumption")
        risk = item.get("risk", item.get("failure_mode_or_risk"))
        domain = item.get("domain")
        for field_name, field_value in (
            ("title", title),
            ("concept", concept),
            ("rationale", rationale),
            ("hidden_assumption", hidden_assumption),
            ("risk", risk),
            ("domain", domain),
        ):
            if not isinstance(field_value, str) or not field_value.strip():
                raise ValueError(f"Idea #{number} requires {field_name}")

        ideas.append(
            {
                "number": number,
                "title": title.strip(),
                "concept": concept.strip(),
                "rationale": rationale.strip(),
                "hidden_assumption": hidden_assumption.strip(),
                "risk": risk.strip(),
                "domain": domain.strip(),
                "technique": item.get("technique", "unknown"),
            }
        )
    return ideas


def cmd_create(args: argparse.Namespace) -> int:
    graph = open_graph()
    try:
        timestamp = now_iso()
        brainstorm_id = new_id()
        constraints = read_json_file(args.constraints_json) if args.constraints_json else []
        techniques = read_json_file(args.techniques_json) if args.techniques_json else []
        props = {
            "id": brainstorm_id,
            "title": args.topic,
            "topic": args.topic,
            "goal": args.goal,
            "initial_context": args.initial_context or "",
            "scope": args.scope,
            "target_ideas": args.target_ideas,
            "mode": args.mode,
            "downstream_consumer": args.downstream_consumer,
            "constraints": json_text(constraints),
            "techniques": json_text(techniques),
            "status": "active",
            "created_at": timestamp,
            "finished_at": "",
        }
        graph.upsert_node(brainstorm_id, props, label="Brainstorm")
        graph.reload_graph()
    finally:
        graph.close()
    output({"status": "ok", "brainstorm_id": brainstorm_id})
    return 0


def cmd_append_ideas(args: argparse.Namespace) -> int:
    graph = open_graph()
    try:
        require_active_brainstorm(graph, args.brainstorm_id)
        current_numbers = existing_idea_numbers(graph, args.brainstorm_id)
        start_number = max(current_numbers.keys(), default=0) + 1
        ideas = validate_ideas(read_json_file(args.ideas_json), start_number=start_number)
        timestamp = now_iso()
        idea_ids: list[str] = []
        for idea in ideas:
            if idea["number"] in current_numbers:
                raise ValueError(f"Idea number already exists: {idea['number']}")
            idea_id = new_id()
            props = {
                "id": idea_id,
                "brainstorm_id": args.brainstorm_id,
                "created_at": timestamp,
                "updated_at": timestamp,
                "revision": 1,
                "revision_of": "",
                "superseded": False,
                **idea,
            }
            graph.upsert_node(idea_id, props, label="BrainstormIdea")
            graph.upsert_edge(args.brainstorm_id, idea_id, {"type": "HAS_IDEA"}, rel_type="HAS_IDEA")
            idea_ids.append(idea_id)
        graph.reload_graph()
    finally:
        graph.close()
    output({"status": "ok", "brainstorm_id": args.brainstorm_id, "idea_ids": idea_ids})
    return 0


def cmd_revise_idea(args: argparse.Namespace) -> int:
    graph = open_graph()
    try:
        require_active_brainstorm(graph, args.brainstorm_id)
        current = current_idea_by_number(graph, args.brainstorm_id, args.idea_number)
        if current is None:
            raise ValueError(f"Idea number does not exist: {args.idea_number}")
        raw = read_json_file(args.idea_json)
        ideas = validate_ideas([raw], start_number=args.idea_number)
        idea = {**ideas[0], "number": args.idea_number}
        timestamp = now_iso()
        superseded = {**current, "superseded": True, "updated_at": timestamp}
        graph.upsert_node(current["id"], superseded, label="BrainstormIdea")
        revised_id = new_id()
        root_revision_id = current.get("revision_of") or current["id"]
        props = {
            "id": revised_id,
            "brainstorm_id": args.brainstorm_id,
            "created_at": timestamp,
            "updated_at": timestamp,
            "revision": int(current.get("revision", 1)) + 1,
            "revision_of": root_revision_id,
            "superseded": False,
            **idea,
        }
        graph.upsert_node(revised_id, props, label="BrainstormIdea")
        graph.upsert_edge(args.brainstorm_id, revised_id, {"type": "HAS_IDEA"}, rel_type="HAS_IDEA")
        graph.upsert_edge(revised_id, current["id"], {"type": "REVISION_OF"}, rel_type="REVISION_OF")
        graph.reload_graph()
    finally:
        graph.close()
    output(
        {
            "status": "ok",
            "brainstorm_id": args.brainstorm_id,
            "idea_number": args.idea_number,
            "superseded_idea_id": current["id"],
            "revised_idea_id": revised_id,
        }
    )
    return 0


def cmd_finish(args: argparse.Namespace) -> int:
    graph = open_graph()
    try:
        brainstorm = require_active_brainstorm(graph, args.brainstorm_id)
        timestamp = now_iso()
        props = {
            **brainstorm,
            "status": args.status,
            "finished_at": timestamp,
            "updated_at": timestamp,
        }
        graph.upsert_node(args.brainstorm_id, props, label="Brainstorm")
        graph.reload_graph()
    finally:
        graph.close()
    output(
        {
            "status": "ok",
            "brainstorm_id": args.brainstorm_id,
            "brainstorm_status": args.status,
        }
    )
    return 0


def cmd_ideas(args: argparse.Namespace) -> int:
    graph = open_graph()
    try:
        brainstorm = decoded_brainstorm(get_brainstorm(graph, args.brainstorm_id))
        ideas = brainstorm_ideas(
            graph,
            args.brainstorm_id,
            include_superseded=getattr(args, "include_superseded", False),
        )
    finally:
        graph.close()
    output({"status": "ok", "brainstorm": brainstorm, "ideas": ideas})
    return 0


def cmd_list(_: argparse.Namespace) -> int:
    graph = open_graph()
    try:
        rows = graph.query("MATCH (b:Brainstorm) RETURN b ORDER BY b.topic")
        brainstorms = []
        for row in rows:
            props = row["b"]["properties"]
            brainstorms.append(
                {
                    "id": props.get("id", ""),
                    "title": props.get("title", props.get("topic", "")),
                    "topic": props.get("topic", ""),
                    "goal": props.get("goal", ""),
                    "scope": props.get("scope", ""),
                    "target_ideas": props.get("target_ideas", 0),
                    "mode": props.get("mode", ""),
                    "downstream_consumer": props.get("downstream_consumer", ""),
                    "status": props.get("status", ""),
                    "created_at": props.get("created_at", ""),
                    "finished_at": props.get("finished_at", ""),
                }
            )
    finally:
        graph.close()
    output({"status": "ok", "brainstorms": brainstorms})
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    if args.confirm != args.brainstorm_id:
        raise ValueError("Confirmation does not match brainstorm_id")

    graph = open_graph()
    try:
        get_brainstorm(graph, args.brainstorm_id)
        brainstorm_id = cypher_string(args.brainstorm_id)
        rows = graph.query(
            f"MATCH (n) WHERE n.id = {brainstorm_id} OR n.brainstorm_id = {brainstorm_id} RETURN n"
        )
        brainstorm_count = 0
        idea_count = 0
        for row in rows:
            labels = row["n"].get("labels", [])
            if "Brainstorm" in labels:
                brainstorm_count += 1
            elif "BrainstormIdea" in labels:
                idea_count += 1
        graph.query(
            f"MATCH (n) WHERE n.id = {brainstorm_id} OR n.brainstorm_id = {brainstorm_id} DETACH DELETE n"
        )
        graph.reload_graph()
    finally:
        graph.close()
    output(
        {
            "status": "ok",
            "deleted": {
                "brainstorm_id": args.brainstorm_id,
                "brainstorms": brainstorm_count,
                "ideas": idea_count,
                "nodes": len(rows),
            },
        }
    )
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create")
    create.add_argument("--topic", required=True)
    create.add_argument("--goal", required=True)
    create.add_argument("--initial-context", default="")
    create.add_argument("--scope", default="normal")
    create.add_argument("--target-ideas", required=True, type=int)
    create.add_argument("--mode", default="guided")
    create.add_argument("--downstream-consumer", default="general")
    create.add_argument("--constraints-json")
    create.add_argument("--techniques-json")
    create.set_defaults(func=cmd_create)

    append_ideas = subparsers.add_parser("append-ideas")
    append_ideas.add_argument("--brainstorm-id", required=True)
    append_ideas.add_argument("--ideas-json", required=True)
    append_ideas.set_defaults(func=cmd_append_ideas)

    revise_idea = subparsers.add_parser("revise-idea")
    revise_idea.add_argument("--brainstorm-id", required=True)
    revise_idea.add_argument("--idea-number", required=True, type=int)
    revise_idea.add_argument("--idea-json", required=True)
    revise_idea.set_defaults(func=cmd_revise_idea)

    finish = subparsers.add_parser("finish")
    finish.add_argument("--brainstorm-id", required=True)
    finish.add_argument("--status", choices=("complete", "complete_with_warnings"), required=True)
    finish.set_defaults(func=cmd_finish)

    ideas = subparsers.add_parser("ideas")
    ideas.add_argument("--brainstorm-id", required=True)
    ideas.add_argument("--include-superseded", action="store_true")
    ideas.set_defaults(func=cmd_ideas)

    get = subparsers.add_parser("get")
    get.add_argument("--brainstorm-id", required=True)
    get.add_argument("--include-superseded", action="store_true")
    get.set_defaults(func=cmd_ideas)

    list_parser = subparsers.add_parser("list")
    list_parser.set_defaults(func=cmd_list)

    delete = subparsers.add_parser("delete")
    delete.add_argument("--brainstorm-id", required=True)
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
