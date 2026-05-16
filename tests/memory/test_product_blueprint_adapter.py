from __future__ import annotations

import json

import pytest

from .conftest import assert_uuid, stdout_json, write_json


def sections(**overrides):
    data = {
        "product-definition": "A conceptual product shape for SSD planning.",
        "in-scope": "Product definition, boundaries, capabilities, principles, and unknowns.",
        "out-of-scope": "Implementation detail, architecture, delivery sequencing, and metrics.",
        "major-capabilities": "Brief creation, blueprint creation, memory-backed handoff, and review gates.",
        "product-principles": "Keep product definition separate from engineering execution.",
        "cross-cutting-concerns": "Traceability, source-backed content, and durable memory references.",
        "assumptions": "Users want guided product shaping before implementation planning.",
        "major-unknowns": "How much product detail is enough before downstream work starts?",
    }
    data.update(overrides)
    return data


def payload(**overrides):
    data = {
        "product_brief_artifact_id": "00000000-0000-4000-8000-000000000001",
        "source_brainstorms": [
            {
                "brainstorm_id": "brainstorm-1",
                "role": "product_dream",
                "handoff_command": [
                    "python3",
                    ".opencode/scripts/ssd_brainstorming/memory.py",
                    "ideas",
                    "--brainstorm-id",
                    "brainstorm-1",
                ],
            },
            {
                "brainstorm_id": "brainstorm-2",
                "role": "supplemental",
                "handoff_command": [
                    "python3",
                    ".opencode/scripts/ssd_brainstorming/memory.py",
                    "ideas",
                    "--brainstorm-id",
                    "brainstorm-2",
                ],
            },
        ],
        "cited_idea_ids": ["idea-1", "idea-2"],
        "source_artifacts": [
            {
                "artifact_id": "artifact-extra",
                "kind": "architecture-blueprint",
                "role": "extra_source",
            }
        ],
        "sections": sections(),
        "change_summary": "Initial Product Blueprint",
    }
    data.update(overrides)
    return data


def create_product_blueprint(product_blueprint_memory, tmp_path, args, capsys, **overrides):
    path = write_json(tmp_path / "product-blueprint.json", payload(**overrides))
    product_blueprint_memory.cmd_create(args(payload_json=str(path)))
    return stdout_json(capsys)


def create_source_nodes(product_blueprint_memory):
    graph = product_blueprint_memory.open_graph()
    try:
        graph.upsert_node(
            "00000000-0000-4000-8000-000000000001",
            {"artifact_id": "00000000-0000-4000-8000-000000000001", "kind": "product-brief"},
            label="Artifact",
        )
        graph.upsert_node("brainstorm-1", {"id": "brainstorm-1", "title": "Brainstorm 1"}, label="Brainstorm")
        graph.upsert_node("idea-1", {"id": "idea-1", "title": "Idea 1"}, label="BrainstormIdea")
        graph.upsert_node(
            "artifact-extra",
            {"id": "artifact-extra", "kind": "architecture-blueprint", "title": "Architecture Blueprint"},
            label="Artifact",
        )
        graph.reload_graph()
    finally:
        graph.close()


def test_create_get_and_context(product_blueprint_memory, tmp_path, args, capsys):
    create_source_nodes(product_blueprint_memory)
    created = create_product_blueprint(product_blueprint_memory, tmp_path, args, capsys)
    assert created["status"] == "ok"
    assert created["artifact_kind"] == "product-blueprint"
    assert_uuid(created["artifact_id"])

    product_blueprint_memory.cmd_get(args())
    current = stdout_json(capsys)
    assert current["artifact"]["kind"] == "product-blueprint"
    assert [section["section_key"] for section in current["sections"]] == product_blueprint_memory.REQUIRED_KEYS
    assert [section["canonical_text"] for section in current["sections"] if section["section_key"] == "in-scope"] == [sections()["in-scope"]]

    graph = product_blueprint_memory.open_graph()
    try:
        edges = graph.get_edges_from(created["artifact_id"])
        assert any(edge["target"] == "00000000-0000-4000-8000-000000000001" and edge["r"]["type"] == "DERIVED_FROM" for edge in edges)
        assert any(edge["target"] == "brainstorm-1" and edge["r"]["type"] == "DERIVED_FROM" for edge in edges)
        assert any(edge["target"] == "artifact-extra" and edge["r"]["properties"].get("role") == "extra_source" for edge in edges)
        assert any(edge["target"] == "idea-1" and edge["r"]["type"] == "CITES" for edge in edges)
    finally:
        graph.close()


def test_duplicate_create_and_missing_required_section_failures(
    product_blueprint_memory, tmp_path, args, capsys
):
    create_product_blueprint(product_blueprint_memory, tmp_path, args, capsys)
    with pytest.raises(ValueError, match="already exists"):
        product_blueprint_memory.cmd_create(
            args(payload_json=str(write_json(tmp_path / "again.json", payload())))
        )

    incomplete = sections()
    del incomplete["out-of-scope"]
    with pytest.raises(ValueError, match="missing required sections: out-of-scope"):
        product_blueprint_memory.normalize_sections(incomplete)


def test_product_brief_source_required(product_blueprint_memory):
    raw = payload()
    del raw["product_brief_artifact_id"]
    with pytest.raises(ValueError, match="product_brief_artifact_id is required"):
        product_blueprint_memory.payload_to_memory_inputs(raw)


def test_create_accepts_payload_from_stdin(product_blueprint_memory, monkeypatch, args, capsys):
    from io import StringIO
    import json

    monkeypatch.setattr("sys.stdin", StringIO(json.dumps(payload())))
    product_blueprint_memory.cmd_create(args(payload_json=None))
    created = stdout_json(capsys)
    assert created["status"] == "ok"


def test_delete_removes_product_blueprint_owned_nodes(product_blueprint_memory, tmp_path, args, capsys):
    create_source_nodes(product_blueprint_memory)
    created = create_product_blueprint(product_blueprint_memory, tmp_path, args, capsys)

    product_blueprint_memory.cmd_delete(
        args(artifact_id=created["artifact_id"], confirm=created["artifact_id"])
    )
    deleted = stdout_json(capsys)
    assert deleted["status"] == "ok"
    assert deleted["deleted"]["artifact_kind"] == "product-blueprint"
    assert deleted["deleted"]["nodes"] == 9

    graph = product_blueprint_memory.open_graph()
    try:
        with pytest.raises(ValueError, match="Product Blueprint does not exist"):
            product_blueprint_memory.current_product_blueprint(graph)
    finally:
        graph.close()


def test_delete_requires_matching_confirmation(product_blueprint_memory, tmp_path, args, capsys):
    created = create_product_blueprint(product_blueprint_memory, tmp_path, args, capsys)

    with pytest.raises(ValueError, match="Confirmation does not match artifact_id"):
        product_blueprint_memory.cmd_delete(
            args(artifact_id=created["artifact_id"], confirm="different")
        )


def test_source_brainstorm_validation(product_blueprint_memory):
    with pytest.raises(ValueError, match=r"source_brainstorms\[1\] requires brainstorm_id"):
        product_blueprint_memory.normalize_source_brainstorms([{"role": "product_dream"}])
    with pytest.raises(ValueError, match="handoff_command must be an array"):
        product_blueprint_memory.normalize_source_brainstorms(
            [{"brainstorm_id": "brainstorm-1", "handoff_command": "not-array"}]
        )


def test_source_artifact_validation(product_blueprint_memory):
    with pytest.raises(ValueError, match=r"source_artifacts\[1\] requires artifact_id"):
        product_blueprint_memory.normalize_source_artifacts([{"kind": "product-brief"}])
    with pytest.raises(ValueError, match=r"source_artifacts\[1\] requires kind"):
        product_blueprint_memory.normalize_source_artifacts([{"artifact_id": "artifact-1"}])


def test_source_file_snapshot_and_edge(
    product_blueprint_memory, tmp_path, monkeypatch, args, capsys
):
    monkeypatch.chdir(tmp_path)
    source = tmp_path / "notes.md"
    source.write_text("source notes", encoding="utf-8")
    create_source_nodes(product_blueprint_memory)

    created = create_product_blueprint(
        product_blueprint_memory,
        tmp_path,
        args,
        capsys,
        source_files=[{"path": "notes.md", "title": "Notes", "role": "extra_source"}],
    )

    graph = product_blueprint_memory.open_graph()
    try:
        source_files = graph.query("MATCH (f:SourceFile) RETURN f")
        assert len(source_files) == 1
        props = source_files[0]["f"]["properties"]
        assert props["title"] == "Notes"
        assert props["original_path"] == "notes.md"
        assert props["content_sha256"]
        assert props["size_bytes"] == len("source notes")
        assert (tmp_path / props["snapshot_path"]).is_file() or product_blueprint_memory.Path(props["snapshot_path"]).is_file()

        edges = graph.get_edges_from(created["artifact_id"])
        assert any(edge["target"] == props["id"] and edge["r"]["properties"].get("role") == "extra_source" for edge in edges)
    finally:
        graph.close()


def test_source_file_validation(product_blueprint_memory, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    outside = tmp_path.parent / "outside.md"
    outside.write_text("outside", encoding="utf-8")
    graph = product_blueprint_memory.open_graph()
    with pytest.raises(ValueError, match="source file must be inside the workspace"):
        product_blueprint_memory.snapshot_source_file(
            graph, {"path": str(outside), "title": None, "role": "extra_source"}
        )
    graph.close()


def test_main_returns_error_for_missing_product_blueprint(product_blueprint_memory, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["memory.py", "get"])
    assert product_blueprint_memory.main() == 1
    assert "Product Blueprint does not exist" in json.loads(capsys.readouterr().err)["error"]
