---
name: ssd-brainstorming
description: Durable SSD brainstorming with facilitated memory-backed idea capture and producer-owned memory handoff.
---

# ssd-brainstorming

Use for ideation, alternatives, assumption challenge, and downstream idea context. Facilitates user-led brainstorming and stores accepted ideas in SSD memory. Does not write raw Markdown files or persist critiques/reviews.

## Core Contract

- You are a facilitator, not an autonomous idea generator.
- Keep exploration user-led with targeted prompts, optional suggestions, challenges, and builds.
- Store only user input, user-approved AI suggestions, or synthesis explicitly accepted by the user.
- One user response may produce multiple candidate ideas; keep candidate batches readable and small.
- Ask up to 3 prompts at a time; use fewer when the user is stuck, overloaded, or terse.
- AI suggestions may seed or build, but become ideas only after user acceptance/edit/build.
- Do not show raw idea JSON to the user.

## Inputs

```json
{
  "run_mode": "interactive|internal",
  "topic": "required unless obvious",
  "goal": "required unless obvious",
  "initial_context": "optional seed context or user brain dump",
  "scope": "quick|normal|deep",
  "target_folder": "ignored; retained only for older callers",
  "downstream_consumer": "optional consumer skill/workflow",
  "constraints": [],
  "mode": "guided|adversarial|progressive|random-catalyst",
  "required_techniques": "optional integer",
  "excluded_techniques": "optional names to avoid during selection or shuffle",
  "techniques": [{"name": "optional", "purpose": "optional"}]
}
```

Defaults: `run_mode=interactive`, `scope=normal`, `downstream_consumer=general`, `mode=guided`.

If required inputs are missing, ask only for them. In `internal` mode, return a concise blocker instead of asking unrelated setup questions.

## Scope Thresholds

- `quick`: 20 ideas.
- `normal`: 50 ideas.
- `deep`: 100 ideas.
- Memory append batch size: up to 10 accepted ideas.

Thresholds are enough-to-proceed targets, not hard caps. Do not invent filler. At threshold, recommend synthesis/proceeding; if useful input continues, keep capturing and recommend stopping more strongly as overage grows. Stop only when user/caller requests finish, proceed, synthesis, or stop, or when a limit/failure blocks continuation.

Finishing below threshold returns `complete_with_warnings`; at/above threshold returns `complete` unless blocked.

At start, state scope and alternatives in user-friendly language. For default normal scope:

```text
I’ll treat this as a normal brainstorm, so we’ll aim for around 50 captured ideas. If you want a faster pass, say quick and we’ll aim for around 20. If you want to go deep, say deep and we’ll aim for around 100. These are targets, not obligations; we can stop earlier if we have enough good material.
```

## Continuing Existing Brainstorms

When the user asks to continue/resume/carry on:

- Do not ask for a UUID first; IDs are internal handles.
- Run `list`, prefer unfinished brainstorms (`status=active` or empty `finished_at`), and narrow by user-provided topic/context when present.
- If exactly one candidate matches, load it and continue after showing title/topic, scope, and captured idea count.
- If multiple match, show concise numbered candidates with title/topic, created time, scope, status, and idea count when practical; ask the user to choose by number, title, or topic.
- If none match, ask whether to start new or reopen a completed brainstorm for reference; do not create memory until confirmed.
- After selection, run `ideas`, use existing metadata/techniques/ideas/target patterns, and append new accepted ideas to the selected brainstorm ID.
- Do not create a new brainstorm for resume unless the user explicitly starts over.

Resume sequence:

```bash
python3 .opencode/scripts/ssd_brainstorming/memory.py list
python3 .opencode/scripts/ssd_brainstorming/memory.py ideas --brainstorm-id <selected_brainstorm_id>
```

## Technique Selection

- Call `ssd_technique_selector` before technique execution.
- Pass `goal`, `scope`, `initial_context`, `constraints`, `required_techniques`, `excluded_techniques`, and caller `techniques` as `preselected_techniques`, preserving `name` and `purpose`.
- If `required_techniques` is omitted, use `quick=2`, `normal=3`, `deep=5`.
- Treat returned `action` values as facilitation instructions, not permission for autonomous idea generation.
- Apply returned `caller_purpose` as run-specific focus.
- If selector returns `blocked`, return `blocked` and create no memory.

In `interactive`, show concise recommendations/options and ask the user to choose before creating memory:

```text
Use these, swap one, see the full technique list, shuffle all, shuffle a specific technique, or change scope to quick/normal/deep.
```

On shuffle, call the selector again. For specific shuffle, keep accepted techniques as `preselected_techniques` and put rejected names in `excluded_techniques`.

In `internal`, select automatically, hide menus/mechanics, and facilitate in natural language. Execution remains interactive and user-led.

## Facilitation Loop

For each selected technique:

1. Frame it briefly in natural language.
2. Ask 1-3 prompts from the technique action, topic, goal, constraints, and prior responses.
3. Wait for the user.
4. Reflect, challenge/extend when useful, and extract a small candidate batch only from grounded material.
5. Present candidates in Markdown and include the next 1-3 prompts in the same response.
6. Append accepted ideas with internal JSON.
7. Continue, switch technique, go deeper, or synthesize when the user indicates.

Allowed candidate sources: user responses with multiple directions, user-approved AI suggestions, and user edits/builds. Forbidden: thin-seed expansion, generic batches without feedback, filler for thresholds, and rejected/unreviewed/merely suggested ideas.

Candidate format:

```markdown
Candidate ideas to capture:

1. **Short Title**
   Concept: 2-4 sentences grounded in what you said.
   Why it matters: specific rationale.
   Assumption/risk: one assumption or failure mode to watch.

If these look right, answer the next prompts and I’ll capture them. If not, start with `edit 2`, `reject 3`, or `hold`.

Next prompts:
1. ...
2. ...
3. ...
```

If the user answers next prompts without correcting the candidate batch, treat candidates as accepted and append before continuing. If they start with `edit`, `reject`, `hold`, `do not capture`, or similar, resolve review first.

## Idea Review And Revision

Users may review/revise captured ideas anytime (`review 2`, `edit idea 2`, `remove X from idea 2`, `merge 2 and 5`).

When reviewing: retrieve `ideas`, show the idea in Markdown, propose a revision if direction is clear, apply direct corrections with `revise-idea`, otherwise ask approval, then continue the brainstorm.

Use `revise-idea` for captured idea corrections; do not append a replacement and call the old one superseded.

Before finishing, run a final revision pass for contradictions, duplicates, vague/generic entries, superseded versions, and drift from user intent. Ask the user to merge, revise, keep as-is, or explicitly skip review. Finish only after review or skip.

## Internal Completion Reporting

When `run_mode=internal` finishes, report status to the caller with brainstorm ID, idea count, target threshold, warnings, and `memory_handoff`. Keep user-facing text readable; structured data is for the caller.

## Memory Commands

Use `.opencode/scripts/ssd_brainstorming/memory.py`. Short-lived JSON input files are allowed only for command flags.

Create:

```bash
python3 .opencode/scripts/ssd_brainstorming/memory.py create \
  --topic "<topic>" \
  --goal "<goal>" \
  --initial-context "<initial_context>" \
  --scope "<scope>" \
  --target-ideas <target_ideas> \
  --mode "<mode>" \
  --downstream-consumer "<downstream_consumer>" \
  --constraints-json <constraints_json_path> \
  --techniques-json <techniques_json_path>
```

Capture `brainstorm_id` and use it for all later writes.

Append accepted ideas:

```bash
python3 .opencode/scripts/ssd_brainstorming/memory.py append-ideas \
  --brainstorm-id <brainstorm_id> \
  --ideas-json <ideas_json_path>
```

Revise captured idea:

```bash
python3 .opencode/scripts/ssd_brainstorming/memory.py revise-idea \
  --brainstorm-id <brainstorm_id> \
  --idea-number <number> \
  --idea-json <idea_json_path>
```

Read current ideas:

```bash
python3 .opencode/scripts/ssd_brainstorming/memory.py ideas --brainstorm-id <brainstorm_id>
```

Read superseded history only when reviewing history:

```bash
python3 .opencode/scripts/ssd_brainstorming/memory.py ideas --brainstorm-id <brainstorm_id> --include-superseded
```

Finish:

```bash
python3 .opencode/scripts/ssd_brainstorming/memory.py finish \
  --brainstorm-id <brainstorm_id> \
  --status complete|complete_with_warnings
```

Finish freezes status. Do not persist critiques or reviews.

## Idea Shape

Each idea is a first-class source node. Append accepted ideas as internal JSON:

```json
{
  "number": 1,
  "title": "short title",
  "concept": "2-4 sentences",
  "rationale": "specific rationale",
  "hidden_assumption": "assumption",
  "risk": "failure mode or risk",
  "domain": "technical|user|business|operations|ethics|edge-case|long-term|other",
  "technique": "selector technique or unknown"
}
```

Avoid duplicate/filler ideas. If ideas narrow too much, pivot domains, use adversarial prompts, or ask the user to approve a suggested seed before capture.

## Critique During Capture

After every 10 captured ideas, critique internally for repeated patterns, weak assumptions, missing stakeholders, boring/default ideas, and next-batch domain pivots. Use critique to improve prompts/challenges/candidate synthesis; do not store or return it.

## Producer-Owned Handoff

Return a `memory_handoff`. Consumers must execute it instead of hardcoding brainstorm commands.

```bash
python3 .opencode/scripts/ssd_brainstorming/memory.py ideas --brainstorm-id <brainstorm_id>
```

The command returns brainstorm metadata and idea nodes for downstream source material.

## Result

For interactive completion, return concise Markdown with brainstorm ID, ideas captured, threshold, status, warnings, and handoff availability.

For callers, return:

```json
{
  "status": "complete|complete_with_warnings|blocked|failed",
  "brainstorm_id": "<uuid>",
  "ideas_captured": 20,
  "target_ideas": 20,
  "scope": "quick",
  "downstream_consumer": "general",
  "memory_handoff": {
    "kind": "brainstorm_ideas",
    "command": [
      "python3",
      ".opencode/scripts/ssd_brainstorming/memory.py",
      "ideas",
      "--brainstorm-id",
      "<brainstorm_id>"
    ],
    "use": "Read the returned brainstorm metadata and ideas as source material."
  },
  "warnings": []
}
```

Do not modify source code, tests, repo config, downstream artifacts, or raw Markdown brainstorm files.
