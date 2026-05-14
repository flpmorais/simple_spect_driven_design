# Step 4: PRD Gate

## Goal

Ensure a complete PRD exists before architecture work can proceed.

## Rules

- Read this entire step before acting.
- Refuse architecture work until the PRD gate passes.
- If the tracker already marks PRD `complete`, do not inspect the PRD file; route to design-system.
- The PRD file must be `{prd_file}`.
- The PRD creation skill is `bmad-create-prd`.

## Completion Check

The PRD is complete only when:

- `{prd_file}` exists and is readable.
- Its frontmatter `stepsCompleted` contains `step-12-complete`.

## Instructions

1. Read `{tracker_file}`.
2. If the PRD row status is `complete`, trust the tracker and read fully and follow `./step-05-design-system.md`.
3. Inspect `{prd_file}` only because the tracker does not mark this gate complete.
4. If the file is missing or `stepsCompleted` does not contain `step-12-complete`:
   - Update `{tracker_file}`:
     - `currentGate: prd`
     - `status: blocked-on-prd`
     - `nextRequiredAction: Run bmad-create-prd with the user to create or complete _bmad-output/planning-artifacts/prd.md, then stop. Do not run architecture until the PRD is complete.`
     - Artifact inventory PRD row status: `missing` or `incomplete`.
     - Used files: product brief and completed brainstorm files already found.
     - Append a run-log entry with the reason.
   - Tell the user the planner refuses architecture until PRD is complete.
   - Invoke the `bmad-create-prd` skill.
   - After `bmad-create-prd` completes, re-check `{prd_file}` and update `{tracker_file}`.
   - If the user asks to stop, STOP. Otherwise continue to `./step-05-design-system.md`.
5. If the PRD is complete:
   - Update `{tracker_file}`:
     - PRD row status: `complete`
     - generated file: `_bmad-output/planning-artifacts/prd.md`
     - used files: product brief and completed brainstorms
     - `currentGate: design-system`
     - `nextRequiredAction: Check the design-system tracker gate. If not complete, create or update _bmad-output/design-system/MASTER.md from the PRD delta using bmad-agent-ux-designer.`
   - Read fully and follow `./step-05-design-system.md`.

## Success Criteria

- Complete PRD exists and tracker advances to `design-system`, then the planner continues unless the user asks to stop.
