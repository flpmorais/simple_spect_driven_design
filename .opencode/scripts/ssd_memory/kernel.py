"""Shared SSD memory kernel helpers backed by GraphQLite."""

from __future__ import annotations

import json
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    import graphqlite
except ModuleNotFoundError as exc:  # pragma: no cover - dependency guard
    raise SystemExit(
        "graphqlite is required. Install with: python3 -m pip install --user graphqlite"
    ) from exc


MEMORY_DIR = Path(".opencode/shared/memory")
DB_PATH = MEMORY_DIR / "ssd-memory.db"
GRAPH_NAMESPACE = "ssd"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def new_id() -> str:
    return str(uuid.uuid4())


def slug(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.strip().lower())
    normalized = normalized.strip("-")
    if not normalized:
        raise ValueError("Value cannot be normalized to an id slug")
    return normalized


def output(data: dict[str, Any]) -> None:
    print(json.dumps(data, indent=2, sort_keys=True))


def fail(message: str, *, code: str = "error") -> int:
    print(json.dumps({"status": code, "error": message}, indent=2), file=sys.stderr)
    return 1


def open_graph() -> Any:
    MEMORY_DIR.mkdir(parents=True, exist_ok=True)
    return graphqlite.Graph(DB_PATH, namespace=GRAPH_NAMESPACE)


def node_props(node: dict[str, Any] | None) -> dict[str, Any] | None:
    if node is None:
        return None
    return node.get("properties", {})


def read_json_file(path_text: str) -> Any:
    path = Path(path_text)
    if not path.is_file():
        raise ValueError(f"Expected JSON file: {path_text}")
    return json.loads(path.read_text(encoding="utf-8"))


def read_text_file(path_text: str | None) -> str | None:
    if not path_text:
        return None
    path = Path(path_text)
    if not path.is_file():
        raise ValueError(f"Expected text file: {path_text}")
    return path.read_text(encoding="utf-8")


def json_text(value: Any) -> str:
    return json.dumps(value, ensure_ascii=True, sort_keys=True)


def maybe_json(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    try:
        return json.loads(value)
    except json.JSONDecodeError:
        return value
