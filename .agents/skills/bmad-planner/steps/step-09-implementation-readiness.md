# Step 9: Implementation Readiness Gate

## Goal

Ensure implementation readiness has been checked after epics and stories are created.

## Rules

- Read this entire step before acting.
- If the tracker already marks implementation-readiness `complete`, do not inspect readiness reports; route to edit routing.
- The readiness skill is `bmad-check-implementation-readiness`.
- Completion is owned by `{tracker_file}` after the workflow completes.

## Instructions

1. Read `{tracker_file}`.
2. If the implementation-readiness row status is `complete`, trust the tracker and read fully and follow `./step-10-edit-routing.md`.
3. Update `{tracker_file}`:
   - `currentGate: implementation-readiness`
   - `status: blocked-on-implementation-readiness`
   - `nextRequiredAction: Run bmad-check-implementation-readiness, then mark implementation-readiness complete.`
   - Artifact inventory implementation-readiness row status: `not-run`.
   - Used files: PRD, UX design specification, architecture, and epics.md.
4. Invoke `bmad-check-implementation-readiness`.
5. After the skill returns, update `{tracker_file}`:
   - implementation-readiness row status: `complete`
   - generated files: latest `_bmad-output/planning-artifacts/implementation-readiness-report-*.md` if known
   - `currentGate: edit-routing`
   - `status: complete-through-readiness`
   - `nextRequiredAction: Planning gates are complete. User may now request edits to product brief, PRD, design system, UX design, architecture, epics/stories, or readiness artifacts.`
6. Read fully and follow `./step-10-edit-routing.md`.

## Success Criteria

- Tracker marks implementation-readiness complete and the planner routes to edit mode.
