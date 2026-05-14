---
name: ssd-brainstorming
description: Durable SSD brainstorming with raw capture, critique, review, and final distillation.
---

# ssd-brainstorming

Use for ideation, alternatives, assumption challenge, and downstream context. This skill writes a raw working file, preserves all useful ideas, then calls `ssd_distillator` to produce the final distillate.

## Inputs

```json
{
  "run_mode": "interactive|internal",
  "topic": "required unless obvious",
  "goal": "required unless obvious",
  "initial_context": "optional seed context or user brain dump",
  "scope": "quick|normal|deep",
  "target_folder": "subfolder under brainstorming/",
  "downstream_consumer": "optional consumer skill/workflow",
  "constraints": [],
  "mode": "guided|adversarial|progressive|random-catalyst",
  "required_techniques": "optional integer",
  "techniques": [{"name": "optional", "purpose": "optional"}]
}
```

Defaults: `run_mode=interactive`, `scope=normal`, `target_folder=general`, `downstream_consumer=general`, `mode=guided`.

If required inputs are missing, ask only for the missing fields. In `internal` mode, return a concise blocker to the caller instead of asking the user directly.

## Paths

- Filename: `brainstorm-<yyyy-mm-dd-hh-mm>-<shorttopic>.md`.
- Raw: `._ssd_docs_temp/brainstorming/<target_folder>/<filename>`.
- Final: `._ssd_docs_distil/brainstorming/<target_folder>/<filename>`.
- `shorttopic`: lowercase ASCII slug; choose a neutral slug for sensitive or awkward topics.
- Treat `target_folder` as a subfolder name, not an arbitrary path.

## Scope Thresholds

- `quick`: 20 ideas.
- `normal`: 50 ideas.
- `deep`: 100 ideas.
- Batch size: 10 ideas.

Scope is an enough-to-proceed threshold, not a hard cap. Do not stop automatically at the threshold. At the threshold, recommend synthesis/proceeding. If useful input continues, keep capturing it and recommend stopping more strongly as overage grows. Stop only when the user or invoking skill requests finish/proceed/synthesis/stop, or when an external limit/failure prevents continuing.

If finishing below threshold, return `complete_with_warnings`. If finishing at or above threshold, return `complete` unless another blocker occurs.

## Internal Mode

In `run_mode=internal`, hide implementation mechanics in user-facing text: do not say this skill/workflow is running, do not show technique menus, and do not expose technique names. Use domain-natural language if progress text is needed. Still record techniques in the raw file.

Technique resolution:

- Call `ssd_technique_selector` before generating ideas.
- Pass `goal`, `scope`, `initial_context`, `constraints`, `required_techniques`, and caller `techniques` as `preselected_techniques`, preserving each technique `name` and `purpose` exactly as provided.
- If `required_techniques` is omitted, use `quick=2`, `normal=3`, `deep=5`.
- Execute only the selector-returned `action` values.
- If a selector-returned technique includes `caller_purpose`, apply that purpose as the run-specific focus for the action. Do not treat `caller_purpose` as display-only metadata.
- If the selector returns `blocked`, return `blocked` and do not create or update raw files.

## Raw File Requirements

Create/update only the raw file under `._ssd_docs_temp/brainstorming/<target_folder>/`.

Frontmatter must include: `type: ssd-brainstorm-raw`, `run_mode`, `topic`, `goal`, `initial_context`, `scope`, `target_ideas`, `mode`, `target_folder`, `downstream_consumer`, `techniques`, `created`, `final_distillate`.

Then include `# Raw Brainstorm: <topic>` and a `## Session Frame` with goal, initial context, constraints, scope threshold, mode, downstream consumer, and selector-returned techniques including any `caller_purpose` values. Treat `initial_context` as source material, not as a constraint.

Each idea must be self-contained:

```markdown
### Idea <number>: <short title>
- Concept: <2-4 sentences>
- Why it might work: <specific rationale>
- Hidden assumption: <assumption>
- Failure mode or risk: <risk>
- Domain: <technical|user|business|operations|ethics|edge-case|long-term|other>
```

After every 10 ideas append:

```markdown
## Batch <n> Critique
- Repeated patterns: <patterns>
- Weak assumptions: <assumptions>
- Missing stakeholders: <stakeholders>
- Boring/default ideas: <too-obvious directions>
- Domain pivot for next batch: <pivot>
```

Avoid duplicate or filler ideas. If ideas narrow too much, pivot domains or use adversarial prompts.

## Finish And Distill

When stop/proceed/synthesis is requested, read the full raw file before distillation. Append:

```markdown
## Full Raw Review
- Strongest ideas: <list with reasons>
- Most surprising ideas: <list with reasons>
- Quick wins: <list with reasons>
- Risky bets: <list with reasons>
- Major themes: <themes>
- Unresolved questions: <questions>
- Ideas to avoid or treat carefully: <weak/risky directions>
```

Do not distill until `## Full Raw Review` exists. If below threshold, include the shortfall reason in the review.

Call `ssd_distillator` with one explicit raw file path:

```json
{
  "source_documents": ["._ssd_docs_temp/brainstorming/<target_folder>/<filename>"],
  "downstream_consumer": "<downstream_consumer or general>",
  "output_path": "._ssd_docs_distil/brainstorming/<target_folder>/<filename>",
  "audit": true,
  "max_fix_passes": 2,
  "fail_on_audit_findings": false
}
```

Never pass a folder or glob to `ssd_distillator`. Do not hand-write final distillates.

## Result

Return concise structured output:

```json
{
  "status": "complete|complete_with_warnings|blocked|failed",
  "raw_brainstorm": "._ssd_docs_temp/brainstorming/<target_folder>/<filename>",
  "distillate": "._ssd_docs_distil/brainstorming/<target_folder>/<filename>",
  "ideas_generated": 20,
  "target_ideas": 20,
  "scope": "quick",
  "target_folder": "<target_folder>",
  "downstream_consumer": "<downstream_consumer or general>",
  "completion_reason": "user_or_invoking_skill_requested_finish",
  "warnings": []
}
```

Do not modify source code, tests, repo config, unrelated workflow artifacts, or final distillates directly.
