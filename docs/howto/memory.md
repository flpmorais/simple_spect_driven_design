# Memory How-To

Machine-optimized instructions for adding, using, linking, creating, or changing SSD memory. For memory concepts, current node families, graph conventions, evidence rules, lifecycle rules, and script paths, see [../memory.md](../memory.md). Unit contracts live in `docs/memory/<unit>.md`.

## Prime Directive

Use existing memory shapes first.

Current shapes:

- `Artifact`: durable document-like outputs.
- `Brainstorm`: brainstorm runs and accepted ideas.

Add nodes, relationships, commands, or routes only when current contracts cannot represent the needed durable state or provenance.

## Decision Order

For any requested memory change, decide in this order:

1. Is this durable? If no, do not store in memory.
2. Is it a document-like SSD output? Use `Artifact`.
3. Is it brainstorm run state or accepted ideas? Use `Brainstorm` / `BrainstormIdea`.
4. Is it only a new section/field of an existing artifact? Update that unit contract only.
5. Is it only consumption of existing memory? Add dependency/use docs and read command use; do not create nodes.
6. Is a new durable object with independent lifecycle required? Add a new unit-owned memory contract.
7. Is a relationship needed for retrieval/provenance? Use an existing relationship type first.
8. Add new relationship type only if no current type is semantically correct.

## Add Artifact Memory

Use for durable document-like SSD outputs.

Required docs:

- Add or update `docs/memory/<owner>.md` from `docs/templates/memory-template.md`.
- Reference shared `Artifact` schema; do not restate all shared nodes.
- Define artifact kind, section keys, required fields, defaults, validation, commands, outputs.

Do not add new nodes for artifact sections. Add `ArtifactSection` entries with new section keys.

## Use Existing Memory

When a unit consumes memory it does not own:

- document it in `Uses Memory` only;
- call producer-owned semantic command or handoff command;
- do not hardcode another unit's graph traversal unless that contract exposes it;
- do not duplicate consumed memory shape;
- record missing behavior: `block`, `warn`, `skip`, or `regenerate`.

Use returned memory references, not Markdown paths.

## Link Memory

Use relationships for durable traceability, not temporary execution flow.

Default relationship choices:

```text
DERIVED_FROM  generated from prior durable content
CITES         cites source node as evidence/provenance
CONSUMES      workflow read dependency
SUPPORTED_BY  fact supported by evidence/source
SUPERSEDES    replacement relationship
RELATED_TO    last resort only
```

Relationship rules:

- Link to source nodes when downstream memory depends on accepted ideas or captured outputs.
- Link to `Artifact` when downstream memory depends on current artifact content.
- Link to `BrainstormIdea` when an idea influenced output content.
- Link to `Brainstorm` when only run-level provenance matters.
- Add evidence properties or an `Evidence` node when storing accepted durable facts.

## Add New Nodes

Add a new node label only when all are true:

- current `Artifact` or `Brainstorm` shapes cannot represent the object;
- the object has durable identity;
- it has lifecycle or query needs independent from its parent;
- consumers need to retrieve or link to it directly.

Do not add a node for:

- one more artifact section;
- one more metadata field;
- transient intermediate reasoning;
- display-only grouping;
- data already returned by a producer-owned command.

New node setup:

```text
1. define owner unit
2. add docs/memory/<owner>.md
3. define label, UUID id behavior, lookup fields, status values
4. define lifecycle and mutability
5. define semantic commands
6. define returned references
7. define allowed relationships
8. update readers/wiki only if read shape changes
```

## Add New Relationships

Add a relationship type only when existing types are misleading.

Before adding, test against defaults:

```text
source/provenance -> CITES or DERIVED_FROM
read dependency   -> CONSUMES
evidence          -> SUPPORTED_BY
replacement       -> SUPERSEDES
generic link      -> RELATED_TO
```

New relationship setup:

```text
1. add type to docs/memory.md Graph Conventions
2. add usage rule to owner memory contract
3. define direction
4. define required properties/evidence
5. expose through semantic read command if consumers need it
```

## Change Memory

When changing an existing memory contract:

- preserve existing node labels and ID semantics unless changing them is the purpose of the work;
- add fields instead of changing meanings;
- document migration/backfill if stored data already exists;
- update semantic command input/output docs;
- update consumers that rely on changed output;
- preserve current-state retrieval behavior unless changing it is the purpose of the work.

Do not design IDs to be human-readable. Store readable or discriminating values in properties, and expose semantic commands that resolve by those properties.

If changing only docs or display, do not change memory.

## Product Brief Consumes Brainstorm

Goal: product brief uses brainstorm ideas as upstream sources.

Default answer:

```text
Product brief = Artifact
Brainstorm = existing source memory
BrainstormIdea = existing source nodes
No new nodes by default
```

Memory contract changes:

- Product brief contract creates/updates `Artifact` memory.
- Product brief contract uses `Brainstorm` via `memory_handoff.command` or documented brainstorm `ideas` command.
- Product brief contract records upstream source references returned by brainstorm memory.
- Product brief contract defines missing brainstorm behavior: usually `block` if required, `skip` if optional.

Relationships:

```text
(:Artifact {kind:'product-brief'})-[:DERIVED_FROM]->(:Brainstorm)
(:Artifact {kind:'product-brief'})-[:CITES]->(:BrainstormIdea)
```

Use `DERIVED_FROM` for run-level lineage. Use `CITES` for specific idea provenance. Do not add `ProductBriefBrainstorm` node unless the link itself has durable fields or lifecycle.

Artifact sections:

```text
why-this-exists
product-definition
problem
high-level-solution
audience
necessity-and-differentiation
positioning
practical-constraints
assumptions
open-questions
```

These are `ArtifactSection` rows, not new node labels.

Returned references:

```text
artifact_kind=product-brief
artifact_id=<uuid>
source_brainstorm_id=<uuid>
cited_idea_ids=[...]
```

## Command Use Rules

Normal agents:

- use semantic commands;
- use handoff commands returned by producer workflows;
- do not write raw Cypher;
- do not infer unstated durable facts;
- return memory IDs;
- run delete commands only when the user explicitly asks to delete the specific memory artifact.

Admin/debug only:

- raw graph query;
- schema inspection;
- migration checks.

## Required Doc Updates

For source changes that create/mutate/read memory:

- update typed doc: `docs/skills/<name>.md`, `docs/agents/<name>.md`, or `docs/commands/<name>.md`;
- update memory contract: `docs/memory/<name>.md`;
- update `docs/memory.md` only for shared shape, shared relationship, shared lifecycle, or shared convention changes;
- update `docs/howto/wiki.md` only if wiki read/view behavior changes.

## Stop Rules

Stop and ask when:

- durable vs transient state is unclear;
- owner unit is unclear;
- existing relationship type seems close but semantically wrong;
- changing stored IDs or meanings of existing fields;
- source material does not support an accepted fact.
