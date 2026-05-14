# Step 3: Brainstorming Gate

## Goal

Ensure brainstorming is complete before PRD creation or validation can proceed.

## Rules

- Read this entire step before acting.
- Refuse PRD or architecture work until this gate passes.
- If the tracker already marks brainstorming `complete`, do not inspect brainstorm files; route to PRD.
- At least one completed brainstorm must exist in `{brainstorming_folder}`.
- All existing brainstorm files in `{brainstorming_folder}` must be complete.
- The brainstorming skill is `bmad-brainstorming`.

## Completion Check

A brainstorm file is complete only when its frontmatter contains all of:

- `workflow_completed: true`
- `session_active: false`
- `stepsCompleted: [1, 2, 3, 4]` or an equivalent YAML list containing `1`, `2`, `3`, and `4`

The brainstorming gate is complete only when:

- `{brainstorming_folder}` exists.
- At least one `*.md` file exists in `{brainstorming_folder}`.
- At least one brainstorm file is complete.
- No brainstorm file in `{brainstorming_folder}` is incomplete.

## Instructions

1. Read `{tracker_file}`.
2. If the brainstorming row status is `complete`, trust the tracker and read fully and follow `./step-04-prd.md`.
3. List all markdown files in `{brainstorming_folder}` only because the tracker does not mark this gate complete.
4. Read the frontmatter of each brainstorm file.
5. Classify each file as complete or incomplete using the criteria above.
6. If there are no brainstorm files, no completed brainstorms, or any incomplete brainstorms:
   - Update `{tracker_file}`:
     - `currentGate: brainstorming`
     - `status: blocked-on-brainstorming`
     - `nextRequiredAction: Run bmad-brainstorming to create or complete brainstorming sessions, then stop. Do not run PRD or architecture until at least one brainstorm is complete and all brainstorm files are complete.`
     - Artifact inventory brainstorming row status: `missing`, `no-complete-session`, or `incomplete-sessions`.
     - Generated files: list any brainstorm files found.
     - Append a run-log entry listing incomplete files, if any.
   - Tell the user the planner refuses PRD and architecture work until brainstorming is complete.
   - Invoke the `bmad-brainstorming` skill.
   - After `bmad-brainstorming` completes, re-check brainstorm files and update `{tracker_file}`.
   - If the user asks to stop, STOP. Otherwise continue to `./step-04-prd.md`.
7. If the brainstorming gate is complete:
   - Update `{tracker_file}`:
     - brainstorming row status: `complete`
     - generated files: all complete brainstorm file paths
     - `currentGate: prd`
      - `nextRequiredAction: Check for a complete PRD at _bmad-output/planning-artifacts/prd.md because the tracker has not marked PRD complete.`
   - Read fully and follow `./step-04-prd.md`.

## Success Criteria

- Brainstorming gate passes and tracker advances to `prd`, then the planner continues unless the user asks to stop.
