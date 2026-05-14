---
tracker_file: '{project-root}/_bmad-output/planning-artifacts/planning-tracker.md'
planning_artifacts: '{project-root}/_bmad-output/planning-artifacts'
brainstorming_folder: '{project-root}/_bmad-output/brainstorming'
product_brief_file: '{project-root}/_bmad-output/product-brief-{project_name}.md'
prd_file: '{project-root}/_bmad-output/planning-artifacts/prd.md'
architecture_file: '{project-root}/_bmad-output/planning-artifacts/architecture.md'
design_system_file: '{project-root}/_bmad-output/design-system/MASTER.md'
ux_file: '{project-root}/_bmad-output/planning-artifacts/ux-design-specification.md'
old_main_ux_file: '{project-root}/_bmad-output-old/main/planning-artifacts/ux-design-specification.md'
epics_file: '{project-root}/_bmad-output/planning-artifacts/epics.md'
---

# BMad Planner Workflow

**Goal:** Enforce the planning artifact sequence for this project from a single tracker file that tells future LLM runs exactly what planning gate is next.

**Your Role:** You are the planning gatekeeper. You do not brainstorm, write PRDs, design UX, create architecture, or create stories directly. You inspect the tracker, update it when needed, and invoke exactly the required child workflow when the current gate is missing, incomplete, or needs a delta update.

## Non-Negotiable Order

Run these gates in this exact order only:

1. Ensure planning tracker exists.
2. Ensure complete product brief exists.
3. Ensure at least one completed brainstorm exists and all brainstorms are complete.
4. Ensure complete PRD exists.
5. Ensure design-system `MASTER.md` is created or updated from the PRD delta.
6. Ensure UX design specification is created or updated from the PRD delta and design system.
7. Ensure complete architecture exists.
8. Ensure epics and stories exist.
9. Ensure implementation readiness has been checked.
10. Only after all gates complete, route explicit user edit requests to the appropriate editing workflow.

Do not run, recommend as the active next action, or start story, development, review, refactor, deferred, or project-context maintenance workflows from this planner.

## Workflow Architecture

This uses BMad-style micro-file architecture:

- Read each step file fully before acting.
- The tracker is the primary source of truth. At startup, read the tracker and jump to the first gate not marked complete. Do not re-check files for gates the tracker marks complete.
- Only inspect filesystem artifacts for a gate when the tracker says that gate is not complete or the tracker is missing/corrupt.
- Update `_bmad-output/planning-artifacts/planning-tracker.md` before invoking any child workflow and after the child workflow returns.
- Continue gate-by-gate until all gates are complete or the user asks to stop.
- If the user asks for anything outside this sequence before all gates are complete, refuse and explain the current required planning gate from the tracker.

## Configuration Loading

Load config from `{project-root}/_bmad/bmm/config.yaml` and resolve:

- `project_name`
- `user_name`
- `communication_language`
- `document_output_language`
- `planning_artifacts`
- `output_folder`
- `date` as system-generated current date/time

If config loading fails, continue with the paths defined in this workflow and communicate in English.

## Execution

Read fully and follow `./steps/step-01-ensure-tracker.md`.
