from __future__ import annotations

import json
import re
import uuid

import pytest

from .conftest import stdout_json, write_json, write_text


def test_slug_normalizes_and_rejects_empty(kernel):
    assert kernel.slug(" Product Brief!! ") == "product-brief"
    assert kernel.slug("SQLite/GraphQLite") == "sqlite-graphqlite"

    with pytest.raises(ValueError, match="cannot be normalized"):
        kernel.slug(" !!! ")


def test_ids_and_timestamps(kernel):
    uuid.UUID(kernel.new_id())
    assert re.match(r"\d{4}-\d{2}-\d{2}T", kernel.now_iso())


def test_json_helpers(kernel):
    assert kernel.json_text({"b": 2, "a": 1}) == '{"a": 1, "b": 2}'
    assert kernel.maybe_json('["x"]') == ["x"]
    assert kernel.maybe_json("not json") == "not json"
    assert kernel.maybe_json({"x": 1}) == {"x": 1}


def test_file_readers(kernel, tmp_path):
    json_path = write_json(tmp_path / "data.json", {"ok": True})
    text_path = write_text(tmp_path / "data.txt", "hello")

    assert kernel.read_json_file(str(json_path)) == {"ok": True}
    assert kernel.read_text_file(str(text_path)) == "hello"
    assert kernel.read_text_file(None) is None

    with pytest.raises(ValueError, match="Expected JSON file"):
        kernel.read_json_file(str(tmp_path / "missing.json"))
    with pytest.raises(ValueError, match="Expected text file"):
        kernel.read_text_file(str(tmp_path / "missing.txt"))


def test_node_props(kernel):
    assert kernel.node_props(None) is None
    assert kernel.node_props({"properties": {"id": "x"}}) == {"id": "x"}


def test_output_and_fail(kernel, capsys):
    kernel.output({"b": 2, "a": 1})
    assert stdout_json(capsys) == {"a": 1, "b": 2}

    assert kernel.fail("bad", code="blocked") == 1
    captured = capsys.readouterr()
    assert json.loads(captured.err) == {"status": "blocked", "error": "bad"}


def test_open_graph_creates_database(kernel):
    graph = kernel.open_graph()
    try:
        graph.upsert_node("node:1", {"id": "node:1"}, label="TestNode")
        assert graph.get_node("node:1")["properties"]["id"] == "node:1"
    finally:
        graph.close()

    assert kernel.MEMORY_DIR.exists()
    assert kernel.DB_PATH.exists()
