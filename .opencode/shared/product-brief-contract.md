# Product Brief Contract

Apply this contract for product brief creation and editing.

## Artifact Boundary

The Product Brief is a business/product definition for non-experts. Priority order:

1. Why this should exist.
2. What is being built.
3. How it solves the problem at a high level.
4. Who it is for.

Include differentiation, positioning, practical constraints, assumptions, and useful open questions.

Exclude technology stack, architecture, databases, hosting, containers, frameworks, implementation patterns, detailed requirements, MVP scope, success metrics, epics, stories, delivery plans, and engineering tasks. If the product is technical, discuss only product value, user problem, audience, and concept.

## Required Sections

Store the Product Brief as SQLite-backed `Artifact` memory with kind `product-brief`. Use these exact section keys and headings:

| Section Key | Heading |
| --- | --- |
| `why-this-exists` | Why This Exists |
| `product-definition` | Product Definition |
| `problem` | Problem |
| `high-level-solution` | High-Level Solution |
| `audience` | Audience |
| `necessity-and-differentiation` | Necessity And Differentiation |
| `positioning` | Positioning |
| `practical-constraints` | Practical Constraints |
| `assumptions` | Assumptions |
| `open-questions` | Open Questions |

Unsupported required sections must be `Unknown` or a clear assumption. Do not invent content.

Every stored statement must be grounded in explicit user input, confirmed source memory, a user-provided file, accepted brainstorm idea memory, an explicit user-approved assumption, or `Unknown`.

Do not turn broad labels such as "I am a painter", "I need an app", or yes/no answers into complete prose. If support is partial, keep only the supported part and move the rest to `Unknown`, `Assumption:`, or Open Questions.

Preserve readable line breaks in stored section text: bullets each start on their own `- ` line; paragraphs are separated by newline characters; never flatten bullets or paragraphs into one inline string.

## Optional Ideation

Recommend one short ideation pass when context is thin, vague, generic, conflicted, or assumption-heavy. The user may decline.

Do not pass `required_techniques` or fixed `techniques` to `ssd-brainstorming`; let it select techniques.

Run at most one optional ideation pass unless the user explicitly asks for more. Use brainstorm memory handoff output as source material, not markdown paths.

## Review And User Validation Gate

Review the section payload before presenting it. Do not call product-brief review subagents.

Do not write while the payload has invented specificity, generic `why`/`problem`/`differentiation`, inference from vague answers, verbose thin-evidence prose, flattened formatting, missing audience or constraints without `Unknown`, source contradictions, or forbidden technical/PRD/MVP/roadmap/metrics/delivery/epic/story content.

Also verify the solution connects to the problem, positioning is clear, assumptions are explicit, open questions are useful, and every section is grounded in allowed evidence or `Unknown`.

Ask the user only for strategic choices: audience ambiguity, conflicting positioning, contradictory constraints, major assumption inclusion/removal, or multiple viable product directions.

After internal fixes, create flows run the create-only advanced elicitation validation gate; edits skip it.

Present the reviewed payload in human-readable Markdown and ask for approval or section-level changes. Creation shows every section. Editing shows a concise change summary and changed sections only, preferably before/after bullets or equivalent deltas, plus affected assumptions, open questions, or sources and an optional offer to see the full final document.

Approval prompt placement matters: show the complete create/edit review first, then put the approval/change instruction as the final paragraph. Discussion, clarification, or source selection is not approval.

Do not output only raw JSON, memory command output, or a tool result as the user-facing review. If the user requests changes, revise and repeat this gate.

## Memory Write

After internal review and explicit user approval, write Product Brief memory through `.opencode/scripts/ssd_product_brief/memory.py`.

Create command:

```text
python .opencode/scripts/ssd_product_brief/memory.py create
```

Update command:

```text
python .opencode/scripts/ssd_product_brief/memory.py update
```

Pass the JSON payload on stdin:

```json
{
  "change_summary": "brief explanation of why the brief changed",
  "sections": {
    "why-this-exists": "...",
    "product-definition": "...",
    "problem": "...",
    "high-level-solution": "...",
    "audience": "...",
    "necessity-and-differentiation": "...",
    "positioning": "...",
    "practical-constraints": "...",
    "assumptions": "...",
    "open-questions": "..."
  },
  "cited_brainstorm_ids": [],
  "cited_idea_ids": []
}
```

The adapter stores current `Artifact` and `ArtifactSection` memory with provenance relationships for cited brainstorms and ideas.

Do not create Product Brief markdown or temp markdown drafts.
