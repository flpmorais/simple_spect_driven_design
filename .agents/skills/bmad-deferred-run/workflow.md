---
tracker_file: '{project-root}/_bmad-output/implementation-artifacts/deferred-work-tracker.md'
deferred_artifacts_dir: '{project-root}/_bmad-output/implementation-artifacts/deferred'
project_context_file: '{project-root}/_bmad-output/project-context.md'
---

# Deferred Work Execution Workflow

**Goal:** Execute one approved deferred work plan safely, update tests, run validations until passing, then commit and push.

**Your Role:** You are the deferred work execution agent. You implement only approved deferred plans, preserve project-context rules, keep tests aligned, and commit/push completed fixes.

## Non-Negotiable Rules

- Only execute per-item artifacts under `_bmad-output/implementation-artifacts/deferred/deferred-*.md`.
- The per-item artifact must have frontmatter `workflow: bmad-deferred` and `status: planned` or `status: in-progress`.
- Do not execute raw bullets from `deferred-work.md` directly.
- Read `_bmad-output/project-context.md` before coding. If missing or unreadable, fail gracefully.
- If implementation must materially deviate from the approved deferred plan, STOP and ask the user.
- Update/add/remove tests as needed.
- Run required validations until passing.
- When complete, commit all deferred-work-related changes and push to remote. Never force push.

## Execution

Read fully and follow `./steps/step-01-select-plan.md`.
