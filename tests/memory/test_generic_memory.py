from __future__ import annotations

import json

import pytest

from .conftest import assert_uuid, stdout_json, write_json


def valid_sections():
    return [
        {"section_key": "Problem", "heading": "Problem", "canonical_text": "Problem text"},
        {
            "section_key": "Audience",
            "heading": "Audience",
            "canonical_text": "Audience text",
            "position": 5,
        },
    ]


def test_validate_sections_success(generic_memory):
    sections = generic_memory.validate_sections(valid_sections())
    assert sections == [
        {
            "section_key": "problem",
            "heading": "Problem",
            "canonical_text": "Problem text",
            "position": 1,
        },
        {
            "section_key": "audience",
            "heading": "Audience",
            "canonical_text": "Audience text",
            "position": 5,
        },
    ]


@pytest.mark.parametrize(
    ("raw", "match"),
    [
        ({}, "non-empty array"),
        ([], "non-empty array"),
        (["x"], "must be an object"),
        ([{"heading": "H", "canonical_text": "T"}], "requires section_key"),
        ([{"section_key": "k", "canonical_text": "T"}], "requires heading"),
        ([{"section_key": "k", "heading": "H"}], "requires canonical_text"),
        (
            [
                {"section_key": "A!", "heading": "A", "canonical_text": "T"},
                {"section_key": "A", "heading": "A", "canonical_text": "T"},
            ],
            "Duplicate section_key",
        ),
    ],
)
def test_validate_sections_failures(generic_memory, raw, match):
    with pytest.raises(ValueError, match=match):
        generic_memory.validate_sections(raw)


def test_artifact_create_get_context_update_and_list(generic_memory, tmp_path, args, capsys):
    sections_path = write_json(tmp_path / "sections.json", valid_sections())

    generic_memory.cmd_init(args())
    assert stdout_json(capsys)["status"] == "ok"

    generic_memory.cmd_artifact_create(
        args(
            kind="product_brief",
            title="Product Brief",
            sections_json=str(sections_path),
            change_summary="Initial",
        )
    )
    created = stdout_json(capsys)
    assert created["status"] == "ok"
    assert_uuid(created["artifact_id"])

    generic_memory.cmd_artifact_get(args(kind="product_brief"))
    current = stdout_json(capsys)
    assert [section["section_key"] for section in current["sections"]] == ["problem", "audience"]

    sections_v2 = write_json(
        tmp_path / "sections-v2.json",
        [{"section_key": "Problem", "heading": "Problem", "canonical_text": "Updated"}],
    )
    generic_memory.cmd_artifact_update(
        args(
            kind="product_brief",
            sections_json=str(sections_v2),
            change_summary="Update",
        )
    )
    updated = stdout_json(capsys)
    assert updated["artifact_id"] == created["artifact_id"]

    generic_memory.cmd_graph_query(args(cypher="MATCH (n) RETURN n", unsafe_write=False))
    graph_nodes = stdout_json(capsys)["rows"]
    assert graph_nodes
    assert all(row["n"]["properties"].get("title") for row in graph_nodes)

    generic_memory.cmd_artifact_get(args(kind="product_brief"))
    current = stdout_json(capsys)
    assert [section["canonical_text"] for section in current["sections"]] == ["Updated"]

    generic_memory.cmd_graph_query(args(cypher="MATCH (n) RETURN n", unsafe_write=False))
    assert len(stdout_json(capsys)["rows"]) == 2

    generic_memory.cmd_artifact_list(args())
    listed = stdout_json(capsys)
    assert [artifact["kind"] for artifact in listed["artifacts"]] == ["product-brief"]


def test_artifact_error_paths(generic_memory, tmp_path, args):
    sections_path = write_json(tmp_path / "sections.json", valid_sections())
    create_args = args(
        kind="thing",
        title="Thing",
        sections_json=str(sections_path),
        change_summary="Initial",
    )
    generic_memory.cmd_artifact_create(create_args)

    with pytest.raises(ValueError, match="already exists"):
        generic_memory.cmd_artifact_create(create_args)
    with pytest.raises(ValueError, match="does not exist"):
        generic_memory.cmd_artifact_get(args(kind="missing"))
    with pytest.raises(ValueError, match="does not exist"):
        generic_memory.cmd_artifact_update(
            args(
                kind="missing",
                sections_json=str(sections_path),
                change_summary="Update",
            )
        )


def test_graph_query_read_and_write_guard(generic_memory, args, capsys):
    generic_memory.cmd_init(args())
    capsys.readouterr()

    generic_memory.cmd_graph_query(args(cypher="MATCH (n) RETURN n LIMIT 1", unsafe_write=False))
    assert stdout_json(capsys) == {"status": "ok", "rows": []}

    with pytest.raises(ValueError, match="read-only"):
        generic_memory.cmd_graph_query(args(cypher="CREATE (n:Thing)", unsafe_write=False))


def test_main_returns_error_for_validation_failure(generic_memory, monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        [
            "memory.py",
            "artifact",
            "create",
            "--kind",
            "x",
            "--title",
            "X",
            "--sections-json",
            "missing.json",
            "--change-summary",
            "Initial",
        ],
    )
    assert generic_memory.main() == 1
    assert "Expected JSON file" in json.loads(capsys.readouterr().err)["error"]
