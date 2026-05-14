---
workflow: bmad-deferred
id: DW-0048
status: done
source: Deferred from: code review of 1-1-brainstorm-runtime-foundation (2026-05-09)
createdAt: 2026-05-12-1505
updatedAt: 2026-05-12-1626
---

# Deferred Work Plan: DW-0048 Timing-unsafe Agent Key Comparison

## Raw Item

Timing-unsafe key comparison in `verify_agent_key` — uses `!=` instead of `hmac.compare_digest`. Low risk for internal-only service behind compose networking. [agent/main.py:11]

## Understanding

The agent service protects internal endpoints with an `X-Agent-Key` header. Current comparison uses normal string inequality, which is not constant-time. The service is internal-only, but replacing the comparison with `hmac.compare_digest` is a small security hardening change.

## Decision

Approved plan-work. Use constant-time comparison for agent key verification.

## Plan

### Tasks

#### 1. Harden `verify_agent_key` comparison

- Objective: Compare provided and configured agent keys with `hmac.compare_digest` while preserving current auth behavior.
- Likely files / areas:
  - `agent/main.py`
  - `agent/tests/test_agent_key.py`
- Subtasks:
  - Import `hmac` in `agent/main.py`.
  - Replace `key != settings.AGENT_KEY` with a safe `hmac.compare_digest` check.
  - Preserve rejection when the header is missing or empty.
  - Keep status code and error detail unchanged.
- Tests to update/add:
  - Run existing agent key tests.
  - Add a focused assertion only if existing tests do not cover valid/invalid key behavior.
- Validation:
  - `pytest agent/tests/test_agent_key.py`
  - Run related agent tests if imports or startup behavior change.
- Risks / notes:
  - Ensure both compared values are strings/bytes acceptable to `compare_digest`.

## Execution Record

- Updated `agent/main.py` to compare the provided `X-Agent-Key` and configured `AGENT_KEY` with `hmac.compare_digest`, preserving missing/empty key rejection and existing 401 response behavior.
- Existing valid, invalid, missing, empty, and startup agent key tests already covered behavior; no additional behavioral test was required.
- Files changed: `agent/main.py`, `_bmad-output/implementation-artifacts/deferred-work-tracker.md`, `_bmad-output/implementation-artifacts/deferred/deferred-DW-0048-timing-unsafe-agent-key-comparison.md`.
- Validation: `pytest agent/tests/test_agent_key.py` (5 passed); `pytest agent/tests` (106 passed).
- Commit: `2de160a` (`Complete deferred work DW-0048`); push result: pushed to `origin/1_datapipeline`.
