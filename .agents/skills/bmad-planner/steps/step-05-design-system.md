# Step 5: Design-System Gate

## Goal

Ensure `_bmad-output/design-system/MASTER.md` is created or updated after PRD completion and before UX design.

## Rules

- Read this entire step before acting.
- If the tracker already marks design-system `complete`, do not inspect `MASTER.md`; route to UX design.
- This gate uses `bmad-agent-ux-designer` because there is no installed `UI UX PRO MAX` skill in this repository.
- Completion is owned by `{tracker_file}`, not by the design-system file frontmatter.
- If `MASTER.md` exists, preserve it and apply only PRD deltas: additions, explicit changes, and explicit removals.
- If `MASTER.md` does not exist, create it from the PRD.

## Instructions

1. Read `{tracker_file}`.
2. If the design-system row status is `complete`, trust the tracker and read fully and follow `./step-06-ux-design.md`.
3. Check whether `{design_system_file}` exists only because the tracker does not mark this gate complete.
4. Update `{tracker_file}`:
   - `currentGate: design-system`
   - `status: blocked-on-design-system`
   - `nextRequiredAction: Run bmad-agent-ux-designer to create or delta-update _bmad-output/design-system/MASTER.md from _bmad-output/planning-artifacts/prd.md, then mark the design-system tracker row complete.`
   - Artifact inventory design-system row status: `missing` if the file is absent, otherwise `needs-delta-update`.
   - Used files: `_bmad-output/planning-artifacts/prd.md` and existing `_bmad-output/design-system/MASTER.md` when present.
5. Invoke `bmad-agent-ux-designer` with these exact instructions:
   - Act as the UI UX PRO MAX designer.
   - Use `_bmad-output/planning-artifacts/prd.md` as the source of new, changed, or explicitly removed requirements.
   - If `_bmad-output/design-system/MASTER.md` exists, preserve the current design system and apply only the PRD delta; do not rewrite stable decisions.
   - If `_bmad-output/design-system/MASTER.md` does not exist, create it.
   - Write only `_bmad-output/design-system/MASTER.md`.
   - Make the file self-contained enough for later UX and frontend implementation agents.
6. After the designer skill returns, check that `{design_system_file}` exists.
7. If it exists, update `{tracker_file}`:
   - design-system row status: `complete`
   - generated file: `_bmad-output/design-system/MASTER.md`
   - `currentGate: ux-design`
   - `nextRequiredAction: Check the UX design tracker gate. If not complete, create or delta-update _bmad-output/planning-artifacts/ux-design-specification.md using the PRD and design-system MASTER.md.`
8. If the user asks to stop, STOP. Otherwise read fully and follow `./step-06-ux-design.md`.

## Success Criteria

- Tracker marks design-system complete and the planner continues to UX unless the user asks to stop.
