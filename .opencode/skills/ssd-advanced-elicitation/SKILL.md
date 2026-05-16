---
name: ssd-advanced-elicitation
description: Refine current or supplied content with BMAD advanced elicitation methods without writing artifacts.
---

# ssd-advanced-elicitation

Use when current or supplied content needs deeper critique, reconsideration, or refinement. This skill is pull-anytime and non-durable: it returns enhanced content to the conversation or invoking skill, and writes no files.

## Inputs

```json
{
  "run_mode": "interactive|internal",
  "target_content": "required unless recent content is obvious",
  "goal": "optional refinement goal",
  "initial_context": "optional supporting context",
  "constraints": [],
  "methods": [{"method_name": "optional exact method name", "purpose": "optional caller purpose"}],
  "required_methods": "optional integer"
}
```

Defaults: `run_mode=interactive`, `required_methods=1` in internal mode. If `target_content` is missing in interactive mode, ask only for the content to refine. If it is missing in internal mode, return `needs_input`.

## Method Catalogue

- Read `.opencode/skills/ssd-advanced-elicitation/methods.md` before selecting or applying methods.
- Preserve catalogue `category`, `method_name`, `description`, and `output_pattern` exactly as written.
- Do not add, infer, or expose catalogue fields such as `covers`, `action`, aliases, tags, or normalized names.
- Execute methods using only their preserved `description` and `output_pattern`, plus caller purpose when supplied.

## Internal Mode

- Do not present menus, method lists, reshuffles, or confirmation gates.
- If `methods` includes exact method names from the catalogue, use those methods.
- If no usable method is supplied, call `ssd_elicitation_selector` with `target_content`, `goal`, `initial_context`, `constraints`, `required_methods`, and `methods` as `preselected_methods`.
- Apply the selected method or methods immediately to the current enhanced content.
- Return the enhanced content to the caller.

## Interactive Mode

Select 5 context-fit methods by analyzing content type, complexity, stakeholder needs, risk level, and creative potential. Prefer exact user-requested method names when present. Balance method categories when no method is requested.

Present method names only:

```text
Advanced Elicitation Options

Choose a number (1-5), [r] Reshuffle, [a] List All, or [x] Proceed:

1. <Method Name>
2. <Method Name>
3. <Method Name>
4. <Method Name>
5. <Method Name>
r. Reshuffle the list with 5 new options
a. List all methods with descriptions
x. Proceed / No Further Actions
```

Response handling:

- `1-5`: apply the selected method to the current enhanced content, show the proposed refinement, ask whether to apply it, then re-present the same options.
- `r`: present 5 different context-fit methods.
- `a`: list all methods compactly with descriptions and allow selection by name or number.
- `x`: complete and return the current enhanced content.
- Direct feedback: apply the user's requested adjustment, then re-present options.
- Multiple numbers: execute selected methods in sequence, asking before applying each proposed refinement, then re-present options.

Only accepted refinements become the current enhanced content. Rejected refinements are discarded.

## Result

Return concise structured output:

```json
{
  "status": "complete|needs_input|cancelled",
  "skill_run": "ssd-advanced-elicitation",
  "methods_used": ["Socratic Questioning"],
  "enhanced_content": "<enhanced content returned to caller>",
  "notes": []
}
```

## Hard Stops

- Do not create raw files, final files, logs, or reviews.
- Do not edit source code, docs, temp files, final artifacts, sprint status, planning trackers, kanban state, or repository configuration.
- Do not modify the method catalogue during a run.
