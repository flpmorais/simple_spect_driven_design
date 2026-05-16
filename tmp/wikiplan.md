# Wiki Implementation Plan

1. Scaffold SvelteKit wiki app
   - Create `wiki/` with the minimal SvelteKit structure, shared layout, and development scripts.

2. Add server-side graph read boundary
   - Implement server-only adapters that call semantic memory reads and return typed view models.

3. Build baseline navigation and shell
   - Add graph-derived navigation, global layout, and home page for browsing available wiki sections.

4. Implement artifact browsing
   - Add artifact index, generic artifact detail, artifact version pages, and artifact page registry fallback.

5. Add type-specific views
   - Add custom page wiring for artifact/entity types only when the generic pages are not enough.

6. Add graph/entity browsing support
   - Add brainstorm browsing, generic node detail, graph overview, and read-only diagnostics needed for navigation and debugging.
