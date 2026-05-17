# Wiki How-To

This document gives machine-optimized instructions for changing the SSD SvelteKit wiki: route decisions, custom page decisions, memory-contract updates, registry changes, navigation changes, and examples. For the wiki's purpose, source-of-truth rules, architecture boundaries, baseline routes, and page categories, see [../wiki.md](../wiki.md).

## Prime Directive

Follow `docs/wiki.md`: graph memory is canonical, graph access is server-side, and page rendering is read-only.

## Change Checklist

When memory changes, update the wiki only where the read/view contract changed.

Check in this order:

1. Graph read adapter: does the wiki need new data or a changed query?
2. View model: does the page data shape need a new field or type?
3. Registry: does an artifact/entity need a custom page mapping?
4. Route: is there a new URL shape, or can an existing route load it?
5. Component/view: does presentation need to change?
6. Navigation: should the new entity appear in graph-derived nav?

Prefer changing adapters and view models over adding routes.

## Route Decision Rule

Add a route only when the URL model changes.

Do not add a route just because memory gained fields.

Use existing route classes when possible:

```text
artifact current state      -> /artifacts/:kind
reference list              -> /lists/:listKey
generic node/entity         -> /nodes/:id
entity collection           -> existing index if group already exists
```

Add a new route when:

- the entity is not an artifact and deserves a stable top-level collection;
- the page has its own identity outside artifact kind or node ID;
- the URL needs extra path parameters that existing routes cannot express;
- navigation needs a distinct section with index/detail pages.

Do not add a route when:

- the default artifact page can display the data;
- only layout/presentation changes are needed;
- only a new artifact kind exists;
- a generic node detail page is enough.

## Custom Page Decision Rule

Use the default artifact page unless custom presentation materially improves comprehension.

Default artifact page is enough when the artifact can be read as:

```text
metadata + ordered sections + related nodes
```

Add a custom artifact page when:

- sections need domain-specific grouping;
- related graph nodes need first-class placement;
- the artifact combines current content, upstream inputs, and downstream outputs;
- users need comparison, status, provenance, or traceability beyond a section list.

Custom artifact page wiring:

```text
graph adapter function -> typed view model -> Svelte view -> artifact page registry entry
```

Do not put graph queries or memory semantics in the Svelte component.

## Memory Change Handling

When a memory adapter adds or changes nodes, edges, properties, or commands, map the change to wiki layers.

### New Artifact Kind

If a new artifact kind is stored through the existing artifact model:

```text
Artifact
ArtifactSection
```

Required wiki changes:

- none, if generic artifact rendering is enough;
- optional registry entry plus custom view, if presentation needs specialization;
- optional navigation label/title tuning, if default display is unclear.

Do not add a route for each artifact kind. Use `/artifacts/:kind`.

### New Artifact Field

If the graph adds an artifact property or section field:

- update graph read adapter if the field is not already returned;
- update the artifact view model type;
- update generic/custom views only if the field should be visible;
- do not add a route.

### New Relationship

If memory adds a relationship between existing nodes:

- update related-node query or relationship summary;
- expose it in the relevant view model;
- render it in generic detail pages by default;
- add custom rendering only if the relationship is central to the page.

### New Entity Label

If memory adds a non-artifact entity label:

- generic `/nodes/:id` should display it without custom work;
- add navigation grouping only if users need to browse the label as a collection;
- add index/detail routes only if generic node browsing is not enough.

### Reference Lists

If memory adds `ReferenceList` and `ReferenceItem` nodes:

```text
ReferenceList collection -> /lists
ReferenceList detail     -> /lists/:listKey
ReferenceItem detail     -> /nodes/:id
```

Required wiki changes:

- add or update a server-only reference list graph adapter;
- add `ReferenceListSummary`, `ReferenceItemSummary`, and `ReferenceListDetailView` view models;
- include `Lists` in primary navigation;
- include a graph-derived `Lists` navigation section;
- keep item detail browsing on `/nodes/:id` unless a separate item route is explicitly needed.

Do not add `/lists/:listKey/:itemKey` by default. Use the generic node page for item inspection.

### Changed Memory Contract

If memory command output changes:

- update the server-only graph adapter first;
- keep route and component contracts stable where possible;
- adapt raw command JSON into the existing view model shape;
- change components only when the user-facing page data changes.

## Product Brief Example

Scenario:

```text
Product Brief becomes memory-backed as an artifact.
It also consumes upstream brainstorm memory.
```

Route decision:

```text
Use /artifacts/product-brief.
Do not add /product-brief unless there is a separate URL identity requirement.
```

Default page decision:

```text
Use GenericArtifact if ordered sections and related nodes are enough.
Add ProductBrief view if upstream brainstorms, decisions, or derived outputs need a domain-specific layout.
```

Required changes if generic page is enough:

```text
memory writes Product Brief as Artifact
artifact list/get returns Product Brief
wiki generic artifact page renders it automatically
no route change
no registry change
```

Required changes if custom page is needed:

```text
add ProductBrief view model fields in graph adapter
add ProductBrief.svelte view
register product-brief -> ProductBrief
keep route /artifacts/:kind
```

Upstream brainstorm consumption:

```text
memory must expose relationships from Product Brief to brainstorm/source nodes
wiki adapter reads those relationships
ProductBrief view model includes upstreamSources or relatedBrainstorms
ProductBrief.svelte renders them
```

Do not encode brainstorm semantics inside the Product Brief component. Render the graph-derived relationship summary and link to the brainstorm page.

## Brainstorm Example

Scenario:

```text
Brainstorm memory exists as non-artifact graph entities.
Product Brief links to one or more brainstorms as sources.
```

Route decision:

```text
Use /brainstorms and /brainstorms/:id if brainstorms are a browsable collection.
Use /nodes/:id if only low-level inspection is needed.
```

Product Brief page behavior:

```text
show linked brainstorms as upstream sources
link each source to /brainstorms/:id when the route exists
fallback to /nodes/:id otherwise
```

Brainstorm page setup:

```text
brainstorm graph adapter -> BrainstormDetailView -> Brainstorm.svelte -> /brainstorms/:id
```

Keep detailed brainstorm contract rules in brainstorm memory docs, not wiki docs.

## Registry Rules

Artifact page registry maps artifact kind to component. See `docs/wiki.md` for the conceptual registry role.

```text
product-brief -> ProductBrief
product-blueprint -> ProductBlueprint
missing mapping -> GenericArtifact
```

Registry responsibilities:

- choose presentation;
- provide fallback;
- keep mapping small and explicit.

Registry must not:

- query the graph;
- validate memory contracts;
- transform raw command output;
- own artifact business rules.

## View Model Rules

Server adapters return view models, not raw graph rows. See `docs/wiki.md` for the canonical view-model boundary.

Good:

```text
ArtifactDetailView.sections[].heading
ArtifactDetailView.related[].relationship
BrainstormDetailView.ideas[]
```

Avoid:

```text
row["a"]["properties"] in Svelte components
Cypher result objects in page data
Python command JSON passed directly to browser views
```

Include graph IDs when the page needs linking or provenance.

## Navigation Rules

Navigation is graph-derived. See `docs/wiki.md` for baseline navigation groups.

Update navigation only when a new browsable group or label should appear.

Examples:

```text
new artifact kind -> appears under Artifacts automatically
new brainstorm node -> appears under Brainstorms if brainstorm index exists
new Decision label -> add Decisions nav group only when users browse decisions directly
```

Do not maintain a hand-written list of individual artifacts.

## Testing Guidance

For wiki changes, verify the boundary that changed:

- adapter tests for command/query mapping;
- view model tests for shape changes;
- route load tests for URL/data behavior;
- component tests only for meaningful rendering logic.

Use fixture graph data or command-output fixtures. Do not rely on a developer's local memory database for deterministic tests.
