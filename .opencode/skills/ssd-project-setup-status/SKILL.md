---
name: ssd-project-setup-status
description: Reads SSD setup memory status and identifies required setup work before planning continues.
---

# ssd-project-setup-status

Read current project setup state from SSD memory and explain what must happen before non-brainstorm planning continues.

This skill is read-only. It does not create, update, delete, or infer durable memory.

## Contract

Input:

```json
{
  "scope": "optional; auto or root; default auto"
}
```

Rules:

- Run the setup status memory adapter exactly once.
- Use `.opencode/scripts/ssd_project_setup/memory.py status --scope <scope>`.
- Do not run Product Brief, Product Blueprint, Architecture Blueprint, brainstorm, elicitation, or downstream planning skills.
- Do not inspect artifact-specific memory scripts.
- Do not create new memory nodes.
- If setup is incomplete, tell the user what must be done and that you need acceptance before the next setup skill runs.
- If setup is blocked, report the blocker and do not recommend continuing.

## Memory Command

```text
python .opencode/scripts/ssd_project_setup/memory.py status --scope auto
```

## Response Rules

When `status=complete`, return a concise setup summary and say non-brainstorm planning may continue.

When `status=incomplete` and `must_do` has one item, return:

- what setup artifact is missing;
- the exact skill that must run next;
- why it must run before other non-brainstorm planning;
- a clear acceptance question.

Use this style:

```text
Project setup is incomplete.

Must do next: create Product Brief.
Skill that will run after you accept: `ssd-product-brief-create`.
Reason: Product Brief memory is required before Product Blueprint or downstream planning work.

Do you want me to run `ssd-product-brief-create` now?
```

When `status=incomplete` and `must_do` has multiple items, list each required available branch and ask the user which one to run.

When `status=blocked`, report the blocker from `blocked_reason` and stop.

## Output Fields

Include these fields in the completion report:

```json
{
  "status": "complete|incomplete|blocked",
  "scope": {},
  "must_do": [],
  "available_next_steps": [],
  "blocked_steps": []
}
```

## Hard Stops

- Do not run the next setup skill inside this skill.
- Do not treat brainstorming as setup completion.
- Do not add roadmap or future artifacts unless the setup memory adapter returns them.
