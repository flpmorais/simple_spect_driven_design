# SSD Wiki

This document defines what the wiki is: purpose, source-of-truth rules, architecture boundaries, route model, and page categories. For instructions on changing the wiki when memory changes, adding routes, adding custom pages, or wiring examples such as Product Brief and Brainstorm, see [howto/wiki.md](howto/wiki.md).

## Purpose

The SSD wiki is a SvelteKit reading interface over SSD graph memory.

The graph is canonical. The wiki only projects graph data into navigation, indexes, detail pages, and type-specific views. It must not duplicate canonical state into Markdown, frontend state, generated pages, or cache files.

## Source

Default graph database:

```text
.opencode/shared/memory/ssd-memory.db
```

Wiki content must be recoverable from the graph. Deleting and recreating the wiki must not lose source data.

## Boundaries

- Read from the graph through server-side adapters.
- Keep database paths, GraphLite details, raw Cypher, and Python command details out of browser code.
- Prefer semantic read commands or a read-only service over direct SQLite table access.
- Do not write to the graph while rendering pages or navigation.
- Treat any future editing surface as a separate explicit workflow.

Runtime shape:

```text
SvelteKit server loaders
-> server-only graph read adapters
-> semantic graph reads
-> GraphLite SQLite database
```

Use only server-side modules for graph reads:

```text
+layout.server.ts
+page.server.ts
*.server.ts
```

## Navigation

Navigation is graph-derived, not hand-maintained.

Baseline groups:

```text
Home
Artifacts
Brainstorms
Lists
Graph
```

Additional groups may mirror graph labels such as `Decision`, `Technology`, `Pattern`, `Concern`, and `Constraint`.

Graph navigation and detail headings should display node `title` values first. UUID node IDs remain internal route keys and should be shown only where useful for diagnostics or provenance.

Navigation entries should use stable graph IDs or route-safe slugs.

## Routes

Baseline routes:

```text
/                         wiki home
/artifacts                artifact index
/artifacts/:kind          current artifact page
/brainstorms              brainstorm index
/brainstorms/:id          brainstorm page
/lists                    reference list index
/lists/:listKey           reference list page
/nodes/:id                generic node detail
/graph                    graph overview
```

Routes load view models server-side. Browser components do not query the graph.

## Page Types

### Index Pages

Index pages list graph entities by type or group. They show selection metadata such as title, kind, status, timestamps, and relationship counts.

### Generic Detail Pages

Generic detail pages make any graph node browsable.

They should show:

- node ID;
- labels;
- properties;
- incoming and outgoing relationships;
- related nodes;
- links to typed pages when available.

### Type-Specific Pages

Type-specific pages render known artifact or entity types with custom layouts.

They are still graph projections. They must not introduce alternate canonical fields, local persistence, or page-only source data.

## Artifact Pages

Every artifact has a generic page based on the core artifact model.

Generic artifact pages show:

- artifact metadata;
- status;
- ordered current sections;
- related graph nodes.

Custom artifact pages are selected through an artifact-kind registry:

```text
artifact kind -> page component
```

If no custom page is registered, render the generic artifact page.

## Reference List Pages

Reference lists have a generic collection and list-detail page based on the shared reference list model.

Routes:

```text
/lists
/lists/:listKey
```

Generic list pages show:

- list metadata;
- status;
- seed version;
- item count;
- all items linked to their generic node pages.

Reference item detail pages are intentionally not a separate route. Use `/nodes/:id` for item-level inspection unless a future workflow requires a polished item URL.

## View Models

Do not pass raw graph rows directly to Svelte components.

Use explicit view models, for example:

```text
NavigationView
ArtifactIndexView
ArtifactDetailView
BrainstormDetailView
ReferenceListDetailView
NodeDetailView
GraphOverviewView
```

Include graph IDs and relationship summaries where useful so polished pages can link back to lower-level graph pages.

## Graph Explorer

The graph explorer is read-only.

It may show:

- an interactive node-link graph from server-provided view data;
- label counts;
- relationship type counts;
- recent nodes;
- node lookup by ID;
- node neighborhoods;
- read-only query results.

Default browsing should use typed pages and semantic read adapters. Raw read queries are advanced/admin behavior.

## Caching

Caching is disposable and non-canonical.

Cache keys should include enough graph state to avoid stale display, such as artifact kind plus updated timestamp. Cache files must never become hidden source material.
