# Step 7: Architecture Gate

## Goal

Ensure a complete architecture document exists after PRD, design system, and UX design completion.

## Rules

- Read this entire step before acting.
- If the tracker already marks architecture `complete`, do not inspect the architecture file; route to epics and stories.
- The architecture file must be `{architecture_file}`.
- The architecture creation skill is `bmad-create-architecture`.

## Completion Check

The architecture is complete only when `{architecture_file}` exists and its frontmatter contains all of:

- `status: complete` or quoted equivalent
- `lastStep: 8` or quoted equivalent
- `stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]` or an equivalent YAML list containing `1` through `8`

## Instructions

1. Read `{tracker_file}`.
2. If the architecture row status is `complete`, trust the tracker and read fully and follow `./step-08-epics-and-stories.md`.
3. Inspect `{architecture_file}` only because the tracker does not mark this gate complete.
4. If the file is missing or incomplete:
   - Update `{tracker_file}`:
     - `currentGate: architecture`
     - `status: blocked-on-architecture`
     - `nextRequiredAction: Run bmad-create-architecture with the user to create or complete _bmad-output/planning-artifacts/architecture.md, then continue to epics and stories.`
     - Artifact inventory architecture row status: `missing` or `incomplete`.
     - Used files: product brief, completed brainstorms, PRD, design-system MASTER.md, and UX design specification.
   - Invoke the `bmad-create-architecture` skill.
   - After `bmad-create-architecture` completes, re-check `{architecture_file}` and update `{tracker_file}`.
5. If the architecture is complete:
   - Update `{tracker_file}`:
     - architecture row status: `complete`
     - generated file: `_bmad-output/planning-artifacts/architecture.md`
     - used files: product brief, completed brainstorms, PRD, design-system MASTER.md, and UX design specification
     - `currentGate: epics-and-stories`
     - `nextRequiredAction: Check epics-and-stories tracker gate. If not complete, run bmad-create-epics-and-stories.`
6. If the user asks to stop, STOP. Otherwise read fully and follow `./step-08-epics-and-stories.md`.

## Success Criteria

- Architecture is complete and tracker advances to epics and stories, then the planner continues unless the user asks to stop.
