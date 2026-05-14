# Step 1: Load And Validate Inputs

## Rules

- Speak in `{communication_language}`.
- Do not modify any file in this step.
- Fail gracefully if required files are missing or unreadable.

## Required Files

Load fully:

- `{architecture_file}` (`_bmad-output/planning-artifacts/architecture.md`)
- `{project_context_file}` (`_bmad-output/project-context.md`)

If either file is missing or unreadable, STOP and report:

```text
Cannot update project context.

Missing or unreadable required file: <path>
```

## Validate Current Project Context

Check the current project context:

- Has frontmatter.
- Has `# Project Context for AI Agents`.
- Has technical rule sections.
- Is under or near `{max_project_context_lines}` lines.

If current project context already exceeds 300 lines, continue only if the merge can reduce it safely. Otherwise STOP and ask the user whether to compress existing context first.

## Validate Architecture Scope

Confirm `architecture.md` appears to be a BMad architecture artifact or architecture work-package document.

Treat it as incremental even if it uses broad wording. The absence of an existing project-context rule from this architecture document is not removal evidence.

## Report Input Summary

Report:

- architecture file path
- project context file path
- current project-context line count
- architecture scope summary

Then load `./step-02-extract-deltas.md`.
