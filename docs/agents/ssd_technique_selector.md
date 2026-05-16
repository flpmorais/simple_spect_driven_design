# Agent Template

## Summary

- Name: `ssd_technique_selector`
- Description: Selects and resolves SSD brainstorming techniques from the catalogue, returning only facilitation actions.
- Mode: subagent

## Purpose

Reads the SSD brainstorming techniques catalogue, resolves caller-provided technique selections, adds missing techniques when required, and returns a compact facilitation technique set. It does not brainstorm ideas or write files.

## When To Use

Use when an SSD brainstorming flow needs techniques selected or normalized against `.opencode/skills/ssd-brainstorming/techniques.md` before facilitation.

Do not use when the task is to brainstorm ideas, write files, run shell commands, or execute the selected techniques.

## How It Is Used

Callers invoke it as a subagent with JSON input containing a brainstorming goal, scope, optional context and constraints, required technique count, optional excluded technique names, and any preselected techniques. The agent reads the catalogue, matches exact names first, falls back to safe catalogue matches using category, `Fit`, and `Action`, adds fitting catalogue techniques when needed, or creates conservative custom techniques when no safe match exists. Returned `action` values are facilitation instructions for user-led ideation, not autonomous generation commands.

## Inputs

- `goal`: Required. Brainstorming purpose.
- `scope`: Required. One of `quick`, `normal`, or `deep`.
- `initial_context`: Optional. Seed context string.
- `constraints`: Required. Constraint array.
- `required_techniques`: Required. Number of techniques required.
- `excluded_techniques`: Optional. Technique names to avoid during selection or shuffle.
- `preselected_techniques`: Required. Array of technique objects with `name` and caller `purpose`.

## Outputs

Returns JSON only with:

- `status`: `complete` or `blocked`.
- `techniques`: Compact array of selected technique objects.
- `warnings`: Warning array.
- `name`: Technique name.
- `category`: Technique category.
- `caller_purpose`: Caller purpose or `null`.
- `catalogue_purpose`: Catalogue purpose or `null`.
- `covers`: Coverage tag array.
- `action`: Facilitation action.
- `source`: `caller_matched_catalogue`, `selector_added`, or `custom`.

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

Can read files and use glob or grep search to inspect the techniques catalogue.

Cannot run shell commands, edit files, delegate tasks, write todos, fetch or search the web, use LSP tools, or use skills.

## Invocation

Invoke as a subagent with JSON input describing the brainstorming goal, desired scope, constraints, required technique count, and any preselected techniques.

Expected response: JSON only containing `status`, `techniques`, and `warnings`.

## Related Files

- Source agent: `.opencode/agents/ssd_technique_selector.md`
- Related skill: `.opencode/skills/ssd-brainstorming/techniques.md`
- Target artifact: None.

## Notes

- Always reads the catalogue before selecting.
- Ensures the final set includes challenge, risk, assumption, failure, or critique coverage.
- Rewrites catalogue action patterns into facilitation instructions that ask up to 3 prompts, allow optional AI seed suggestions, and require user input or approval before capture.
- Supports technique shuffling by preserving fixed preselected techniques while avoiding `excluded_techniques` when filling remaining slots.
- Returns `blocked` only if the catalogue cannot be read or no usable technique set can be produced.
