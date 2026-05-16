from __future__ import annotations

import json

import pytest

from .conftest import stdout_json, write_json


def idea(**overrides):
    data = {
        "title": "Idea",
        "concept": "Concept",
        "rationale": "Rationale",
        "hidden_assumption": "Assumption",
        "risk": "Risk",
        "domain": "business",
    }
    data.update(overrides)
    return data


def create_brainstorm(brainstorm_memory, args, capsys, **overrides):
    params = {
        "topic": "Topic",
        "goal": "Goal",
        "initial_context": "Context",
        "scope": "quick",
        "target_ideas": 20,
        "mode": "guided",
        "downstream_consumer": "consumer",
        "constraints_json": None,
        "techniques_json": None,
    }
    params.update(overrides)
    brainstorm_memory.cmd_create(args(**params))
    return stdout_json(capsys)["brainstorm_id"]


def test_decoded_brainstorm(brainstorm_memory):
    decoded = brainstorm_memory.decoded_brainstorm(
        {"constraints": '["c"]', "techniques": '[{"name": "t"}]', "topic": "T"}
    )
    assert decoded["constraints"] == ["c"]
    assert decoded["techniques"] == [{"name": "t"}]
    assert decoded["topic"] == "T"


def test_create_with_constraints_and_techniques(brainstorm_memory, tmp_path, args, capsys):
    constraints = write_json(tmp_path / "constraints.json", ["constraint"])
    techniques = write_json(tmp_path / "techniques.json", [{"name": "tech"}])
    brainstorm_id = create_brainstorm(
        brainstorm_memory,
        args,
        capsys,
        constraints_json=str(constraints),
        techniques_json=str(techniques),
    )

    brainstorm_memory.cmd_ideas(args(brainstorm_id=brainstorm_id))
    result = stdout_json(capsys)
    assert result["brainstorm"]["title"] == "Topic"
    assert result["brainstorm"]["constraints"] == ["constraint"]
    assert result["brainstorm"]["techniques"] == [{"name": "tech"}]
    assert result["ideas"] == []


def test_list_brainstorms_empty_and_populated(brainstorm_memory, args, capsys):
    brainstorm_memory.cmd_list(args())
    assert stdout_json(capsys) == {"status": "ok", "brainstorms": []}

    second_id = create_brainstorm(brainstorm_memory, args, capsys, topic="Second")
    first_id = create_brainstorm(brainstorm_memory, args, capsys, topic="First")

    brainstorm_memory.cmd_list(args())
    result = stdout_json(capsys)
    assert result["status"] == "ok"
    assert [item["topic"] for item in result["brainstorms"]] == ["First", "Second"]
    assert [item["title"] for item in result["brainstorms"]] == ["First", "Second"]
    assert {item["id"] for item in result["brainstorms"]} == {first_id, second_id}
    assert all("constraints" not in item for item in result["brainstorms"])
    assert all("techniques" not in item for item in result["brainstorms"])


def test_append_finish_and_get_ideas(brainstorm_memory, tmp_path, args, capsys):
    brainstorm_id = create_brainstorm(brainstorm_memory, args, capsys)
    ideas_path = write_json(
        tmp_path / "ideas.json",
        [
            idea(number=2, title="Second", technique="forced"),
            idea(number=1, title="First", technique="forced"),
        ],
    )
    brainstorm_memory.cmd_append_ideas(args(brainstorm_id=brainstorm_id, ideas_json=str(ideas_path)))
    appended = stdout_json(capsys)
    assert len(appended["idea_ids"]) == 2

    brainstorm_memory.cmd_finish(args(brainstorm_id=brainstorm_id, status="complete"))
    assert stdout_json(capsys)["brainstorm_status"] == "complete"

    brainstorm_memory.cmd_ideas(args(brainstorm_id=brainstorm_id))
    result = stdout_json(capsys)
    assert result["brainstorm"]["status"] == "complete"
    assert [item["number"] for item in result["ideas"]] == [1, 2]
    assert [item["title"] for item in result["ideas"]] == ["First", "Second"]


def test_delete_brainstorm_removes_root_ideas_and_relationships(brainstorm_memory, tmp_path, args, capsys):
    brainstorm_id = create_brainstorm(brainstorm_memory, args, capsys)
    ideas_path = write_json(tmp_path / "ideas.json", [idea(number=1), idea(number=2)])
    brainstorm_memory.cmd_append_ideas(args(brainstorm_id=brainstorm_id, ideas_json=str(ideas_path)))
    idea_ids = stdout_json(capsys)["idea_ids"]

    with pytest.raises(ValueError, match="Brainstorm does not exist"):
        brainstorm_memory.cmd_delete(args(brainstorm_id=idea_ids[0], confirm=idea_ids[0]))

    with pytest.raises(ValueError, match="Confirmation does not match brainstorm_id"):
        brainstorm_memory.cmd_delete(args(brainstorm_id=brainstorm_id, confirm="wrong"))

    brainstorm_memory.cmd_delete(args(brainstorm_id=brainstorm_id, confirm=brainstorm_id))
    deleted = stdout_json(capsys)
    assert deleted == {
        "status": "ok",
        "deleted": {
            "brainstorm_id": brainstorm_id,
            "brainstorms": 1,
            "ideas": 2,
            "nodes": 3,
        },
    }

    with pytest.raises(ValueError, match="does not exist"):
        brainstorm_memory.get_brainstorm(brainstorm_memory.open_graph(), brainstorm_id)

    graph = brainstorm_memory.open_graph()
    try:
        for idea_id in idea_ids:
            assert graph.get_node(idea_id) is None
        rows = graph.query("MATCH (n) RETURN n")
        assert rows == []
    finally:
        graph.close()


def test_auto_numbering_and_alias_fields(brainstorm_memory, tmp_path, args, capsys):
    brainstorm_id = create_brainstorm(brainstorm_memory, args, capsys)
    first = write_json(tmp_path / "first.json", [idea(title="First")])
    second = write_json(
        tmp_path / "second.json",
        [
            {
                "title": "Second",
                "concept": "Concept",
                "why_it_might_work": "Alias rationale",
                "hidden_assumption": "Assumption",
                "failure_mode_or_risk": "Alias risk",
                "domain": "user",
            }
        ],
    )

    brainstorm_memory.cmd_append_ideas(args(brainstorm_id=brainstorm_id, ideas_json=str(first)))
    capsys.readouterr()
    brainstorm_memory.cmd_append_ideas(args(brainstorm_id=brainstorm_id, ideas_json=str(second)))
    capsys.readouterr()
    brainstorm_memory.cmd_ideas(args(brainstorm_id=brainstorm_id))
    result = stdout_json(capsys)
    assert [item["number"] for item in result["ideas"]] == [1, 2]
    assert result["ideas"][1]["rationale"] == "Alias rationale"
    assert result["ideas"][1]["risk"] == "Alias risk"
    assert result["ideas"][1]["technique"] == "unknown"


def test_revise_idea_supersedes_previous_idea(brainstorm_memory, tmp_path, args, capsys):
    brainstorm_id = create_brainstorm(brainstorm_memory, args, capsys)
    original = write_json(tmp_path / "original.json", [idea(number=1, title="Original")])
    revised = write_json(
        tmp_path / "revised.json",
        idea(number=1, title="Revised", concept="Revised concept", technique="review"),
    )

    brainstorm_memory.cmd_append_ideas(args(brainstorm_id=brainstorm_id, ideas_json=str(original)))
    first_id = stdout_json(capsys)["idea_ids"][0]

    brainstorm_memory.cmd_revise_idea(
        args(brainstorm_id=brainstorm_id, idea_number=1, idea_json=str(revised))
    )
    revision = stdout_json(capsys)
    assert revision["status"] == "ok"
    assert revision["superseded_idea_id"] == first_id
    assert revision["revised_idea_id"] != first_id

    brainstorm_memory.cmd_ideas(args(brainstorm_id=brainstorm_id, include_superseded=False))
    latest = stdout_json(capsys)["ideas"]
    assert len(latest) == 1
    assert latest[0]["number"] == 1
    assert latest[0]["title"] == "Revised"
    assert latest[0]["revision"] == 2
    assert latest[0]["revision_of"] == first_id
    assert latest[0]["superseded"] is False

    brainstorm_memory.cmd_ideas(args(brainstorm_id=brainstorm_id, include_superseded=True))
    history = stdout_json(capsys)["ideas"]
    assert [item["title"] for item in history] == ["Original", "Revised"]
    assert history[0]["superseded"] is True
    assert history[1]["superseded"] is False


def test_revise_missing_and_inactive_brainstorm_errors(brainstorm_memory, tmp_path, args, capsys):
    brainstorm_id = create_brainstorm(brainstorm_memory, args, capsys)
    revised = write_json(tmp_path / "revised.json", idea(number=1))

    with pytest.raises(ValueError, match="Idea number does not exist"):
        brainstorm_memory.cmd_revise_idea(
            args(brainstorm_id=brainstorm_id, idea_number=1, idea_json=str(revised))
        )

    original = write_json(tmp_path / "original.json", [idea(number=1)])
    brainstorm_memory.cmd_append_ideas(args(brainstorm_id=brainstorm_id, ideas_json=str(original)))
    capsys.readouterr()
    brainstorm_memory.cmd_finish(args(brainstorm_id=brainstorm_id, status="complete"))
    capsys.readouterr()

    with pytest.raises(ValueError, match="not active"):
        brainstorm_memory.cmd_revise_idea(
            args(brainstorm_id=brainstorm_id, idea_number=1, idea_json=str(revised))
        )


@pytest.mark.parametrize(
    ("raw", "match"),
    [
        ({}, "non-empty array"),
        ([], "non-empty array"),
        (["x"], "must be an object"),
        ([idea(number=0)], "positive integer"),
        ([idea(number=1), idea(number=1)], "Duplicate idea number"),
        ([idea(title="")], "requires title"),
        ([idea(concept="")], "requires concept"),
        ([idea(rationale="")], "requires rationale"),
        ([idea(hidden_assumption="")], "requires hidden_assumption"),
        ([idea(risk="")], "requires risk"),
        ([idea(domain="")], "requires domain"),
    ],
)
def test_validate_ideas_failures(brainstorm_memory, raw, match):
    with pytest.raises(ValueError, match=match):
        brainstorm_memory.validate_ideas(raw, start_number=1)


def test_missing_and_inactive_brainstorm_errors(brainstorm_memory, tmp_path, args, capsys):
    with pytest.raises(ValueError, match="does not exist"):
        brainstorm_memory.get_brainstorm(brainstorm_memory.open_graph(), "missing")

    brainstorm_id = create_brainstorm(brainstorm_memory, args, capsys)
    brainstorm_memory.cmd_finish(args(brainstorm_id=brainstorm_id, status="complete_with_warnings"))
    capsys.readouterr()

    with pytest.raises(ValueError, match="not active"):
        brainstorm_memory.cmd_append_ideas(
            args(brainstorm_id=brainstorm_id, ideas_json=str(write_json(tmp_path / "ideas.json", [idea()])))
        )
    with pytest.raises(ValueError, match="not active"):
        brainstorm_memory.cmd_finish(args(brainstorm_id=brainstorm_id, status="complete"))


def test_duplicate_existing_idea_number_rejected(brainstorm_memory, tmp_path, args, capsys):
    brainstorm_id = create_brainstorm(brainstorm_memory, args, capsys)
    first = write_json(tmp_path / "first.json", [idea(number=1)])
    second = write_json(tmp_path / "second.json", [idea(number=1, title="Duplicate")])

    brainstorm_memory.cmd_append_ideas(args(brainstorm_id=brainstorm_id, ideas_json=str(first)))
    capsys.readouterr()
    with pytest.raises(ValueError, match="already exists"):
        brainstorm_memory.cmd_append_ideas(args(brainstorm_id=brainstorm_id, ideas_json=str(second)))


def test_main_returns_error_for_validation_failure(brainstorm_memory, monkeypatch, capsys):
    monkeypatch.setattr(
        "sys.argv",
        ["memory.py", "append-ideas", "--brainstorm-id", "missing", "--ideas-json", "missing.json"],
    )
    assert brainstorm_memory.main() == 1
    assert "Brainstorm does not exist" in json.loads(capsys.readouterr().err)["error"]
