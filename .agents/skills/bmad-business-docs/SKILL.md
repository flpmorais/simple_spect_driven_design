---
name: bmad-business-docs
description: 'Create and maintain business/domain documentation. Use when the user asks to document business rules, workflows, policies, actors, terminology, decision tables, domain behavior, or business documentation.'
---

# Business Docs Workflow

**Goal:** Create and maintain business/domain documentation organized by business domain, with explicit rules, workflows, actors, terminology, decision tables, open questions, and discrepancies.

**Your Role:** Business documentation facilitator and domain rule curator. You help turn domain knowledge into durable documentation while clearly separating approved rules, proposed rules, observed implementation behavior, planned behavior, and open questions.

You will continue to operate with your given name, identity, and communication_style, merged with the details of this role description.

## Scope

This workflow documents business meaning and domain behavior:

- Business domains and bounded contexts
- Actors, responsibilities, and permissions
- Business rules and invariants
- Business workflows, states, and transitions
- Decision tables and trigger mappings
- Policies and cross-domain constraints
- Domain terminology and entity meanings
- Open questions and business/code discrepancies

This workflow does not document implementation details except as optional implementation evidence. Technical implementation belongs in `bmad-technical-docs`.

## Source Of Truth Rules

- Approved user/domain decisions are business truth.
- PRD, business rules docs, accepted planning artifacts, and explicit user input are business-intent sources.
- Code is observed implementation behavior, not automatically approved business policy.
- If code and approved business docs disagree, create a discrepancy instead of silently changing the rule.
- If a business rule has no source, mark it `proposed` or record it as an open question.

## Output Model

Default output root:

`{output_folder}/business-artifacts`

Default structure:

```text
business-artifacts/
  index.md
  glossary.md
  actors.md
  domains/
    <domain-slug>/
      overview.md
      rules.md
      workflows.md
      decision-tables.md
      open-questions.md
  cross-domain/
    policies.md
    invariants.md
    discrepancies.md
  business-docs-state.json
```

## Domain Split Rule

Create a separate business domain when an area has its own actors, lifecycle, decisions, terminology, workflow triggers, success/failure conditions, or ownership boundaries. Do not split by technical layer such as backend, frontend, API, database, or agent runtime.

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
- Business docs are maintained by domain folders.
- Update mode may replace targeted sections to prevent stale duplicates.

## Step Processing Rules

1. **Read completely:** Always read the entire current step file before taking action.
2. **Follow sequence:** Execute numbered sections in order.
3. **Wait for input:** If a menu is presented, halt and wait for user selection.
4. **Check continuation:** Only proceed to the next step when the current step says to do so.
5. **Save state:** Update frontmatter and state file when writing or modifying business docs.
6. **Load next:** Read the next step fully only when directed.

## Critical Rules

- Never invent business rules.
- Never treat implementation behavior as approved business policy.
- Never mix approved rules, observed behavior, planned behavior, and open questions.
- Never bury contradictions. Record them as discrepancies.
- Never split domains by technical components.
- Always preserve user-authored content outside targeted sections.
- Prefer decision tables for conditional logic.
- Prefer state tables or diagrams for lifecycle behavior.

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
- Use `{output_folder}` for business documentation output.
- Use `{planning_artifacts}` and `{project_knowledge}` as possible input sources only.

### Step 5: Resolve Workflow Paths

- `businessArtifactsRoot` = `{output_folder}/business-artifacts`
- `businessDocsIndex` = `{businessArtifactsRoot}/index.md`
- `businessStateFile` = `{businessArtifactsRoot}/business-docs-state.json`
- `domainsRoot` = `{businessArtifactsRoot}/domains`
- `crossDomainRoot` = `{businessArtifactsRoot}/cross-domain`

### Step 6: Greet The User

Greet `{user_name}` if you have not already, speaking in `{communication_language}`.

### Step 7: Execute Append Steps

Execute each entry in `{workflow.activation_steps_append}` in order.

Activation is complete. Begin the workflow below.

## Execution

Always speak in `{communication_language}`.
Always write documentation artifacts in `{document_output_language}`.

Read fully and follow: `./steps/step-01-route.md`
