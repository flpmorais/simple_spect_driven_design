# Step 2: Product Brief Gate

## Goal

Ensure a complete product brief exists before any other planning work can proceed.

## Rules

- Read this entire step before acting.
- Refuse to do anything else until a complete product brief exists.
- If the tracker already marks product-brief `complete`, do not inspect the product brief file; route to brainstorming.
- The product brief skill is `bmad-product-brief`.
- The expected product brief file is `{output_folder}/product-brief-{project_name}.md`.
- Product brief distillates do not satisfy this gate.

## Completion Check

The product brief is complete only when:

- `{product_brief_file}` exists and is readable.
- Its frontmatter contains `status: "complete"` or `status: 'complete'` or `status: complete`.

## Instructions

1. Read `{tracker_file}`.
2. If the product-brief row status is `complete`, trust the tracker and read fully and follow `./step-03-brainstorms.md`.
3. Inspect `{product_brief_file}` only because the tracker does not mark this gate complete.
4. If the file is missing or does not have complete status:
   - Update `{tracker_file}`:
     - `currentGate: product-brief`
     - `status: blocked-on-product-brief`
     - `nextRequiredAction: Run bmad-product-brief to create a complete product brief, then stop. Do not run brainstorming, PRD, or architecture until the product brief is complete.`
     - Artifact inventory product-brief row status: `missing` or `incomplete`.
     - Append a run-log entry with the reason.
   - Tell the user the planner refuses downstream planning until product brief is complete.
   - Invoke the `bmad-product-brief` skill.
   - After `bmad-product-brief` completes, re-check `{product_brief_file}` and update `{tracker_file}` with the generated product brief path and status.
   - If the user asks to stop, STOP. Otherwise continue to `./step-03-brainstorms.md`.
5. If the product brief is complete:
   - Update `{tracker_file}`:
     - product-brief row status: `complete`
     - generated file: `_bmad-output/product-brief-{project_name}.md`
     - `currentGate: brainstorming`
     - `nextRequiredAction: Check _bmad-output/brainstorming because the tracker has not marked brainstorming complete. Require at least one complete brainstorming session and verify all existing brainstorms are complete.`
   - Read fully and follow `./step-03-brainstorms.md`.

## Success Criteria

- Complete product brief exists and tracker advances to `brainstorming`, then the planner continues unless the user asks to stop.
