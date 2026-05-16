from __future__ import annotations

import json

from .conftest import stdout_json


def create_artifact(project_setup_memory, artifact_id: str, kind: str, title: str) -> None:
    graph = project_setup_memory.open_graph()
    try:
        graph.upsert_node(
            artifact_id,
            {
                "id": artifact_id,
                "kind": kind,
                "title": title,
                "status": "accepted",
            },
            label="Artifact",
        )
        graph.reload_graph()
    finally:
        graph.close()


def test_status_reports_product_brief_as_required_first(project_setup_memory, args, capsys):
    project_setup_memory.cmd_status(args(scope="auto"))
    result = stdout_json(capsys)

    assert result["status"] == "incomplete"
    assert result["scope"] == {
        "scope_id": "root",
        "scope_type": "project",
        "name": "root",
    }
    assert result["available_next_steps"] == [
        {
            "artifact_kind": "product-brief",
            "skill": "ssd-product-brief-create",
            "reason": "Product Brief is missing and all prerequisites are complete.",
        }
    ]
    assert result["must_do"] == result["available_next_steps"]

    brief = result["artifacts"][0]
    blueprint = result["artifacts"][1]
    architecture = result["artifacts"][2]
    assert brief["state"] == "available"
    assert brief["complete"] is False
    assert blueprint["state"] == "blocked"
    assert blueprint["blocked_by"] == ["product-brief"]
    assert architecture["state"] == "blocked"
    assert architecture["blocked_by"] == ["product-blueprint"]


def test_status_reports_product_blueprint_after_brief(project_setup_memory, args, capsys):
    create_artifact(project_setup_memory, "brief-1", "product-brief", "Product Brief")

    project_setup_memory.cmd_status(args(scope="auto"))
    result = stdout_json(capsys)

    assert result["status"] == "incomplete"
    assert result["available_next_steps"] == [
        {
            "artifact_kind": "product-blueprint",
            "skill": "ssd-product-blueprint-create",
            "reason": "Product Blueprint is missing and all prerequisites are complete.",
        }
    ]
    assert result["must_do"] == result["available_next_steps"]
    assert result["artifacts"][0]["complete"] is True
    assert result["artifacts"][0]["artifact_id"] == "brief-1"
    assert result["artifacts"][1]["state"] == "available"


def test_status_reports_architecture_blueprint_after_product_blueprint(project_setup_memory, args, capsys):
    create_artifact(project_setup_memory, "brief-1", "product-brief", "Product Brief")
    create_artifact(project_setup_memory, "blueprint-1", "product-blueprint", "Product Blueprint")

    project_setup_memory.cmd_status(args(scope="auto"))
    result = stdout_json(capsys)

    assert result["status"] == "incomplete"
    assert result["available_next_steps"] == [
        {
            "artifact_kind": "architecture-blueprint",
            "skill": "ssd-architecture-blueprint-create",
            "reason": "Architecture Blueprint is missing and all prerequisites are complete.",
        }
    ]
    assert result["must_do"] == result["available_next_steps"]
    assert result["artifacts"][2]["state"] == "available"


def test_status_reports_complete_when_setup_artifacts_exist(project_setup_memory, args, capsys):
    create_artifact(project_setup_memory, "brief-1", "product-brief", "Product Brief")
    create_artifact(project_setup_memory, "blueprint-1", "product-blueprint", "Product Blueprint")
    create_artifact(project_setup_memory, "architecture-1", "architecture-blueprint", "Architecture Blueprint")

    project_setup_memory.cmd_status(args(scope="auto"))
    result = stdout_json(capsys)

    assert result["status"] == "complete"
    assert result["available_next_steps"] == []
    assert result["blocked_steps"] == []
    assert result["must_do"] == []
    assert [artifact["complete"] for artifact in result["artifacts"]] == [True, True, True]
    assert result["all_artifacts"] == [
        {
            "artifact_id": "architecture-1",
            "kind": "architecture-blueprint",
            "title": "Architecture Blueprint",
            "scope_id": "root",
        },
        {
            "artifact_id": "blueprint-1",
            "kind": "product-blueprint",
            "title": "Product Blueprint",
            "scope_id": "root",
        },
        {
            "artifact_id": "brief-1",
            "kind": "product-brief",
            "title": "Product Brief",
            "scope_id": "root",
        },
    ]


def test_status_blocks_on_duplicate_setup_artifacts(project_setup_memory, args, capsys):
    create_artifact(project_setup_memory, "brief-1", "product-brief", "Product Brief")
    create_artifact(project_setup_memory, "brief-2", "product-brief", "Product Brief")

    project_setup_memory.cmd_status(args(scope="auto"))
    result = stdout_json(capsys)

    assert result["status"] == "blocked"
    assert result["available_next_steps"] == []
    assert result["must_do"] == []
    assert result["blocked_reason"] == "Multiple Artifacts exist for kind: product-brief"


def test_main_returns_status(project_setup_memory, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["memory.py", "status"])

    assert project_setup_memory.main() == 0
    assert json.loads(capsys.readouterr().out)["status"] == "incomplete"
