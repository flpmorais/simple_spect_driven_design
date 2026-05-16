from __future__ import annotations

import json

import pytest

from .conftest import assert_uuid, stdout_json, write_json


def sections(**overrides):
    data = {
        "why-this-exists": "Teams need a clearer reason for this product to exist.",
        "product-definition": "A product definition assistant for early planning.",
        "problem": "Planning jumps to implementation before product intent is clear.",
        "high-level-solution": "Guide the user through a concise product brief.",
        "audience": "Product-minded builders and small teams.",
        "necessity-and-differentiation": "It keeps product definition separate from delivery planning.",
        "positioning": "Positioned as an early product clarity workflow.",
        "practical-constraints": "Must avoid implementation detail.",
        "assumptions": "Users can answer a few strategic questions.",
        "open-questions": "Which audience segment should be prioritized first?",
    }
    data.update(overrides)
    return data


def payload(**overrides):
    data = {
        "sections": sections(),
        "change_summary": "Initial Product Brief",
    }
    data.update(overrides)
    return data


def create_product_brief(product_brief_memory, tmp_path, args, capsys, **overrides):
    path = write_json(tmp_path / "product-brief.json", payload(**overrides))
    product_brief_memory.cmd_create(args(payload_json=str(path)))
    return stdout_json(capsys)


def create_source_nodes(product_brief_memory):
    graph = product_brief_memory.open_graph()
    try:
        graph.upsert_node("brainstorm-1", {"id": "brainstorm-1", "title": "Brainstorm 1"}, label="Brainstorm")
        graph.upsert_node("idea-1", {"id": "idea-1", "title": "Idea 1"}, label="BrainstormIdea")
        graph.reload_graph()
    finally:
        graph.close()


def create_duplicate_product_brief_artifacts(product_brief_memory):
    graph = product_brief_memory.open_graph()
    try:
        for artifact_id in ["brief-1", "brief-2"]:
            graph.upsert_node(
                artifact_id,
                {
                    "id": artifact_id,
                    "kind": "product-brief",
                    "title": "Product Brief",
                    "status": "accepted",
                },
                label="Artifact",
            )
        graph.reload_graph()
    finally:
        graph.close()


def test_create_get_and_context(product_brief_memory, tmp_path, args, capsys):
    create_source_nodes(product_brief_memory)
    created = create_product_brief(
        product_brief_memory,
        tmp_path,
        args,
        capsys,
        cited_brainstorm_ids=["brainstorm-1"],
        cited_idea_ids=["idea-1"],
    )
    assert created["status"] == "ok"
    assert created["artifact_kind"] == "product-brief"
    assert_uuid(created["artifact_id"])

    product_brief_memory.cmd_get(args())
    current = stdout_json(capsys)
    assert current["artifact"]["kind"] == "product-brief"
    assert [section["section_key"] for section in current["sections"]] == product_brief_memory.REQUIRED_KEYS
    assert current["cited_brainstorm_ids"] == ["brainstorm-1"]
    assert current["cited_idea_ids"] == ["idea-1"]


def test_duplicate_create_and_missing_required_section_failures(product_brief_memory, tmp_path, args, capsys):
    create_product_brief(product_brief_memory, tmp_path, args, capsys)
    with pytest.raises(ValueError, match="already exists"):
        product_brief_memory.cmd_create(args(payload_json=str(write_json(tmp_path / "again.json", payload()))))

    incomplete = sections()
    del incomplete["audience"]
    with pytest.raises(ValueError, match="missing required sections: audience"):
        product_brief_memory.normalize_sections(incomplete)


def test_duplicate_product_brief_artifacts_are_corrupt_state(
    product_brief_memory, tmp_path, args
):
    create_duplicate_product_brief_artifacts(product_brief_memory)
    message = "Multiple Artifacts exist for kind: product-brief"

    with pytest.raises(ValueError, match=message):
        product_brief_memory.cmd_get(args())

    with pytest.raises(ValueError, match=message):
        product_brief_memory.cmd_create(
            args(payload_json=str(write_json(tmp_path / "create.json", payload())))
        )

    with pytest.raises(ValueError, match=message):
        product_brief_memory.cmd_update(
            args(payload_json=str(write_json(tmp_path / "update.json", payload())))
        )

    with pytest.raises(ValueError, match=message):
        product_brief_memory.cmd_delete(args(artifact_id="brief-1", confirm="brief-1"))


def test_update_replaces_current_state_and_preserves_provenance(product_brief_memory, tmp_path, args, capsys):
    create_source_nodes(product_brief_memory)
    created = create_product_brief(
        product_brief_memory,
        tmp_path,
        args,
        capsys,
        cited_brainstorm_ids=["brainstorm-1"],
        cited_idea_ids=["idea-1"],
    )
    updated_payload = payload(
        sections=sections(problem="Updated product-level problem."),
        change_summary="Clarify problem",
    )
    update_path = write_json(tmp_path / "update.json", updated_payload)
    product_brief_memory.cmd_update(args(payload_json=str(update_path)))
    updated = stdout_json(capsys)
    assert updated["artifact_id"] == created["artifact_id"]

    product_brief_memory.cmd_get(args())
    current = stdout_json(capsys)
    problem_current = [
        section for section in current["sections"] if section["section_key"] == "problem"
    ][0]
    assert problem_current["canonical_text"] == "Updated product-level problem."

    graph = product_brief_memory.open_graph()
    try:
        edges = graph.get_edges_from(created["artifact_id"])
        assert any(edge["target"] == "brainstorm-1" and edge["r"]["type"] == "DERIVED_FROM" for edge in edges)
        assert any(edge["target"] == "idea-1" and edge["r"]["type"] == "CITES" for edge in edges)
        assert len(graph.query("MATCH (n) RETURN n")) == 13
    finally:
        graph.close()


def test_payload_must_be_object(product_brief_memory, tmp_path):
    with pytest.raises(ValueError, match="payload must be a JSON object"):
        product_brief_memory.read_payload(str(write_json(tmp_path / "array.json", [])))


def test_create_accepts_payload_from_stdin(product_brief_memory, monkeypatch, args, capsys):
    from io import StringIO

    monkeypatch.setattr("sys.stdin", StringIO(json.dumps(payload())))
    product_brief_memory.cmd_create(args(payload_json=None))
    created = stdout_json(capsys)
    assert created["status"] == "ok"


def test_delete_product_brief_removes_artifact_children_and_relationships(
    product_brief_memory, tmp_path, args, capsys
):
    created = create_product_brief(product_brief_memory, tmp_path, args, capsys)
    artifact_id = created["artifact_id"]

    with pytest.raises(ValueError, match="Confirmation does not match artifact_id"):
        product_brief_memory.cmd_delete(args(artifact_id=artifact_id, confirm="wrong"))

    product_brief_memory.cmd_delete(args(artifact_id=artifact_id, confirm=artifact_id))
    deleted = stdout_json(capsys)
    assert deleted == {
        "status": "ok",
        "deleted": {
            "artifact_id": artifact_id,
            "artifact_kind": "product-brief",
            "nodes": 11,
        },
    }

    with pytest.raises(ValueError, match="Product Brief does not exist"):
        product_brief_memory.current_product_brief(product_brief_memory.open_graph())

    graph = product_brief_memory.open_graph()
    try:
        rows = graph.query("MATCH (n) RETURN n")
        assert rows == []
    finally:
        graph.close()


def test_main_returns_error_for_missing_product_brief(product_brief_memory, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["memory.py", "get"])
    assert product_brief_memory.main() == 1
    assert "Product Brief does not exist" in json.loads(capsys.readouterr().err)["error"]
