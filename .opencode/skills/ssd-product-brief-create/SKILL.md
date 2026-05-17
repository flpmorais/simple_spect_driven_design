---
name: ssd-product-brief-create
description: Create the first foundational product brief for a project through focused discovery, optional ideation, user validation, and SQLite memory storage.
---

# ssd-product-brief-create

Use when the user asks to create the first product brief, define a new product at a high level, or produce the foundational product definition for a project.

OpenCode-native only. Do not use BMad config/steps, hidden workflow variables, artifact scanning, existing planning docs, or markdown product brief files.

## Contract

Input:

```json
{
  "product_or_problem_area": "required unless obvious",
  "initial_context": "optional seed context or user brain dump"
}
```

Rules:

- Read and apply `.opencode/shared/product-brief-contract.md` first.
- Bootstrap and read `product-classifications` through `.opencode/scripts/ssd_memory/memory.py reference` before drafting classification.
- Always guided. Do not offer `headless`, `autonomous`, `yolo`, or `draft-first` modes.
- If `product_or_problem_area` is missing, ask only: "What product, project, or problem area should we explore for the product brief?"
- Ask once near the start whether to include an existing stored memory object or file unless the request names one.
- Source files are read directly. Stored memory objects are loaded through `.opencode/shared/recipes.md` plus the relevant recipe; do not inspect memory scripts unless the recipe is missing or fails.
- Confirm selected source memory objects before drafting. If ambiguous, show concise candidates and ask the user to choose; never silently choose.
- If `.opencode/scripts/ssd_product_brief/memory.py get` finds an existing Product Brief, stop and tell the user to use `ssd-product-brief-edit`.
- Write Product Brief memory exactly once, after internal review and explicit approval, through `.opencode/scripts/ssd_product_brief/memory.py create`.
- Do not create Product Brief markdown or temp markdown drafts.
- Run at most one optional ideation pass unless the user explicitly asks for more.

## Memory

- Shared contract: `.opencode/shared/product-brief-contract.md`
- Memory adapter: `.opencode/scripts/ssd_product_brief/memory.py`
- Product classifications reference list: `.opencode/scripts/ssd_memory/memory.py reference bootstrap/get --list-key product-classifications`
- Artifact recipe index: `.opencode/shared/recipes.md`
- Artifact kind: `product-brief`
- Artifact ID: UUID returned by memory command
- Optional product brainstorm memory: returned by `ssd-brainstorming` memory handoff

## Workflow

### 1. Frame

State briefly that this creates a foundational product definition and excludes technical planning, PRD requirements, MVP scope, roadmap, success metrics, epics, stories, delivery planning, and implementation detail.

### 2. Preflight

Run:

```text
python .opencode/scripts/ssd_product_brief/memory.py get
```

If a Product Brief exists, stop and tell the user to use `ssd-product-brief-edit`. If missing, continue.

### 3. Focused Discovery

Use `initial_context` first. Gather only enough information to populate the shared contract's required sections.

If no source was named, ask:

```text
Is there any existing stored memory object or file you want me to use as source material for this Product Brief?
```

Handle sources as defined in Contract rules. Confirm selected memory objects with:

```text
I found this source memory object:
- <memory type>: <title/topic>
- ID: <id>
- Created: <created_at>
- Status: <status>

Use this as Product Brief source material?
```

Do not run a questionnaire by default. Ask at most 3 focused questions only when drafting would be speculative. If budget or team are missing, ask one concise combined question; otherwise store `Unknown` per contract.

Track evidence per required section. Vague fragments, broad labels, and yes/no answers are weak evidence unless they directly establish a product-level fact.

### 4. Optional Ideation

Recommend one short ideation pass when the shared contract says context is thin, vague, generic, conflicted, or assumption-heavy. The user may decline.

Use this style:

```text
The product direction is still thin. I recommend a short ideation pass before drafting so the brief has stronger problem, audience, and differentiation material. Do you want to run that now?
```

Before starting a new Product Brief brainstorm, run:

```text
python .opencode/scripts/ssd_brainstorming/memory.py list
```

Resume exactly one unfinished matching brainstorm when `status` is `active` or `finished_at` is empty, `downstream_consumer=ssd-product-brief-create`, and topic/goal matches. If multiple match, show numbered candidates and ask the user to choose. Create a new brainstorm only when no match exists or the user explicitly starts over.

If accepted, call `ssd-brainstorming` once with:

```json
{
  "run_mode": "internal",
  "topic": "<product_or_problem_area>",
  "initial_context": "<initial_context plus focused discovery notes>",
  "scope": "quick",
  "downstream_consumer": "ssd-product-brief-create",
  "mode": "guided",
  "goal": "Explore why this product should exist, who it is for, what problem makes it necessary, how it solves the problem at a high level, and what makes it meaningfully different or well-positioned.",
  "constraints": "Apply .opencode/shared/product-brief-contract.md. Avoid implementation, architecture, MVP scope, success metrics, delivery planning, epics, stories, and engineering tasks. Return memory references, not markdown paths."
}
```

Use returned brainstorm memory handoff and idea references as source material.

### 5. Draft Section Payload

Before drafting, run:

```text
python .opencode/scripts/ssd_memory/memory.py reference bootstrap --list-key product-classifications
python .opencode/scripts/ssd_memory/memory.py reference get --list-key product-classifications
```

Draft a JSON-compatible Product Brief section payload in working context using the required section keys from the shared contract.

Allowed sources: product/problem area, initial context, focused discovery, direct files, loaded artifacts, optional brainstorm memory, approved assumptions, or `Unknown`.

Apply contract rules for `product-classification`, `budget`, and `team`: reference-list-backed inferred classification requires user confirmation; budget/team are direct-input-only or `Unknown`.

Do not pad thin source material into polished prose. Unsupported or partial content becomes `Unknown`, `Assumption:`, or Open Questions.

Core sections need direct support before approval review: `why-this-exists`, `product-classification`, `product-definition`, `problem`, `high-level-solution`, and `audience`.

Preserve readable formatting in `canonical_text`: bullets each start on their own `- ` line; paragraphs are separated by newline characters; never flatten bullets or paragraphs into one inline string.

### 6. Internal Review Gate

Apply the shared contract review rules before showing the payload.

Run a grounding audit:

1. Identify explicit source facts for each required section.
2. Replace unsupported content with `Unknown`.
3. Move partial unsupported content to Open Questions or `Assumption:`.
4. Verify classification, budget, and team follow contract rules.
5. Block approval review if core sections other than classification are mostly inferred.
6. Verify bullet and paragraph newlines are preserved.

If core sections remain generic, inferred, or unsupported, ask up to 3 focused evidence questions or recommend the optional ideation pass if not already offered. If declined or unanswered, keep uncertainty as `Unknown` or `Assumption:` and do not present it as complete.

### 7. Create Validation Gate

Before approval, always run one internal `ssd-advanced-elicitation` pass using `Challenge from Critical Perspective`. This create-only gate stress-tests unsupported claims, shallow assumptions, unconfirmed or weak classification, budget/team inference, overconfident positioning, missing constraints, hallucinated specificity, verbose thin-evidence prose, flattened formatting, and unsupported core sections.

Use revision-ready output. Ask up to 3 validation questions, normally 3 for minimal-input drafts. Questions must target only the issues above and must not cover implementation, architecture, roadmap, metrics, detailed requirements, MVP scope, epics, stories, feature backlog, or general brainstorming.

After answers, refine the section payload and rerun the grounding audit.

Run one internal `Socratic Questioning` fallback only if blocking strategic gaps remain. Blocking gaps are unresolved choices that materially change audience, product-level problem, product definition, necessity versus existing tools/workflows, or the core operating constraint.

Do not run Socratic fallback for implementation details, backlog items, nice-to-have details, future expansion, or fields that can safely be `Unknown`, an assumption, or an open question. If it runs, cap at 3 questions, ask only blocking strategic questions, refine once, then stop.

Do not present the Product Brief for approval if validation still finds unsupported core sections that would make it misleading. Instead explain the blocker and offer more user-led discovery or storing an explicitly incomplete brief only if the user accepts the `Unknown` and `Assumption:` markers.

### 8. User Section Validation Gate

Present the complete proposed Product Brief in human-readable Markdown before writing memory. Include every required heading and proposed content, then sources, classification confirmation, assumptions, open questions, and validation summary.

Approval prompt placement: never ask before showing the content. Put the approval/change instruction as the final paragraph.

Use this style:

```text
Proposed Product Brief

<all Product Brief sections>

Source Memory Objects Used
<sources or None>

Classification To Confirm
<primary, secondary, rationale, and uncertainty>

Assumptions That Will Be Stored
<assumptions or None>

Open Questions That Will Remain Unresolved
<open questions or None>

Validation Summary
<create validation summary>

Review complete. Reply with `approve` or `create it` to confirm the classification and store this Product Brief, or tell me what to change by section.
```

Do not call `create` until the user explicitly approves after seeing the reviewed sections and inferred classification. Approval must be affirmative (`approved`, `create it`, `looks good`, or equivalent) and counts as classification confirmation only after the classification is shown. Clarification, discussion, source selection, or answers to questions are not approval.

Before `create`, recheck line breaks and rewrite flattened bullets such as `- first - second - third` as newline-separated bullets.

### 9. Revise Section Payload

If the user requests changes, apply clear fixes to the working section payload and repeat the User Section Validation Gate. If approved, finalize.

### 10. Finalize Once

After explicit approval, pass the approved payload on stdin:

```text
python .opencode/scripts/ssd_product_brief/memory.py create
```

Set `cited_brainstorm_ids` and `cited_idea_ids` when optional ideation or loaded brainstorm artifacts contributed source material.

### 11. Return Result

Return:

```json
{
  "status": "complete|blocked|failed",
  "artifact_kind": "product-brief",
  "artifact_id": "<uuid>",
  "ideation_used": "boolean",
  "cited_brainstorm_ids": [],
  "cited_idea_ids": [],
  "warnings": []
}
```

## Hard Stops

- Do not scan project artifacts or existing docs.
- Do not call `.agents/skills/bmad-product-brief`.
- Do not create, edit, read, or depend on `ssd_docs/1_product_brief.md`.
- Do not create temp Product Brief markdown.
- Do not skip internal review.
- Do not skip the create-only advanced elicitation validation gate.
- Do not store inferred Product Brief section content as fact.
- Do not write Product Brief memory before explicit user approval of proposed sections.
- Do not output only JSON or a tool result as the user-facing review or final response.
- Do not run more than one optional ideation pass unless the user explicitly asks.
