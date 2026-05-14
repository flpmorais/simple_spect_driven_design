# Step 2: Read-Only Exploration

## Rules

- Speak in `{communication_language}`.
- Read `{refactor_file}` completely before exploring.
- Do not edit source code or any file outside `{refactor_dir}`.
- Exploration must be read-only.
- Do not proceed to analysis until exploration findings are written.

## Required Context

Load confirmed context from the `## Context` section in `{refactor_file}`.

Load the project context technical rules:

- `{project_context}` (`_bmad-output/project-context.md`)

If project context is missing or unreadable, fail gracefully: explain that `_bmad-output/project-context.md` is required as the golden technical rules source, update the bundle index as blocked if it already exists, and HALT.

## Exploration Subagents

Launch read-only exploration subagents in parallel when subagents are available. Each subagent must return concise structured Markdown with evidence paths and line references where possible.

### Impact Mapper

Prompt:

```text
You are the Impact Mapper for a refactor planning workflow. Read-only task. Given the confirmed refactor context, inspect the codebase and identify files, modules, routes, APIs, data contracts, tests, config, and documentation likely affected. Return: summary, affected areas, likely change points, dependencies, and evidence paths. Do not modify files.
```

### Risk Hunter

Prompt:

```text
You are the Risk Hunter for a refactor planning workflow. Read-only task. Given the confirmed refactor context, inspect the codebase for hidden coupling, fragile behavior, compatibility risks, migration risks, performance risks, security risks, and likely regressions. Return: risks, trigger conditions, consequences, severity, and evidence paths. Do not modify files.
```

### Test Mapper

Prompt:

```text
You are the Test Mapper for a refactor planning workflow. Read-only task. Given the confirmed refactor context, identify existing tests that cover affected behavior, missing tests, useful validation commands, and suggested test additions. Return: current coverage, gaps, required validation, and evidence paths. Do not modify files.
```

### Project Context Auditor

Prompt:

```text
You are the Project Context Auditor for a refactor planning workflow. Read-only task. Given the confirmed refactor context plus `_bmad-output/project-context.md`, identify technical rules, workflow rules, testing rules, anti-patterns, forbidden deviations, and conflicts between the requested refactor and project context. Return: rules, conflicts, questions, and evidence paths. Do not modify files.
```

If subagents are not available, perform the four exploration roles yourself sequentially and state this limitation in `## Exploration`.

## Write Exploration Section

Replace the `## Exploration` section in `{refactor_file}` with:

```markdown
## Exploration

### Exploration Scope

### Impact Mapper Findings

### Risk Hunter Findings

### Test Mapper Findings

### Project Context Auditor Findings

### Exploration Limitations
```

Update frontmatter:

- `phase: analysis`
- append `exploration` to `phasesCompleted`
- update `lastUpdated`

Then load `./step-03-analysis.md`.

## Success Criteria

- Exploration covers code impact, risks, tests, and project context alignment.
- Findings include evidence paths where possible.
- Only files inside `{refactor_dir}` are modified.
