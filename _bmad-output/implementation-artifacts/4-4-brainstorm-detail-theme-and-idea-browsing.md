# Story 4.4: Brainstorm Detail Theme and Idea Browsing

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a package user,
I want a detailed brainstorm results page with themes and ideas,
so that I can inspect final outputs without reopening the active chat flow.

## Acceptance Criteria

1. Given I open a brainstorm detail page, when results load successfully, then I see the session summary, key insights, theme cards, and idea cards, and the page uses Thagid design system tokens and shadcn-svelte primitives.
2. Given a theme card is collapsed, when I activate the theme header, then the theme expands to show its ideas, and each idea card shows title, concept description, category, and novelty.
3. Given I want to return to the package conversation, when I use the Back to Package action, then I navigate back to the package chat route, and the org, project, and package scope remains consistent in breadcrumbs and sidebar.

## Tasks / Subtasks

- [x] Create the brainstorm detail route and load results (AC: 1, 3)
  - [x] Add `web/src/routes/project/[id]/package/[pkgId]/brainstorm/+page.svelte` for `/project/{projectId}/package/{packageId}/brainstorm`.
  - [x] Read the current package via `getPackage(pkgId)` so the page can preserve package title/context and validate package access through the existing API layer.
  - [x] Load concluded brainstorm results with existing `getBrainstormResults(pkgId)` from `$lib/api/brainstorm.ts`; do not call raw `fetch()` from the page or components.
  - [x] Preserve stale-response protection when route params change before async loads resolve, matching existing package and project dashboard `$effect` patterns.
  - [x] Show a loading skeleton or status while package/results requests are pending.
  - [x] For `404 Brainstorm results not found`, show the design-system empty state with a Go to Chat action instead of a user-visible error toast.
  - [x] For other load failures, show a non-destructive error state and keep the Back to Package action available when route params exist.
- [x] Build the detail page layout (AC: 1, 3)
  - [x] Render a top Back to Package link to `/project/{projectId}/package/{packageId}` using Lucide `arrow-left` and design-system link styles.
  - [x] Render page title `Brainstorm Session`, a concluded `BrainstormPhaseBadge`, and metadata row using date, technique count, idea count, and theme count.
  - [x] Derive technique count as `1` when `BrainstormResultsResponse.technique` is non-null and `0` when null unless the backend response is explicitly extended.
  - [x] Format `concluded_at` first, falling back to `created_at`; never render raw ISO strings and tolerate null or invalid dates with a neutral label.
  - [x] Move focus to the main heading after navigation/render so Story 4.3's View Details focus requirement is satisfied.
  - [x] Preserve the existing app shell, project-scope sidebar, package highlighting, and top-bar breadcrumb behavior; do not implement a separate layout.
- [x] Render session summary and key insights area (AC: 1)
  - [x] Use shadcn `Card` composition for a non-interactive Session Summary card.
  - [x] Render `summary` as safe plain text or simple paragraphs from backend structured data; do not use `{@html}` or introduce a markdown library unless explicitly approved.
  - [x] If no separate `key_insights` field exists, do not change backend contracts just for this story; render the existing session summary and note that explicit key-insight extraction requires a future contract change.
  - [x] Do not expose `context_sources.content`, graph internals, raw Cypher data, or internal `/internal/kg/*` endpoints in the UI.
- [x] Render collapsible themes and idea cards (AC: 1, 2)
  - [x] Reuse existing `BrainstormResultsResponse.themes` and `BrainstormTheme.ideas` data; preserve response ordering, which should reflect graph/theme ordering from Story 4.1.
  - [x] Reuse or update `ThemeCard.svelte` only if it remains compatible with existing chat/theme grouping uses; otherwise create a detail-specific wrapper/component.
  - [x] Ensure theme headers are buttons with `aria-expanded`, visible focus rings, Lucide `layers`, idea count badge, and chevron state.
  - [x] Ensure collapsed theme state hides the idea list until activated; tests must prove collapsed -> expanded behavior.
  - [x] Render each idea with title, concept description, category, and novelty using existing `BrainstormIdea` fields; reuse `IdeaCard.svelte` where practical.
  - [x] Keep all icons Lucide-only; do not use emoji icons from UX mockups.
- [x] Add focused frontend tests (AC: 1, 2, 3)
  - [x] Add component-level tests for any new detail-specific components, covering metadata/date fallback, summary rendering, theme collapse/expand, idea fields, empty state, and Back to Package href.
  - [x] Update `ThemeCard.test.ts` and/or `IdeaCard.test.ts` if those components are changed.
  - [x] If no route-level test harness exists, document that component/page behavior is covered through component tests plus `svelte-check`.
  - [x] Run `cd web && npm run check` and `cd web && npm run test:unit` or a narrower Vitest command covering changed frontend tests.

## Dev Notes

### Scope Boundaries

- This is a frontend results browsing story. Build the brainstorm detail route and theme/idea browsing UI only.
- Reuse the existing browser-facing endpoint: `GET /api/packages/{package_id}/brainstorm/results`. It is JWT-authenticated, verifies package access, and returns `404` with detail `Brainstorm results not found` when no concluded results exist.
- Do not add backend endpoints, migrations, KG write behavior, vector search UI, or agent/container changes unless a hard blocker is found and approved.
- Do not expose internal `/internal/kg/*` endpoints, raw graph IDs beyond stable response IDs already present, raw context chunk content, or Cypher/SQL details to the frontend.

### Current Codebase State

- The package chat route exists at `web/src/routes/project/[id]/package/[pkgId]/+page.svelte`. It loads package data, messages, brainstorm status, techniques, and renders `ChatInterface`.
- There is no existing `web/src/routes/project/[id]/package/[pkgId]/brainstorm/` directory. Story 4.4 owns creating that route.
- `web/src/lib/api/brainstorm.ts` already exports `getBrainstormResults(packageId)` for `/api/packages/{packageId}/brainstorm/results`. Use it; do not duplicate request logic.
- `web/src/lib/types/brainstorm.ts` already defines `BrainstormResultsResponse`, `BrainstormTheme`, `BrainstormIdea`, and `BrainstormPhase`. The response includes `session_id`, `package_id`, `project_id`, `technique`, `summary`, `created_at`, `concluded_at`, `theme_count`, `idea_count`, `context_source_count`, `themes`, and `context_sources`.
- Existing custom components available for reuse:
  - `BrainstormPhaseBadge.svelte` renders phase badge variants including `concluded`.
  - `IdeaCard.svelte` renders title, concept, category, and novelty for a `BrainstormIdea`.
  - `ThemeCard.svelte` renders a collapsible theme with ideas and `aria-expanded`, currently defaulting to expanded.
  - `BrainstormSummaryCard.svelte` links to the planned detail route created by this story.
- Existing tests include `IdeaCard.test.ts`, `ThemeCard.test.ts`, and `BrainstormSummaryCard.test.ts`; no route-level frontend tests were found.

### UI / Design-System Requirements

- Because this story edits UI, the developer must read and follow `design-system/thagid/MASTER.md` and `design-system/thagid/pages/brainstorm-detail.md` before coding.
- Brainstorm detail route: `/project/{projectId}/package/{packageId}/brainstorm`; sidebar stays project scope with the current package highlighted; top bar remains Logo / Org dropdown / Project dropdown.
- Header spec: Back to Package link with `arrow-left`, `text-sm text-primary cursor-pointer hover:underline`; title `Brainstorm Session`, `text-2xl font-bold text-slate-900`; concluded phase badge; metadata `text-sm text-slate-500`.
- Session Summary card: shadcn `Card`, non-interactive, label `text-xs font-medium text-slate-400 uppercase tracking-wider`, content `text-sm text-slate-600`, margins `mt-6 mb-8`.
- Themes section: section title `Themes`, `text-lg font-semibold text-slate-900`; vertical stack with `gap-4`.
- Theme detail cards: `bg-white border border-slate-200 rounded-xl p-5`; header with `layers`, theme title, idea count badge, chevron state; idea rows show title, category, concept/description, and novelty with hover `bg-slate-50` when interactive.
- Empty state: centered Lucide `lightbulb`, heading `No brainstorm session yet`, description, primary CTA `Go to Chat`.
- Desktop-only MVP remains minimum 1024px; do not add mobile/tablet-specific responsive work.
- Accessibility: all interactive controls keyboard reachable; visible focus rings; `aria-expanded` on theme toggles; main content heading receives focus after detail navigation; respect `prefers-reduced-motion` if adding animation.

### Architecture and API Compliance

- Frontend architecture rule: pages call `$lib/api/*` client functions; components render props; no raw `fetch()` in Svelte components.
- Use existing `apiFetch` error behavior through `getBrainstormResults`; handle the expected no-results 404 locally as an empty state.
- Keep JSON field usage snake_case at the API/type boundary (`created_at`, `concluded_at`, `theme_count`, `idea_count`) and camelCase only for local TS helper names.
- Do not change `BrainstormResultsResponse` unless backend schemas and tests are intentionally updated; this story should not need that.
- SvelteKit routing is filesystem-based: create `+page.svelte` under a `brainstorm` subdirectory. Use normal `<a>` links for navigation where possible.
- Svelte 5 runes are already in use; follow existing patterns with `$state`, `$derived`, `$effect`, and `$props` rather than legacy `export let`.

### Current State of Files Likely to be Modified

- `web/src/routes/project/[id]/package/[pkgId]/+page.svelte` currently owns chat-only package detail. This story should normally leave it unchanged unless adding a concluded-session link from chat is explicitly necessary and covered by tests.
- `web/src/lib/components/custom/ThemeCard.svelte` currently defaults expanded and renders inline cards. If changed for detail browsing, preserve current theme grouping/chat usability or use a new detail component to avoid regressions.
- `web/src/lib/components/custom/IdeaCard.svelte` is pure and presentational. It can be reused on the detail page, but the detail design may require row styling; avoid breaking its existing test/contract.
- `web/src/lib/api/brainstorm.ts` and `web/src/lib/types/brainstorm.ts` already contain the needed results API/type. They should usually remain unchanged.

### Previous Story Intelligence

- Story 4.3 created `BrainstormSummaryCard.svelte`, wired the project dashboard to load per-package results, and linked View Details to `/project/{projectId}/package/{packageId}/brainstorm`. Story 4.4 must implement that target route and focus handoff.
- Story 4.3 treated `404 Brainstorm results not found` as an expected no-concluded-results state; keep the same behavior for direct detail visits by rendering the empty state instead of surfacing an error toast.
- Story 4.3 avoided backend changes and reused `getBrainstormResults`; continue that pattern.
- Story 4.1 added browser results retrieval and review fixes that avoid exposing raw context chunk content. The detail view can render source metadata later if needed, but this story's ACs are summary, themes, and ideas.
- Recent commit style is concise and feature-oriented: `feat: add brainstorm dashboard summary card`, `fix vector search review findings`, `fix brainstorm results review findings`, `feat: add extraction validation and node versioning`, `feat: add brainstorm markdown finalization`.

### Latest Technical Context

- Svelte 5 runes (`$state`, `$derived`, `$effect`, `$props`) are language-level syntax and require no imports. Existing project components already use this style.
- SvelteKit routes are defined by directories under `src/routes`; a nested `brainstorm/+page.svelte` creates the needed detail URL. SvelteKit uses standard `<a>` elements for route navigation, so prefer anchors for Back to Package and View/Go to Chat links unless programmatic navigation is required.

### File Structure Requirements

- Likely frontend additions:
  - `web/src/routes/project/[id]/package/[pkgId]/brainstorm/+page.svelte` (new)
  - A focused component under `web/src/lib/components/custom/` only if the page becomes too complex, e.g. `BrainstormDetailView.svelte` or `BrainstormDetailThemeCard.svelte` (new)
  - Matching component tests for new custom components if added
- Possible frontend updates only if needed:
  - `web/src/lib/components/custom/ThemeCard.svelte`
  - `web/src/lib/components/custom/ThemeCard.test.ts`
  - `web/src/lib/components/custom/IdeaCard.svelte`
  - `web/src/lib/components/custom/IdeaCard.test.ts`
- Avoid backend files, schemas, tests, migrations, agent files, KG service files, compose files, and package-chat changes unless explicitly required and approved.

### Testing Requirements

- Frontend checks: run `cd web && npm run check` after UI changes.
- Unit tests: run `cd web && npm run test:unit` or a narrow command that includes every changed/new component test.
- Test expected UI contracts: successful results render summary/metadata/themes/ideas; theme starts collapsed if required by the implemented component state and expands with `aria-expanded`; Back to Package and Go to Chat hrefs preserve project and package ids; missing results renders empty state; invalid/null dates do not crash.
- Backend tests are not required if backend contracts are unchanged. If backend code is changed despite guidance, run `rtk pytest thagid/tests/test_brainstorm.py -q`.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-4.4-Brainstorm-Detail-Theme-and-Idea-Browsing]
- [Source: _bmad-output/planning-artifacts/prd.md#Frontend-Brainstorm-Dashboard]
- [Source: _bmad-output/planning-artifacts/architecture.md#Frontend-Dashboard]
- [Source: _bmad-output/planning-artifacts/architecture.md#API-Boundaries]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Journey-5-Reviewing-Brainstorm-Results]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#Brainstorm-Dashboard-FR34-FR36]
- [Source: design-system/thagid/MASTER.md#Idea-Card]
- [Source: design-system/thagid/MASTER.md#Theme-Card]
- [Source: design-system/thagid/pages/brainstorm-detail.md]
- [Source: web/src/lib/api/brainstorm.ts]
- [Source: web/src/lib/types/brainstorm.ts]
- [Source: web/src/lib/components/custom/BrainstormPhaseBadge.svelte]
- [Source: web/src/lib/components/custom/IdeaCard.svelte]
- [Source: web/src/lib/components/custom/ThemeCard.svelte]
- [Source: thagid/routers/brainstorm.py]
- [Source: thagid/schemas/brainstorm.py]
- [Source: _bmad-output/implementation-artifacts/4-3-brainstorm-summary-card-on-project-dashboard.md#Previous-Story-Intelligence]
- [Source: _bmad-output-old/1_datapipeline/project-context.md#Critical-Implementation-Rules]

## Project Structure Notes

- This story extends the existing SvelteKit route tree under the package route with a nested brainstorm detail page.
- Keep the API access layered: route/page calls `$lib/api/brainstorm.ts`, custom components receive typed props and render UI only.
- Prefer reusing existing brainstorm custom components, but do not change them in ways that break package chat or theme grouping behavior.

## Dev Agent Record

### Agent Model Used

openai/gpt-5.5

### Debug Log References

- `cd web && rtk npm run test:unit -- BrainstormDetailView.test.ts` - passed (5 tests).
- `cd web && rtk npm run check` - passed with 0 errors and 0 warnings.
- `cd web && rtk npm run test:unit` - passed (11 files, 47 tests).

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created.
- Implemented `/project/{projectId}/package/{packageId}/brainstorm` route using `getPackage` and `getBrainstormResults` through existing API clients with stale-response protection.
- Added a detail view component with loading, no-results, non-destructive error, summary, metadata, focus handoff, Back to Package, and Go to Chat states.
- Added detail-specific collapsible theme browsing that preserves response ordering and renders each idea title, concept, category, and novelty without changing backend contracts.
- Covered route-rendered UI behavior through focused component tests; no route-level harness exists, so `svelte-check` plus component tests validate the page behavior.

### File List

- web/src/lib/components/custom/BrainstormDetailView.svelte
- web/src/lib/components/custom/BrainstormDetailView.test.ts
- web/src/routes/project/[id]/package/[pkgId]/brainstorm/+page.svelte
- _bmad-output/implementation-artifacts/4-4-brainstorm-detail-theme-and-idea-browsing.md
- _bmad-output/implementation-artifacts/sprint-status.yaml

### Change Log

- 2026-05-11: Added brainstorm detail route, results browsing view, focused component tests, and moved story to review.
