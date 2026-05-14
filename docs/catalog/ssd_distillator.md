# SSD Distillator

## Summary

- Name: `ssd_distillator`
- Description: Utility subagent that directly distills explicit source files into dense SSD context artifacts.
- Mode: subagent

## Purpose

Converts caller-provided source files into preservation-oriented, token-efficient distillates under `._ssd_docs_distil/` for downstream SSD agents and skills.

## When To Use

Use when explicit files need to be compressed into one durable SSD context artifact while preserving requirements, decisions, rationale, constraints, risks, scope, conflicts, and open questions.

Do not use when inputs require source discovery, directory or glob expansion, repo-root scans, multi-agent splitting, merge compression, delegated compression, planning, story, development, review, refactor, brainstorming, commits, or writes outside `._ssd_docs_distil/`.

## How It Is Used

The caller supplies explicit readable source file paths, an optional downstream consumer, optional token budget, optional output path under `._ssd_docs_distil/`, and audit settings. The agent validates inputs, reads sources, drafts the distillate directly, optionally audits it with `ssd_distillate_auditor`, writes one final file, measures token metrics, and returns a concise structured result.

## Inputs

- `source_documents`: Required. Explicit readable file paths only; directories, globs, repo-root scans, and discovery-style inputs are rejected.
- `downstream_consumer`: Optional. Workflow, skill, or agent that will consume the distillate; defaults to `general`.
- `token_budget`: Optional. Approximate target token count.
- `output_path`: Optional. File path under `._ssd_docs_distil/`; if omitted, the agent derives a path for one source or asks for an output path when multiple sources lack an obvious topic or parent name.
- `audit`: Optional. Boolean audit flag; defaults to `true`.
- `max_fix_passes`: Optional. Maximum audit fix passes; defaults to `2`.
- `fail_on_audit_findings`: Optional. Boolean failure flag for remaining audit findings; defaults to `false`.

## Outputs

Returns one markdown distillate under `._ssd_docs_distil/` and a concise structured JSON-like result with:

- `status`: Completion state, `complete` or `failed`.
- `distillate`: Final distillate path.
- `source_documents`: Explicit source paths used.
- `source_total_tokens`: Measured source token count, or `0` in the failure response contract.
- `distillate_total_tokens`: Measured distillate token count, or `0` in the failure response contract.
- `compression_ratio`: Measured compression ratio, formatted like `N:1`.
- `audit_status`: `pass`, `pass_with_findings`, `failed`, or `skipped`.
- `fix_passes`: Number of audit fix passes used.
- `warnings`: Warnings or blocker details.

## Permissions

- `read`: allow
- `glob`: allow
- `grep`: allow
- `bash`: allow
- `edit`: allow under `._ssd_docs_distil/**`; deny elsewhere.
- `task`: allow
- `todowrite`: allow
- `webfetch`: deny
- `websearch`: deny
- `lsp`: deny
- `skill`: deny all skills

## Tools And Skills

Can read explicit source files, validate paths with allowed tools, write final distillates under `._ssd_docs_distil/**`, call `.opencode/agents/ssd_distillate_auditor.md` through `task` for preservation checks, and run `.opencode/scripts/ssd_distillator/measure_distillation.py` after the final distillate exists.

Cannot write outside `._ssd_docs_distil/**`, use web or LSP tools, use skills, call compressor helpers, call analyzer scripts, run source-discovery scripts as a fallback, or start unrelated workflows.

## Invocation

Invoke as a subagent with a JSON-like payload containing explicit `source_documents` and, when needed, `output_path`, `downstream_consumer`, `token_budget`, `audit`, `max_fix_passes`, and `fail_on_audit_findings`. The agent rejects directories, globs, repo-root scans, discovery-style inputs, and output paths outside `._ssd_docs_distil/`.

Expected response: concise structured result containing status, distillate path, source paths, token metrics, compression ratio, audit status, fix pass count, and warnings.

## Related Files

- Source agent: `.opencode/agents/ssd_distillator.md`.
- Related skill: None.
- Target artifact: `._ssd_docs_distil/` markdown distillate.
- Auditor helper: `.opencode/agents/ssd_distillate_auditor.md`.
- Metrics script: `.opencode/scripts/ssd_distillator/measure_distillation.py`.

## Notes

- Produces exactly one distillation result per invocation.
- Performs preservation-oriented compression, not mathematical losslessness or general summarization.
- Does not perform source discovery, multi-agent splitting, merge compression, delegated compression, commits, planning, story, development, review, refactor, or brainstorming workflows.
