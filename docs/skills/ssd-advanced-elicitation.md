# ssd-advanced-elicitation

## Summary

- Name: `ssd-advanced-elicitation`
- Description: Refine current or supplied content with BMAD advanced elicitation methods without writing artifacts.

## Purpose

Provides pull-anytime critique, reconsideration, and refinement for current or supplied content using preserved BMAD advanced elicitation methods.

## When To Use

Use when current or recent content needs deeper critique, refinement, reconsideration, red-team-style improvement, Socratic review, first-principles review, pre-mortem review, or another advanced elicitation method.

Do not use when the goal is durable ideation, alternatives generation, or downstream idea-context creation; use `ssd-brainstorming` for that.

## How It Is Used

The skill reads the preserved method catalogue, selects or receives methods, applies them to the target content, and returns enhanced content to the conversation or invoking skill. It does not write files or produce raw artifacts.

## Inputs

- `run_mode`: Optional. `interactive` or `internal`.
- `target_content`: Required unless recent content is obvious.
- `goal`: Optional refinement goal.
- `initial_context`: Optional supporting context.
- `constraints`: Optional constraints.
- `methods`: Optional exact method selections with optional caller purpose.
- `required_methods`: Optional integer. Defaults to `1` in internal mode.

## Outputs

- `status`: `complete`, `needs_input`, or `cancelled`.
- `skill_run`: `ssd-advanced-elicitation`.
- `methods_used`: Method names used.
- `enhanced_content`: Enhanced content returned to the caller or conversation.
- `notes`: Additional concise notes.

## Defaults

- `run_mode=interactive`.
- `required_methods=1` in internal mode.
- Interactive mode presents 5 method names plus `r`, `a`, and `x` controls.
- Internal mode uses supplied exact methods or calls `ssd_elicitation_selector`; it does not present menus or confirmation gates.

## Paths

- Source skill: `.opencode/skills/ssd-advanced-elicitation/SKILL.md`.
- Method catalogue: `.opencode/skills/ssd-advanced-elicitation/methods.md`.

## Completion Criteria

Completes when the selected method or methods have been applied and the enhanced content is returned, or when an interactive user selects `x` to proceed.

Stops with `needs_input` when target content is unavailable in internal mode. In interactive mode, the skill asks only for the missing target content.

## Invocation

Invoke with `target_content` unless the current or recent content is obvious. In internal mode, pass exact `methods` when the caller wants a specific method; otherwise expect `ssd_elicitation_selector` to choose one compactly.

Expected caller behavior: apply returned enhanced content to any durable artifact if desired. This skill does not write artifacts itself.

## Related Files

- Source skill: `.opencode/skills/ssd-advanced-elicitation/SKILL.md`.
- Method catalogue: `.opencode/skills/ssd-advanced-elicitation/methods.md`.
- Related agent: `.opencode/agents/ssd_elicitation_selector.md`.
- Related skill: `ssd-brainstorming`.

## Notes

- BMAD method names, categories, descriptions, and output patterns are preserved exactly in the markdown catalogue.
- The catalogue intentionally does not add `covers`, `action`, aliases, tags, or normalized names.
- No raw logs, reviews, or final files are produced.
