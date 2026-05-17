# SSD Memory

This document defines what SSD memory is: storage, source-of-truth rules, current memory shapes, graph conventions, evidence, and lifecycle. For operational instructions on adding, using, linking, or changing memory, see [howto/memory.md](howto/memory.md).

## Purpose

SSD memory is the canonical SQLite-backed store for durable agent and skill state.

It stores:

- canonical structured memory objects;
- source nodes that can be cited by downstream artifacts;
- evidence and provenance for durable facts;
- queryable relationships between stored entities.

Markdown docs describe contracts. They are not the source of truth for runtime memory. Agents and skills read and write memory through semantic commands owned by the relevant unit.

## Contract Layers

`docs/memory.md` defines shared memory rules, graph conventions, and current node families.

`docs/memory/<unit>.md` defines unit-owned memory:

- concrete memory names and node labels;
- fields, metadata, defaults, and validation;
- lifecycle: create, update, append, finalize, derive, read;
- mutability rules;
- semantic commands and returned references;
- boundaries for memory the unit may read but not mutate.

Do not repeat unit-specific schemas here. If a memory object is owned by one unit, its concrete shape belongs in that unit contract.

## Non-Goals

- No vectors yet.
- No raw Cypher as the default agent interface.
- No inferred durable facts without evidence.
- No hidden memory writes without an explicit workflow step.
- No single universal artifact schema forced onto all memory.

## Storage

Database directory:

```text
.opencode/shared/memory/
```

Default database file:

```text
.opencode/shared/memory/ssd-memory.db
```

Memory scripts create the directory on init. Treat database files as runtime state.

Structured seed files for reusable reference lists live under:

```text
.opencode/shared/reference-data/
```

Seed files are human-maintained YAML. They define reusable list data such as profiles, brainstorming techniques, advanced elicitation methods, product classifications, and future SSD reference lists. Markdown may describe these lists for humans, but YAML seed files are the editable seed source. After bootstrap, the graph database is the runtime source for agents.

## Extension

Use `colliery-io/graphqlite`.

Why:

- SQLite-backed property graph.
- Cypher queries.
- Python package: `graphqlite`.
- Embedded, no server.
- Native nodes, relationships, labels, typed properties.

Agents call semantic script commands. GraphQLite and Cypher stay internal except admin/debug commands. See [howto/memory.md](howto/memory.md) for command-use rules.

## Memory Recipe Lookup

Memory recipes are token-lean operation manuals for stored memory objects. They let a skill discover producer-owned browse and load commands without reading memory scripts or hardcoding another unit's adapter details.

Recipe index:

```text
.opencode/shared/recipes.md
```

Memory recipes:

```text
.opencode/shared/recipes/<memory-object>.md
```

Rules:

- If a user supplies a file path as source material, read the file directly.
- If a user asks to include, load, browse, cite, inspect, or derive from a stored memory object, first read `.opencode/shared/recipes.md`.
- Read only the recipe for the memory object being used.
- Follow the recipe's semantic commands for browse, selection, load, and provenance.
- Run recipe delete commands only when the user explicitly asks to delete the specific stored memory object.
- Do not inspect memory scripts to discover commands unless the relevant recipe is missing, stale, or fails.
- Recipes document command usage only; memory schemas and lifecycle rules remain in `docs/memory/<unit>.md`.

## Current Memory Shapes

Memory is a property graph. Current documented memory uses these shared shapes.

### Current-State Artifact

`Artifact` is the shared abstract shape for durable, document-like SSD outputs.

Nodes:

| Node | Role |
| --- | --- |
| `Artifact` | Stable artifact root and current metadata. |
| `ArtifactSection` | Latest editable canonical section content. |

Relationships:

```text
(:Artifact)-[:HAS_CURRENT_SECTION]->(:ArtifactSection)
```

Rules:

- `Artifact` nodes hold stable identity and current metadata.
- Current section nodes hold latest canonical content.
- Updates replace current sections instead of storing history in SQLite.
- Provenance relationships attach to the current artifact root unless a unit contract states otherwise.

Concrete artifact kinds define their section keys, fields, validation, and commands in their owning memory contract.

### Brainstorm Memory

`ssd-brainstorming` owns non-versioned brainstorm memory.

Nodes:

| Node | Role |
| --- | --- |
| `Brainstorm` | Current brainstorm root and metadata. |
| `BrainstormIdea` | First-class accepted idea source node. |

Rules:

- Brainstorm memory is not a generic `Artifact`.
- Brainstorms are not versioned.
- Brainstorm ideas can be appended and revised while the brainstorm is active. Revisions preserve superseded history and expose latest versions by default.
- Finished brainstorms are immutable.
- Critiques and reviews are not stored.
- Consumers retrieve brainstorm data through the producer-owned handoff command.

The concrete schema is `docs/memory/ssd-brainstorming.md`.

### Reference Lists

Reference lists store reusable SSD catalogue data as first-class graph memory. They are not artifacts and are not brainstorm memory.

Nodes:

| Node | Role |
| --- | --- |
| `ReferenceList` | Stable root for one reusable list, such as profiles, methods, techniques, or product classifications. |
| `ReferenceItem` | One first-class item in a reference list. |

Relationships:

```text
(:ReferenceList)-[:HAS_ITEM]->(:ReferenceItem)
```

Rules:

- YAML files under `.opencode/shared/reference-data/` are the editable seed source.
- The graph database is the runtime/query source after bootstrap.
- Bootstrap is idempotent and may run before planner setup status is returned.
- Missing YAML entries create graph items.
- Changed YAML entries update graph items.
- Managed graph items removed from YAML are marked `deprecated`, not deleted.
- Agents consume reference lists through semantic commands once commands exist; they should not read YAML directly for runtime selection.
- Reference item node IDs are opaque UUIDs. Stable lookup values are stored in `ReferenceList.list_key` and `ReferenceItem.item_key`.
- List-specific fields are stored as flat properties when practical. Nested or repeated values may be serialized as JSON text when needed.

Initial list keys:

```text
profiles
product-classifications
brainstorming-techniques
advanced-elicitation-methods
```

Common `ReferenceList` properties:

```text
id
list_key
title
description
seed_version
status
created_at
updated_at
```

Common `ReferenceItem` properties:

```text
id
list_key
item_key
title
name
category
status
seed_version
created_at
updated_at
```

List-specific item properties are allowed. Examples include `definition`, `optimizes_for`, `fit`, `action`, `description`, `output_pattern`, `best_at`, `avoid_when`, and profile lens fields.

## Evidence

Trusted sources:

- explicit user decision;
- reviewed SSD artifact content;
- accepted architecture or planning decision;
- tool output captured by an approved workflow step;
- source nodes produced by a documented memory workflow.

Rules:

- Every durable factual relationship should cite evidence unless the unit contract marks evidence as not required.
- Do not turn speculation into accepted facts.
- Keep `proposed` distinct from `accepted`.
- Use `not_documented` or `unknown` when source material is missing.
- Source nodes must be retrievable by ID or producer-owned handoff command.

Evidence properties:

```text
evidence_id
source_kind
source_ref
source_section
source_quote
created_at
```

Status values:

```text
draft
active
proposed
accepted
complete
complete_with_warnings
superseded
deprecated
rejected
```

Unit contracts may narrow valid statuses.

## Graph Conventions

Node labels use `PascalCase`. Relationship types use `UPPER_SNAKE_CASE`. Properties use `snake_case`.

Node IDs are opaque UUIDs. Do not encode type, kind, section key, status, or human-readable names into IDs.

Every graph node must store a non-empty `title` property for human-facing identification in graph views, navigation, and relationship displays. Titles do not replace UUID node IDs for storage, routes, provenance, or relationship targets.

Store semantic identity and lookup values as properties:

```text
Artifact.kind
ArtifactSection.artifact_id
ArtifactSection.section_key
ReferenceList.list_key
ReferenceItem.list_key
ReferenceItem.item_key
```

Semantic commands resolve memory by meaningful fields such as `kind`, `section_key`, `list_key`, and `item_key`, then return UUID node IDs. Consumers must not construct IDs.

Human display names stay in properties.

Common relationship types:

```text
HAS_CURRENT_SECTION
HAS_ITEM
SUPPORTED_BY
DERIVED_FROM
CITES
CREATED_FROM
CONSUMES
CHOOSES
USES_PATTERN
APPLIES_TO
CHOSEN_BECAUSE
SUPPORTS
CONSTRAINS
SUPERSEDES
RELATED_TO
```

Use `RELATED_TO` only when no specific relationship fits.

## Lifecycle Rules

Artifact memory:

- stores the latest accepted state only;
- replaces current sections on update;
- returns enough references for downstream consumers to retrieve current canonical content;
- relies on Git, explicit exports, or future archival workflows for history outside SQLite.

Brainstorm memory:

- stores the latest state without revision history;
- only changes fields allowed by `docs/memory/ssd-brainstorming.md`;
- finish only changes brainstorm status and `finished_at`;
- must not be treated as versioned by consumers.

Reference list memory:

- is seeded from structured YAML before planner setup status when needed;
- stores reusable lists and items as first-class graph nodes;
- uses idempotent upsert by `list_key` and `(list_key, item_key)`;
- preserves opaque UUID node IDs and stores stable semantic keys as properties;
- marks removed managed items as `deprecated` instead of deleting them;
- is queryable by later agents through semantic commands.

Append-only brainstorm ideas:

- adds child/source nodes without rewriting existing content;
- appends only while the brainstorm is `active`;
- returns enough references for downstream consumers to retrieve created nodes.

Finished or historical memory:

- is not changed after creation except by explicit supersession or deprecation rules.

## Interfaces

Semantic commands are the public interface. Current scripts:

```text
.opencode/scripts/ssd_memory/memory.py
.opencode/scripts/ssd_brainstorming/memory.py
.opencode/scripts/ssd_product_brief/memory.py
```

Generic reference list commands:

```text
python .opencode/scripts/ssd_memory/memory.py reference bootstrap --list-key <list-key>
python .opencode/scripts/ssd_memory/memory.py reference get --list-key <list-key>
```

Raw graph access is admin/debug only. Normal agents use documented commands and returned handoff commands.
