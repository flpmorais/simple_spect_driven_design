# Step 1: Ensure Planning Tracker

## Goal

Ensure `_bmad-output/planning-artifacts/planning-tracker.md` exists, then route directly to the current incomplete gate.

## Rules

- Read this entire step before acting.
- Only inspect and update `_bmad-output/planning-artifacts/planning-tracker.md` in this step, unless the tracker is missing and `{planning_artifacts}` must be created.
- Do not invoke child skills in this step.
- Do not inspect product brief, brainstorm, PRD, design-system, UX, architecture, epics, or readiness files here.
- If the tracker marks a gate complete, trust it and route past that gate without checking the filesystem.

## Instructions

1. Ensure `{planning_artifacts}` exists. If it does not exist, create it.
2. If `{tracker_file}` does not exist, create it using the template below.
3. Read `{tracker_file}` completely.
4. Determine the first gate whose Artifact Inventory status is not `complete`, in this order: product-brief, brainstorming, prd, design-system, ux-design, architecture, epics-and-stories, implementation-readiness.
5. Update frontmatter `currentGate` and `nextRequiredAction` to match that first incomplete gate. Preserve accurate artifact history and run log entries.
6. Route directly to the matching step:
   - `product-brief` -> `./step-02-product-brief.md`
   - `brainstorming` -> `./step-03-brainstorms.md`
   - `prd` -> `./step-04-prd.md`
   - `design-system` -> `./step-05-design-system.md`
   - `ux-design` -> `./step-06-ux-design.md`
   - `architecture` -> `./step-07-architecture.md`
   - `epics-and-stories` -> `./step-08-epics-and-stories.md`
   - `implementation-readiness` -> `./step-09-implementation-readiness.md`
7. If all gates are complete, set `currentGate: edit-routing`, set `status: complete-through-readiness`, and read fully and follow `./step-10-edit-routing.md`.

## Tracker Template

```markdown
---
workflow: bmad-planner
currentGate: product-brief
status: in-progress
updated: '{date}'
nextRequiredAction: 'Check for a complete product brief at _bmad-output/product-brief-{project_name}.md because the tracker has not marked product-brief complete.'
---

# BMad Planning Tracker

This file is the source of truth for BMad planning progress. The planner trusts this file first. Do not re-check files for gates marked `complete`; only inspect files for the first gate not marked `complete`.

## Gate Order

1. product-brief
2. brainstorming
3. prd
4. design-system
5. ux-design
6. architecture
7. epics-and-stories
8. implementation-readiness
9. edit-routing

## Current Required Action

Check for a complete product brief at `_bmad-output/product-brief-{project_name}.md` because the tracker has not marked product-brief complete.

## Artifact Inventory

| Gate | Status | Generated Files | Used Files | Notes |
|---|---|---|---|---|
| product-brief | pending | none | none | Required before any other planning gate. |
| brainstorming | pending | none | none | Requires at least one complete session and no incomplete sessions. |
| prd | pending | none | none | Requires `_bmad-output/planning-artifacts/prd.md` with `step-12-complete`. |
| design-system | pending | none | none | Requires `_bmad-output/design-system/MASTER.md`; completion is tracked only here. |
| ux-design | pending | none | none | Requires `_bmad-output/planning-artifacts/ux-design-specification.md`; must follow design-system MASTER.md and PRD delta. |
| architecture | pending | none | none | Requires `_bmad-output/planning-artifacts/architecture.md` with complete status. |
| epics-and-stories | pending | none | none | Requires `_bmad-output/planning-artifacts/epics.md`; completion is tracked here after workflow completes. |
| implementation-readiness | pending | none | none | Requires a readiness report; completion is tracked here after workflow completes. |

## Completion Rules

- Product brief complete: frontmatter `status: "complete"` in `_bmad-output/product-brief-{project_name}.md`.
- Brainstorm complete: every `_bmad-output/brainstorming/*.md` has `workflow_completed: true`, `session_active: false`, and `stepsCompleted: [1, 2, 3, 4]`; at least one complete brainstorm exists.
- PRD complete: `_bmad-output/planning-artifacts/prd.md` frontmatter `stepsCompleted` contains `step-12-complete`.
- Design system complete: tracker row `design-system` is `complete`; do not infer completion from a non-BMad file marker.
- UX design complete: tracker row `ux-design` is `complete`; when tracker is not complete, file completion means frontmatter `stepsCompleted` contains `step-14-complete` or `lastStep: 14`.
- Architecture complete: `_bmad-output/planning-artifacts/architecture.md` frontmatter has `status: complete`, `lastStep: 8`, and `stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]`.
- Epics and stories complete: tracker row `epics-and-stories` is `complete` after `bmad-create-epics-and-stories` finishes.
- Implementation readiness complete: tracker row `implementation-readiness` is `complete` after `bmad-check-implementation-readiness` finishes.

## Run Log

- {date}: Created planning tracker. Next gate: product-brief.
```

## Success Criteria

- Tracker exists at `{tracker_file}`.
- Tracker includes gate order, artifact inventory, completion rules, run log, and exact next required action.
- The next step is `step-02-product-brief.md`.
