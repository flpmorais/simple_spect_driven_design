# Step 10: Edit Routing

## Goal

After all planning gates are complete, allow the user to edit planning artifacts by routing to the appropriate workflow.

## Rules

- Read this entire step before acting.
- This step is only allowed after every tracker row through implementation-readiness is `complete`.
- If any prior row is not `complete`, route back to the first incomplete gate without honoring edit requests.
- Run at most one edit/update workflow per user request.

## Routing

- Product brief edits: invoke `bmad-product-brief` in update mode with the existing product brief path.
- PRD edits: invoke `bmad-edit-prd` with `_bmad-output/planning-artifacts/prd.md`.
- Design-system edits: invoke `bmad-agent-ux-designer` with instructions to update `_bmad-output/design-system/MASTER.md` while preserving existing decisions unless explicitly changed.
- UX design edits: invoke `bmad-create-ux-design` with instructions to update `_bmad-output/planning-artifacts/ux-design-specification.md` from the PRD delta and design-system MASTER.md.
- Architecture edits: invoke `bmad-create-architecture` with instructions to continue/update `_bmad-output/planning-artifacts/architecture.md`.
- Epics and stories edits: invoke `bmad-create-epics-and-stories` with instructions to update `_bmad-output/planning-artifacts/epics.md` from the current PRD, UX, and architecture.
- Readiness re-check: invoke `bmad-check-implementation-readiness`.

## Instructions

1. Read `{tracker_file}`.
2. Verify all rows through implementation-readiness are `complete`.
3. If any row is not complete, update `currentGate` to that row and load the matching gate step.
4. If the user's request clearly names one artifact to edit, invoke the matching workflow from Routing.
5. If the user's request is ambiguous, ask one short question naming the available edit targets.
6. After the workflow returns, update `{tracker_file}` run log with the edited artifact and keep `currentGate: edit-routing`.

## Success Criteria

- Edits are allowed only after readiness completion and are routed to exactly one appropriate workflow.
