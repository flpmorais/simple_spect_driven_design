from __future__ import annotations

import json

import pytest

from .conftest import assert_uuid, stdout_json, write_json


def sections(**overrides):
    data = {
        "architecture-recommendations": "### Data store - Recommendation: SQLite-backed local memory for SSD prototype state. - Confidence: Strong recommendation - Why: Current workflows are local and memory-backed. - Ideal approach: Durable local graph-backed artifact memory. - Acceptable compromise: SQLite with clear adapter boundaries. - Rejected alternatives: External databases until collaboration needs exist. - Phase 1 validation: Confirm local-only prototype constraints.",
        "decision-coverage": "| Area | Status | Recommendation Summary | Rationale | | --- | --- | --- | --- | | Data store | Recommended | SQLite-backed local memory | Current prototype state is local | | Payments/billing | Not needed | None | No monetization flow is in scope |",
        "open-risks": "If collaboration or hosted workflows become required, local SQLite may no longer be sufficient.",
        "phase-1-validation": "Validate whether the prototype remains local-only before downstream planning depends on SQLite.",
    }
    data.update(overrides)
    return data


def payload(**overrides):
    data = {
        "product_blueprint_artifact_id": "00000000-0000-4000-8000-000000000002",
        "product_brief_artifact_id": "00000000-0000-4000-8000-000000000001",
        "source_brainstorms": [
            {
                "brainstorm_id": "brainstorm-1",
                "role": "architecture_roundtable",
                "handoff_command": [
                    "python3",
                    ".opencode/scripts/ssd_brainstorming/memory.py",
                    "ideas",
                    "--brainstorm-id",
                    "brainstorm-1",
                ],
            }
        ],
        "cited_idea_ids": ["idea-1"],
        "sections": sections(),
        "change_summary": "Initial Architecture Blueprint",
    }
    data.update(overrides)
    return data


def create_architecture_blueprint(architecture_blueprint_memory, tmp_path, args, capsys, **overrides):
    path = write_json(tmp_path / "architecture-blueprint.json", payload(**overrides))
    architecture_blueprint_memory.cmd_create(args(payload_json=str(path)))
    return stdout_json(capsys)


def create_source_nodes(architecture_blueprint_memory):
    graph = architecture_blueprint_memory.open_graph()
    try:
        graph.upsert_node(
            "00000000-0000-4000-8000-000000000001",
            {"id": "00000000-0000-4000-8000-000000000001", "kind": "product-brief"},
            label="Artifact",
        )
        graph.upsert_node(
            "00000000-0000-4000-8000-000000000002",
            {"id": "00000000-0000-4000-8000-000000000002", "kind": "product-blueprint"},
            label="Artifact",
        )
        graph.upsert_node("brainstorm-1", {"id": "brainstorm-1", "title": "Brainstorm 1"}, label="Brainstorm")
        graph.upsert_node("idea-1", {"id": "idea-1", "title": "Idea 1"}, label="BrainstormIdea")
        graph.reload_graph()
    finally:
        graph.close()


def test_create_get_and_context(architecture_blueprint_memory, tmp_path, args, capsys):
    create_source_nodes(architecture_blueprint_memory)
    created = create_architecture_blueprint(architecture_blueprint_memory, tmp_path, args, capsys)
    assert created["status"] == "ok"
    assert created["artifact_kind"] == "architecture-blueprint"
    assert_uuid(created["artifact_id"])

    architecture_blueprint_memory.cmd_get(args())
    current = stdout_json(capsys)
    assert current["artifact"]["kind"] == "architecture-blueprint"
    assert [section["section_key"] for section in current["sections"]] == architecture_blueprint_memory.REQUIRED_KEYS
    assert [section["canonical_text"] for section in current["sections"] if section["section_key"] == "architecture-recommendations"] == [sections()["architecture-recommendations"]]

    graph = architecture_blueprint_memory.open_graph()
    try:
        edges = graph.get_edges_from(created["artifact_id"])
        assert any(edge["target"] == "00000000-0000-4000-8000-000000000002" and edge["r"]["type"] == "DERIVED_FROM" for edge in edges)
        assert any(edge["target"] == "00000000-0000-4000-8000-000000000001" and edge["r"]["type"] == "DERIVED_FROM" for edge in edges)
        assert any(edge["target"] == "brainstorm-1" and edge["r"]["type"] == "DERIVED_FROM" for edge in edges)
        assert any(edge["target"] == "idea-1" and edge["r"]["type"] == "CITES" for edge in edges)
    finally:
        graph.close()


def test_duplicate_create_and_missing_required_section_failures(
    architecture_blueprint_memory, tmp_path, args, capsys
):
    create_architecture_blueprint(architecture_blueprint_memory, tmp_path, args, capsys)
    with pytest.raises(ValueError, match="already exists"):
        architecture_blueprint_memory.cmd_create(
            args(payload_json=str(write_json(tmp_path / "again.json", payload())))
        )

    incomplete = sections()
    del incomplete["decision-coverage"]
    with pytest.raises(ValueError, match="missing required sections: decision-coverage"):
        architecture_blueprint_memory.normalize_sections(incomplete)


def test_product_blueprint_source_required(architecture_blueprint_memory):
    raw = payload()
    del raw["product_blueprint_artifact_id"]
    with pytest.raises(ValueError, match="product_blueprint_artifact_id is required"):
        architecture_blueprint_memory.payload_to_memory_inputs(raw)


def test_create_accepts_payload_from_stdin(architecture_blueprint_memory, monkeypatch, args, capsys):
    from io import StringIO

    monkeypatch.setattr("sys.stdin", StringIO(json.dumps(payload())))
    architecture_blueprint_memory.cmd_create(args(payload_json=None))
    created = stdout_json(capsys)
    assert created["status"] == "ok"


def test_delete_removes_architecture_blueprint_owned_nodes(architecture_blueprint_memory, tmp_path, args, capsys):
    create_source_nodes(architecture_blueprint_memory)
    created = create_architecture_blueprint(architecture_blueprint_memory, tmp_path, args, capsys)

    architecture_blueprint_memory.cmd_delete(
        args(artifact_id=created["artifact_id"], confirm=created["artifact_id"])
    )
    deleted = stdout_json(capsys)
    assert deleted["status"] == "ok"
    assert deleted["deleted"]["artifact_kind"] == "architecture-blueprint"
    assert deleted["deleted"]["nodes"] == 5

    graph = architecture_blueprint_memory.open_graph()
    try:
        with pytest.raises(ValueError, match="Architecture Blueprint does not exist"):
            architecture_blueprint_memory.current_architecture_blueprint(graph)
    finally:
        graph.close()


def test_delete_requires_matching_confirmation(architecture_blueprint_memory, tmp_path, args, capsys):
    created = create_architecture_blueprint(architecture_blueprint_memory, tmp_path, args, capsys)

    with pytest.raises(ValueError, match="Confirmation does not match artifact_id"):
        architecture_blueprint_memory.cmd_delete(
            args(artifact_id=created["artifact_id"], confirm="different")
        )


def test_source_brainstorm_validation(architecture_blueprint_memory):
    with pytest.raises(ValueError, match=r"source_brainstorms\[1\] requires brainstorm_id"):
        architecture_blueprint_memory.normalize_source_brainstorms([{"role": "architecture_roundtable"}])
    with pytest.raises(ValueError, match="handoff_command must be an array"):
        architecture_blueprint_memory.normalize_source_brainstorms(
            [{"brainstorm_id": "brainstorm-1", "handoff_command": "not-array"}]
        )


def test_main_returns_error_for_missing_architecture_blueprint(architecture_blueprint_memory, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["memory.py", "get"])
    assert architecture_blueprint_memory.main() == 1
    assert "Architecture Blueprint does not exist" in json.loads(capsys.readouterr().err)["error"]
