# ssd_profile_analyzer

## Summary

- Name: `ssd_profile_analyzer`
- Description: Analyzes input through a caller-selected SSD profile lens and returns a structured opinion.
- Mode: subagent
- Source: `.opencode/agents/ssd_profile_analyzer.md`

## Purpose

Reads the shared SSD profile catalog, resolves a caller-selected profile by exact stable ID, reads the matched profile file, and analyzes supplied input through that profile as an analytical lens. It returns compact JSON and does not write files or select profiles.

## When To Use

Use when a skill needs an opinionated analysis of a proposal, artifact, decision, architecture, or content through a preselected profile from `.opencode/shared/profiles/catalog.md`.

Do not use when the caller needs automatic profile selection, file edits, shell commands, web research, or theatrical persona roleplay.

## How It Is Used

Callers invoke it as a subagent with JSON containing `profile_id`, `input`, optional analysis goal, optional context, constraints, and output mode. The agent reads the catalog, resolves the profile ID exactly, reads only the matched profile file, applies the profile as weighted evaluation criteria, and returns structured analysis JSON.

## Inputs

- `profile_id`: Required. Exact stable profile ID from `.opencode/shared/profiles/catalog.md`.
- `input`: Required. Proposal, artifact, decision, architecture, or content to analyze.
- `analysis_goal`: Optional. Caller-specific analysis goal.
- `context`: Optional. Supporting context.
- `constraints`: Optional. Constraint array; defaults to `[]`.
- `output_mode`: Optional. One of `opinion`, `risks`, `recommendation`, or `decision_review`; defaults to `opinion`.

## Outputs

Returns JSON only with:

- `status`: `complete`, `needs_input`, or `blocked`.
- `profile_id`: Resolved profile ID.
- `profile_name`: Resolved profile name.
- `analysis`: Structured profile-weighted analysis.
- `opinion`: Profile-weighted judgment.
- `confidence`: `low`, `medium`, or `high`.
- `bias_applied`: How the profile shaped the analysis.
- `bias_risk`: How the profile might distort the conclusion.
- `main_concerns`: Concerns raised by the profile lens.
- `supporting_arguments`: Evidence-based arguments from input and context.
- `counterarguments`: Conditions or arguments that weaken the profile-weighted view.
- `recommendations`: Practical next steps or decision guidance.
- `missing_facts`: Facts that would materially change the opinion.
- `warnings`: Warning array.

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

Can read files and use glob or grep search to inspect the profile catalog and matched profile file.

Cannot run shell commands, edit files, delegate tasks, write todos, fetch or search the web, use LSP tools, or use skills.

## Memory

- Status: none.
- Summary: The agent does not create, update, or consume SSD memory.
- Memory contract: `None`.

## Invocation

Invoke as a subagent with a valid `profile_id` and analyzable `input`.

Expected response: JSON only containing `status`, `profile_id`, `profile_name`, `analysis`, and `warnings`.

## Related Files

- Source agent: `.opencode/agents/ssd_profile_analyzer.md`.
- Profile catalog: `.opencode/shared/profiles/catalog.md`.
- Architect profiles: `.opencode/shared/profiles/architects/`.
- Memory contract: `None`.

## Notes

- Always reads the catalog before analyzing.
- Resolves profile IDs by exact match only.
- Uses profiles as analysis lenses, not personas.
- Does not claim personal experience, memories, authority, emotions, identity, or institutional background.
- Always includes `bias_applied`, `bias_risk`, and `counterarguments`.
- Returns `needs_input` only when analyzable input is missing.
- Returns `blocked` when the catalog or selected profile cannot be read or `profile_id` cannot be resolved.
