# Product Brief Contract

Apply this contract for product brief creation and editing.

## Artifact Boundary

The Product Brief is a business/product definition for non-experts. Priority order:

1. Why this should exist.
2. What is being built.
3. How it solves the problem at a high level.
4. Who it is for.

Include differentiation, positioning, practical constraints, assumptions, and useful open questions.

Exclude technology stack, architecture, databases, hosting, containers, frameworks, implementation patterns, detailed requirements, MVP scope, success metrics, epics, stories, delivery plans, and engineering tasks.

If the product itself is a technical tool, discuss only high-level product value, user problem, audience, and concept. Do not discuss implementation details.

## Required Sections

Use the template at `.opencode/skills/ssd-product-brief-create/templates/product-brief-template.md` for new briefs and to repair malformed briefs.

Required sections:

- Why This Exists
- Product Definition
- Problem
- High-Level Solution
- Audience
- Necessity And Differentiation
- Positioning
- Practical Constraints
- Assumptions
- Open Questions

If source material does not support a required section, state `Unknown` or record a clear assumption. Do not invent content.

## Optional Ideation

Recommend one short ideation pass when context is thin, vague, generic, conflicted, or assumption-heavy. The user may decline.

Do not pass `required_techniques` or fixed `techniques` to `ssd-brainstorming`. Let `ssd-brainstorming` select techniques.

Run at most one optional ideation pass unless the user explicitly asks for more.

## Inline Review Gate

Review the temp draft before finalization. Do not call product-brief review subagents.

The draft cannot be finalized while it has:

- invented unsupported specificity;
- generic `why`, `problem`, or `differentiation`;
- missing audience without `Unknown`;
- missing constraints without `Unknown`;
- unresolved contradiction with source material;
- forbidden technical, architecture, implementation, PRD, MVP, roadmap, metrics, delivery, epics, or stories content.

Also check that the high-level solution connects to the problem, positioning is clear, assumptions are explicit, and open questions are useful rather than excessive.

Ask the user only when a finding requires a strategic choice: audience ambiguity, conflicting positioning, contradictory constraints, major assumption inclusion/removal, or multiple viable product directions.

## Final Distillation

After writing `ssd_docs/1_product_brief.md`, call `ssd_distillator` exactly with:

```json
{
  "source_documents": ["ssd_docs/1_product_brief.md"],
  "downstream_consumer": "PRD creation",
  "output_path": "._ssd_docs_distil/_docs/1_product_brief.md",
  "audit": true,
  "max_fix_passes": 2,
  "fail_on_audit_findings": false
}
```

The caller provides the output path; the distillator must not guess.
