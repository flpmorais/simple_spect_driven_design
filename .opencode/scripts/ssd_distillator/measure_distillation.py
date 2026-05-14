#!/usr/bin/env python3
# /// script
# /// requires-python = ">=3.10"
# /// dependencies = []
# ///
"""Measure SSD distillation token estimates and compression ratio.

This script is intentionally narrow: it accepts explicit source files and one
explicit distillate file, estimates tokens from file size, and prints JSON to
stdout. It does not discover files, expand globs, choose routing, or write files.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


CHARS_PER_TOKEN = 4


def file_metrics(path_text: str) -> dict:
    path = Path(path_text)
    if not path.exists():
        raise ValueError(f"File does not exist: {path_text}")
    if not path.is_file():
        raise ValueError(f"Expected an explicit file path, got non-file: {path_text}")

    size_bytes = path.stat().st_size
    return {
        "path": path_text,
        "size_bytes": size_bytes,
        "estimated_tokens": size_bytes // CHARS_PER_TOKEN,
    }


def ratio_text(source_tokens: int, distillate_tokens: int) -> str:
    if distillate_tokens <= 0:
        return "unavailable"
    return f"{source_tokens / distillate_tokens:.2f}:1"


def measure(source_paths: list[str], distillate_path: str) -> dict:
    sources = [file_metrics(source_path) for source_path in source_paths]
    distillate = file_metrics(distillate_path)

    source_total_tokens = sum(source["estimated_tokens"] for source in sources)
    distillate_total_tokens = distillate["estimated_tokens"]

    return {
        "status": "ok",
        "source_total_tokens": source_total_tokens,
        "distillate_total_tokens": distillate_total_tokens,
        "compression_ratio": ratio_text(source_total_tokens, distillate_total_tokens),
        "sources": sources,
        "distillate": distillate,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        action="append",
        required=True,
        help="Explicit source file path. Repeat for multiple sources.",
    )
    parser.add_argument(
        "--distillate",
        required=True,
        help="Explicit final distillate file path.",
    )
    args = parser.parse_args()

    try:
        result = measure(args.source, args.distillate)
    except ValueError as exc:
        print(json.dumps({"status": "error", "error": str(exc)}, indent=2), file=sys.stderr)
        return 1

    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
