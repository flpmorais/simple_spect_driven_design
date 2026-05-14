# ssd_distillate_auditor

## Summary

- Name: `ssd_distillate_auditor`
- Description: Internal helper for `ssd_distillator`; adversarially audits source-to-distillate preservation.
- Mode: subagent

## Purpose

Adversarially compares original source documents against a produced distillate to find missing, weakened, distorted, or hallucinated information. It returns concrete findings and targeted fix bullets rather than rewriting the distillate.

## When To Use

Use when `ssd_distillator` needs an independent preservation audit of a draft distillate against source documents, especially to verify decisions, rationale, requirements, constraints, numeric details, risks, scope boundaries, open questions, conflicts, and other traceability-critical information.

Do not use when the task is to compress sources, rewrite the whole distillate, defend the distillate, edit files, access web content, run shell commands, or delegate work.

## How It Is Used

It reads every provided source document and the distillate, builds an independent inventory of source information, then checks whether the distillate preserves that information accurately. It ignores harmless wording differences and deliberate compression, but flags omissions, weakened details, changed meaning, missing rationale, missing numeric specificity, and unsupported additions.

## Inputs

- `source_document_paths`: Required. Paths to the original source documents to audit against.
- `draft_distillate`: Required. Draft distillate content or a file path to the draft distillate.
- `downstream_consumer`: Optional. Consumer context used to decide whether consumer-focused filtering is allowed.
- `consumer_focused_filtering_allowed`: Required. Whether omissions clearly irrelevant to the downstream consumer are allowed.

## Outputs

Returns JSON only, or a fenced `json` block if exact JSON is not possible, containing:

- `status`: `pass`, `pass_with_findings`, or `fail`.
- `findings`: preservation gaps with severity, source reference, impact, and suggested distillate bullet.
- `coverage_summary`: pass/gap/not-applicable coverage for key information categories.
- `audit_notes`: additional audit notes.

## Permissions

- `read`: allow
- `glob`: allow
- `grep`: allow
- `bash`: deny
- `edit`: deny for all files
- `task`: deny
- `todowrite`: deny
- `webfetch`: deny
- `websearch`: deny
- `lsp`: deny
- `skill`: deny for all skills

## Tools And Skills

Can perform read-only local inspection through `read`, `glob`, and `grep`.

Cannot run shell commands, edit files, delegate tasks, write todos, access the web, use LSP tools, or use skills.

## Invocation

Invoke as a subagent with original source document paths, the draft distillate content or path, optional downstream consumer context, and whether consumer-focused filtering was allowed.

Expected response: JSON only, with no conversational preamble; if exact JSON is not possible, a fenced `json` block and nothing else.

## Related Files

- Source agent: `.opencode/agents/ssd_distillate_auditor.md`.
- Related agent: `.opencode/agents/ssd_distillator.md`.
- Related skill: None.
- Target artifact: A provided draft distillate path or content.

## Notes

- Normally called only by `ssd_distillator` as an internal helper subagent.
- Assumes omissions exist until the distillate proves otherwise and does not defend or rewrite the distillate.
- Returns `pass` only when no high or medium preservation gaps remain.
- Returns `pass_with_findings` when only low findings remain, or when findings are acceptable because consumer-focused filtering was allowed.
- Returns `fail` when high or medium findings remain.
