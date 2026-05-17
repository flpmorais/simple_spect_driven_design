---
name: ssd-product-brief-edit
description: Edit an existing SQLite-backed Product Brief while preserving the shared product-brief contract.
---

# ssd-product-brief-edit

Use when the user asks to revise, update, correct, or pivot an existing Product Brief.

OpenCode-native only. Do not use BMad config/steps, hidden workflow variables, artifact scanning, existing planning docs, downstream artifact checks, or markdown product brief files.

## Contract

Input:

```json
{
  "change_request": "required unless obvious",
  "additional_context": "optional"
}
```

Rules:

- Read and apply `.opencode/shared/product-brief-contract.md` first.
- Bootstrap and read `product-classifications` through `.opencode/scripts/ssd_memory/memory.py reference` before editing classification.
- If `change_request` is missing, ask only: "What change should we make to the Product Brief?"
- If `.opencode/scripts/ssd_product_brief/memory.py get` reports no Product Brief, stop and tell the user to run `ssd-product-brief-create` first.
- Update Product Brief memory only after inline review and explicit approval, through `.opencode/scripts/ssd_product_brief/memory.py update`.
- Do not run the create validation gate; mandatory `Challenge from Critical Perspective` belongs only to `ssd-product-brief-create`.
- Do not create Product Brief markdown or temp markdown drafts.
- Run at most one optional ideation pass unless the user explicitly asks for more.

## Memory

- Shared contract: `.opencode/shared/product-brief-contract.md`
- Product classifications reference list: `.opencode/scripts/ssd_memory/memory.py reference bootstrap/get --list-key product-classifications`
- Memory adapter: `.opencode/scripts/ssd_product_brief/memory.py`
- Artifact kind: `product-brief`
- Artifact ID: UUID returned by memory command
- Optional edit brainstorm memory: returned by `ssd-brainstorming` memory handoff

## Workflow

### 1. Preflight

Read the shared contract and run:

```text
python .opencode/scripts/ssd_product_brief/memory.py get
```

If missing, stop with:

```text
Product Brief is required before editing.
Expected memory: Product Brief artifact with kind `product-brief`
Run ssd-product-brief-create first.
```

Use returned artifact and current sections as the edit base.

### 2. Classify Change

Classify as one of: minor wording cleanup, section update, positioning or audience change, or major product pivot.

### 3. Clarify

Ask at most 3 questions only for ambiguity, contradiction, strategic choice, or missing direct input for requested budget/team changes. If unknown, continue safely; budget/team become `Unknown` unless directly stated.

### 4. Optional Ideation

Recommend one short ideation pass only for major pivots, unclear audience, weak positioning, or changed problem framing. The user may decline.

If accepted, call `ssd-brainstorming` once with:

```json
{
  "run_mode": "internal",
  "topic": "<product_or_problem_area from existing brief or change request>",
  "initial_context": "<existing Product Brief memory plus change request plus clarifications>",
  "scope": "quick",
  "downstream_consumer": "ssd-product-brief-edit",
  "mode": "guided",
  "goal": "Explore the requested brief change at product-definition level: why it matters, audience impact, positioning, assumptions, and contradictions with the current brief.",
  "constraints": "Apply .opencode/shared/product-brief-contract.md. Avoid implementation, architecture, MVP scope, success metrics, delivery planning, epics, stories, and engineering tasks. Return memory references, not markdown paths."
}
```

Use returned brainstorm memory handoff and idea references as edit source material.

### 5. Draft Edited Section Payload

Before editing classification, run:

```text
python .opencode/scripts/ssd_memory/memory.py reference bootstrap --list-key product-classifications
python .opencode/scripts/ssd_memory/memory.py reference get --list-key product-classifications
```

Create an edited Product Brief section payload in working context from current memory sections.

Apply only requested changes, required consistency fixes, and source-backed additions from clarification or optional ideation.

Apply contract rules for changed `product-classification`, `budget`, and `team`: reference-list-backed inferred classification requires user confirmation; budget/team are direct-input-only or `Unknown`.

Preserve all required section keys. Preserve readable `canonical_text`: bullets each start on their own `- ` line; paragraphs are newline-separated; never flatten bullets or paragraphs into one inline string.

### 6. Inline Review Gate

Apply the shared contract inline review gate to the edited payload.

Validate the change, not the full document:

- Compare current memory sections with the edited payload.
- Show a concise change summary and only changed sections.
- For each changed section, show before/after bullets or an equivalent Markdown delta.
- Include only affected sources, assumptions, and open questions.
- If classification changed, show primary, secondary, rationale, uncertainty, and confirm through final approval.
- If budget or team changed, verify direct user input or `Unknown`.
- Do not display unchanged sections unless the user asks.
- Offer: "Do you want to see the full final document or any specific section before approval?"
- Verify changed sections preserve newline-separated bullets and paragraphs before asking for approval.

Render the complete focused change review first, then put approval/change instruction as the final paragraph:

```text
Product Brief Change Review

Change Summary
<concise summary>

Changed Sections
<before/after bullets or focused deltas>

Affected Assumptions, Open Questions, And Sources
<affected items or None>

Optional Full Review
If you want, ask to see the full final document or any specific section before approval.

Review complete. Reply with `approve` or `update it` to confirm the classification if changed and update the Product Brief, or tell me what to change by section.
```

Do not run `update` until explicit approval after the focused review. If classification changed, approval confirms it only after it is shown. If the edit remains generic, conflicted, or assumption-heavy, recommend the single optional ideation pass if not already used; if declined, use `Unknown` or `Assumption:` where safe, or block if misleading.

### 7. Apply Edit

Pass the reviewed payload on stdin:

```text
python .opencode/scripts/ssd_product_brief/memory.py update
```

Set `cited_brainstorm_ids` and `cited_idea_ids` when optional ideation contributed source material. If omitted, the adapter preserves existing current provenance.

If update fails because memory is missing, rerun preflight and stop if the Product Brief no longer exists.

Before `update`, recheck line breaks and rewrite flattened bullets such as `- first - second - third` as newline-separated bullets.

### 8. Return Result

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

- Do not proceed if Product Brief memory is missing.
- Do not call BMad skills.
- Do not scan project artifacts.
- Do not create, edit, read, or depend on `ssd_docs/1_product_brief.md`.
- Do not create temp Product Brief markdown.
- Do not skip inline review.
- Do not run the Product Brief create validation gate.
- Do not run more than one optional ideation pass unless the user explicitly asks.
- Do not edit or warn about downstream artifacts automatically.
