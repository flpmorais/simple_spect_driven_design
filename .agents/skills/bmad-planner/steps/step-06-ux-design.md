# Step 6: UX Design Gate

## Goal

Ensure `_bmad-output/planning-artifacts/ux-design-specification.md` is created or updated after the design system gate.

## Rules

- Read this entire step before acting.
- If the tracker already marks UX design `complete`, do not inspect the UX file; route to architecture.
- The UX workflow skill is `bmad-create-ux-design`.
- The UX workflow must use `_bmad-output/planning-artifacts/prd.md` and `_bmad-output/design-system/MASTER.md` as inputs.
- If the current UX file is missing, first try to copy `_bmad-output-old/main/planning-artifacts/ux-design-specification.md` to `_bmad-output/planning-artifacts/ux-design-specification.md`.
- A copied old UX file is a baseline only; still run `bmad-create-ux-design` afterward to update it against the current PRD delta and design-system MASTER.md.
- If the UX file already exists and is complete while the tracker is not complete, run the UX skill to delta-update the document rather than trusting the file.

## File Completion Check

When the tracker does not mark UX complete, the UX file is complete only when `{ux_file}` exists and frontmatter contains `step-14-complete` in `stepsCompleted` or `lastStep: 14`.

## Instructions

1. Read `{tracker_file}`.
2. If the ux-design row status is `complete`, trust the tracker and read fully and follow `./step-07-architecture.md`.
3. Inspect `{ux_file}` only because the tracker does not mark this gate complete.
4. If `{ux_file}` is missing:
   - Check `{old_main_ux_file}`.
   - If `{old_main_ux_file}` exists, copy it to `{ux_file}` and update `{tracker_file}` with artifact inventory status `copied-from-old-main-needs-delta-update`.
   - If `{old_main_ux_file}` does not exist, update `{tracker_file}` with artifact inventory status `missing`.
5. If the UX file is missing after the old-main fallback check:
   - Update `{tracker_file}` with `currentGate: ux-design`, `status: blocked-on-ux-design`, and artifact inventory status `missing`.
   - Invoke `bmad-create-ux-design` with `_bmad-output/planning-artifacts/prd.md` and `_bmad-output/design-system/MASTER.md` as required inputs to create the UX document from scratch.
6. If the UX file exists but is incomplete:
   - Update `{tracker_file}` with `currentGate: ux-design`, `status: blocked-on-ux-design`, and artifact inventory status `incomplete`.
   - Invoke `bmad-create-ux-design` with `_bmad-output/planning-artifacts/prd.md` and `_bmad-output/design-system/MASTER.md` as required inputs to complete the UX document.
7. If the UX file exists and is complete but the tracker is not complete:
   - Update `{tracker_file}` with artifact inventory status `needs-delta-update`.
   - Invoke `bmad-create-ux-design` with these instructions: preserve the existing UX design specification, follow `_bmad-output/design-system/MASTER.md`, and apply only the PRD delta from `_bmad-output/planning-artifacts/prd.md`; add new UX requirements, change only explicitly changed UX decisions, and remove only explicitly removed UX requirements.
   - If the file was copied from `{old_main_ux_file}`, treat it as an existing complete baseline and apply the same delta-update instruction.
8. After the UX skill returns, re-check `{ux_file}` and update `{tracker_file}`:
   - ux-design row status: `complete` if the workflow completed or the file now has UX completion markers.
   - generated file: `_bmad-output/planning-artifacts/ux-design-specification.md`
   - used files: `_bmad-output/planning-artifacts/prd.md`, `_bmad-output/design-system/MASTER.md`, and `_bmad-output-old/main/planning-artifacts/ux-design-specification.md` if copied
   - `currentGate: architecture`
   - `nextRequiredAction: Check architecture tracker gate. If not complete, check _bmad-output/planning-artifacts/architecture.md and run bmad-create-architecture if missing or incomplete.`
9. If the user asks to stop, STOP. Otherwise read fully and follow `./step-07-architecture.md`.

## Success Criteria

- Tracker marks UX design complete and the planner continues to architecture unless the user asks to stop.
