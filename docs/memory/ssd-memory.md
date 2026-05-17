# ssd-memory Memory Contract

## Summary

- Unit: `ssd_memory`
- Unit type: `generic memory command`
- Source: `.opencode/scripts/ssd_memory/memory.py`
- Memory role: Creates, reads, updates, and lists generic Artifact memory; bootstraps and reads SQLite-backed ReferenceList memory from YAML seed files.
- Created memory contracts: `Artifact`, `ArtifactSection`, `ReferenceList`, `ReferenceItem`
- Used memory contracts: None
- Memory script: `.opencode/scripts/ssd_memory/memory.py`

## Creates Or Mutates

| Memory | Status | Action | Contract | Command / Step | Result |
| --- | --- | --- | --- | --- | --- |
| `Artifact` | `accepted` | `create`, `update` | `docs/memory.md` | `artifact create`, `artifact update` | Generic current-state Artifact root. |
| `ArtifactSection` | `current` | `create`, `replace` | `docs/memory.md` | `artifact create`, `artifact update` | Generic current Artifact sections. |
| `ReferenceList` | `active` | `create`, `update` | `docs/memory.md` | `reference bootstrap` | Stable reusable reference list root. |
| `ReferenceItem` | `active|deprecated` | `create`, `update`, `deprecate` | `docs/memory.md` | `reference bootstrap` | Stable reusable reference list item. |

## Creation Details

| Created Memory | Input / Source | Stored As | Required | Rule |
| --- | --- | --- | --- | --- |
| `ReferenceList.list_key` | YAML `list_key` | `field` | `yes` | Slug-normalized stable semantic lookup key. |
| `ReferenceList.title` | YAML `title` | `field` | `yes` | Human-facing title. |
| `ReferenceList.description` | YAML `description` | `field` | `no` | Defaults to empty string. |
| `ReferenceList.seed_version` | YAML `seed_version` | `field` | `no` | Defaults to `1`. |
| `ReferenceItem.item_key` | YAML item `item_key` | `field` | `yes` | Slug-normalized stable semantic lookup key within list. |
| `ReferenceItem.name` | YAML item `name` | `field` | `yes` | Human-facing selectable value. |
| `ReferenceItem.title` | YAML item `title` or `name` | `field` | `yes` | Graph display title. |
| `ReferenceItem.status` | YAML item `status` or deprecation rule | `field` | `yes` | Defaults to `active`; removed managed items become `deprecated`. |
| List-specific item fields | YAML item keys | `field` | `no` | Stored as flat properties when provided. |
| `HAS_ITEM` | bootstrap | `relationship` | `yes` | Connects `ReferenceList` to each managed `ReferenceItem`. |

## Creation Rules

- Idempotency: `reference bootstrap` upserts by `ReferenceList.list_key` and `(list_key, item_key)`.
- Mutability: changed YAML entries update graph properties while preserving UUIDs.
- Deletion behavior: removed managed YAML entries are marked `deprecated`, not deleted.
- Evidence requirement: not_required for seeded reference data.
- Missing input behavior: block on missing YAML, missing `list_key`, missing `title`, empty `items`, missing item `item_key`, or missing item `name`.

## Uses Memory

| Memory Dependency | Status | Contract / Owner | Command / Access | Required | Purpose | Missing / Stale Behavior |
| --- | --- | --- | --- | --- | --- | --- |
| None | None | None | None | no | This generic adapter owns the memory it creates and reads. | None |

## Non-Owned Boundaries

- Unit-specific artifact adapters own their concrete Artifact section contracts.
- Reference list consumers use semantic `reference bootstrap` and `reference get` commands; they do not read YAML seed files directly at runtime.
- Raw graph queries remain admin/debug only.

## Returned Memory References

| Output Field | Reference Type | Source Memory | Meaning |
| --- | --- | --- | --- |
| `list_id` | `id` | `ReferenceList` | UUID for the reference list root. |
| `list_key` | semantic key | `ReferenceList` | Stable list lookup key. |
| `item_ids[]` | `id` | `ReferenceItem` | UUIDs for bootstrapped active seed items. |
| `reference_list` | object | `ReferenceList` | Current reference list root properties. |
| `items[]` | object | `ReferenceItem` | Current items, excluding deprecated items unless requested. |

## Invariants

- Reference list node IDs and item node IDs are opaque UUIDs.
- `ReferenceList.list_key` and `ReferenceItem.item_key` are stable semantic lookup values.
- `reference get` excludes deprecated items by default.
- `reference bootstrap` validates that the requested `--list-key` matches the seed file `list_key`.

## Gaps

| Gap | Affects | Status | Source | Notes |
| --- | --- | --- | --- | --- |
| Nested reference item values | `ReferenceItem` | deferred | `docs/memory.md` | Current command stores flat YAML item properties only. |
