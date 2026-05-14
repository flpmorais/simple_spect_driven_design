# Step 8: Epics And Stories Gate

## Goal

Ensure epics and stories are created after architecture completion.

## Rules

- Read this entire step before acting.
- If the tracker already marks epics-and-stories `complete`, do not inspect `epics.md`; route to implementation readiness.
- The epics and stories skill is `bmad-create-epics-and-stories`.
- Completion is owned by `{tracker_file}` after the workflow completes.

## Instructions

1. Read `{tracker_file}`.
2. If the epics-and-stories row status is `complete`, trust the tracker and read fully and follow `./step-09-implementation-readiness.md`.
3. Update `{tracker_file}`:
   - `currentGate: epics-and-stories`
   - `status: blocked-on-epics-and-stories`
   - `nextRequiredAction: Run bmad-create-epics-and-stories, then mark epics-and-stories complete and continue to implementation readiness.`
   - Artifact inventory epics-and-stories row status: `missing-or-needs-refresh`.
   - Used files: PRD, UX design specification, architecture, and design-system MASTER.md.
4. Invoke `bmad-create-epics-and-stories`.
5. After the skill returns, update `{tracker_file}`:
   - epics-and-stories row status: `complete`
   - generated file: `_bmad-output/planning-artifacts/epics.md`
   - `currentGate: implementation-readiness`
   - `nextRequiredAction: Check implementation-readiness tracker gate. If not complete, run bmad-check-implementation-readiness.`
6. If the user asks to stop, STOP. Otherwise read fully and follow `./step-09-implementation-readiness.md`.

## Success Criteria

- Tracker marks epics-and-stories complete and the planner continues to implementation readiness unless the user asks to stop.
