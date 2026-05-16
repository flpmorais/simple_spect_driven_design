from __future__ import annotations

import importlib
import json
import sys
import uuid
from pathlib import Path
from types import SimpleNamespace

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_ROOT = REPO_ROOT / ".opencode" / "scripts"


@pytest.fixture(autouse=True)
def scripts_on_path():
    path = str(SCRIPTS_ROOT)
    if path not in sys.path:
        sys.path.insert(0, path)


@pytest.fixture
def kernel(tmp_path, monkeypatch):
    module = importlib.import_module("ssd_memory.kernel")
    monkeypatch.setattr(module, "MEMORY_DIR", tmp_path / "memory")
    monkeypatch.setattr(module, "DB_PATH", tmp_path / "memory" / "ssd-memory.db")
    return module


@pytest.fixture
def generic_memory(kernel):
    return importlib.import_module("ssd_memory.memory")


@pytest.fixture
def brainstorm_memory(kernel):
    return importlib.import_module("ssd_brainstorming.memory")


@pytest.fixture
def product_brief_memory(kernel):
    return importlib.import_module("ssd_product_brief.memory")


@pytest.fixture
def product_blueprint_memory(kernel):
    return importlib.import_module("ssd_product_blueprint.memory")


@pytest.fixture
def architecture_blueprint_memory(kernel):
    return importlib.import_module("ssd_architecture_blueprint.memory")


@pytest.fixture
def project_setup_memory(kernel):
    return importlib.import_module("ssd_project_setup.memory")


@pytest.fixture
def args():
    def build(**kwargs):
        return SimpleNamespace(**kwargs)

    return build


def write_json(path: Path, data) -> Path:
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def write_text(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def stdout_json(capsys):
    captured = capsys.readouterr()
    return json.loads(captured.out)


def assert_uuid(value: str) -> None:
    uuid.UUID(value)
