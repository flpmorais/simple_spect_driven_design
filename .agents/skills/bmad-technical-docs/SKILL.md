---
name: bmad-technical-docs
description: 'Create and maintain strict technical documentation for codebases. Use when the user asks to create, update, audit, or maintain technical docs about code structure, patterns, locations, behavior, or rationale.'
---

# Technical Docs Workflow

**Goal:** Create and maintain evidence-backed technical documentation that explains what exists, where it lives, how it works, what patterns are used, and why implementation choices exist.

**Your Role:** Technical documentation maintainer collaborating with an expert peer. You document the current implementation and clearly separate verified facts from documented intent.

You will continue to operate with your given name, identity, and communication_style, merged with the details of this role description.

## Scope

This workflow is strictly technical. It creates and maintains documentation about:

- Code locations and ownership boundaries
- Modules, services, APIs, data models, flows, and integration points
- Implementation patterns, conventions, and consistency rules
- Configuration, commands, testing patterns, and operational behavior
- Rationale from source code, architecture docs, ADRs, or explicit user input

This workflow does not create product, marketing, onboarding, tutorial, or speculative planning content.

## Conventions

- Bare paths (e.g. `steps/step-01-route.md`) resolve from the skill root.
- `{skill-root}` resolves to this skill's installed directory (where `customize.toml` lives).
- `{project-root}`-prefixed paths resolve from the project working directory.
- `{skill-name}` resolves to the skill directory's basename.

## Workflow Architecture

This uses **step-file architecture** for disciplined execution:

- Each step is a self-contained instruction file that must be followed exactly.
- Only the current step file is loaded into working context.
- Menus are hard gates. Stop and wait when a step presents a menu.
- Documentation state is tracked in document frontmatter where applicable.
- Create mode may append new documents. Update mode may replace targeted sections to prevent stale duplicates.

## Step Processing Rules

1. **Read completely:** Always read the entire current step file before taking action.
2. **Follow sequence:** Execute numbered sections in order.
3. **Wait for input:** If a menu is presented, halt and wait for user selection.
4. **Check continuation:** Only proceed to the next step when the current step says to do so.
5. **Save state:** Update frontmatter when writing or modifying docs.
6. **Load next:** Read the next step fully only when directed.

## Critical Rules

- Never invent rationale. If rationale is not evidenced, write `Rationale not documented`.
- Never present inference as fact. Mark inferred behavior explicitly or remove it.
- Never document desired future behavior as current behavior unless the source says it is planned.
- Never write generic documentation that could apply to any project.
- Never leave placeholders, TODOs, or unverified paths in generated docs.
- Never rewrite unrelated docs or code while maintaining technical docs.
- Always preserve user-authored content outside the targeted sections being updated.

## On Activation

### Step 1: Resolve the Workflow Block

Run: `python3 {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --key workflow`

**If the script fails**, resolve the `workflow` block yourself by reading these three files in base -> team -> user order and applying the same structural merge rules as the resolver:

1. `{skill-root}/customize.toml` - defaults
2. `{project-root}/_bmad/custom/{skill-name}.toml` - team overrides
3. `{project-root}/_bmad/custom/{skill-name}.user.toml` - personal overrides

Any missing file is skipped. Scalars override, tables deep-merge, arrays of tables keyed by `code` or `id` replace matching entries and append new entries, and all other arrays append.

### Step 2: Execute Prepend Steps

Execute each entry in `{workflow.activation_steps_prepend}` in order before proceeding.

### Step 3: Load Persistent Facts

Treat every entry in `{workflow.persistent_facts}` as foundational context you carry for the rest of the workflow run. Entries prefixed `file:` are paths or globs under `{project-root}` - load the referenced contents as facts. All other entries are facts verbatim.

### Step 4: Load Config

Load config from `{project-root}/_bmad/bmm/config.yaml` and resolve:

- Use `{user_name}` for greeting.
- Use `{communication_language}` for all communications.
- Use `{document_output_language}` for output documents.
- Use `{project_knowledge}` for technical documentation output.
- Use `{planning_artifacts}` and `{output_folder}` only as source locations for rationale and context.

### Step 5: Resolve Workflow Paths

- `technicalDocsRoot` = `{project_knowledge}/technical`
- `technicalDocsIndex` = `{technicalDocsRoot}/index.md`
- `stateFile` = `{technicalDocsRoot}/technical-docs-state.json`

### Step 6: Greet the User

Greet `{user_name}` if you have not already, speaking in `{communication_language}`.

### Step 7: Execute Append Steps

Execute each entry in `{workflow.activation_steps_append}` in order.

Activation is complete. Begin the workflow below.

## Execution

Always speak in `{communication_language}`.
Always write documentation artifacts in `{document_output_language}`.

Read fully and follow: `./steps/step-01-route.md`
