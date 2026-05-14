# Deferred Work

## Deferred from: code review of 1-1-frontend-scaffold-design-system-setup (2026-05-06)

- No production proxy for `/api/` and `/auth/` — Vite proxy only works in dev. Production needs nginx reverse proxy (already architected). Pre-existing infrastructure concern.
- `components.json` baseColor `neutral` mismatches cyan theme — shadcn CLI may generate clashing defaults for new components. Low risk, tokens override at runtime.
- Negative radius risk with `calc()` — `--radius-sm` could go negative if `--radius` < 4px. Default is safe.
- CTA mapped to `accent` token — semantic conflation risk but functional. Will be addressed when building actual UI.

## Deferred from: code review of 1-2-backend-infrastructure-user-authentication (2026-05-07)

- Healthcheck retries may be insufficient for slow first-time DB init (25s total). Increase retries or interval if needed in production.
- `Settings()` crash on malformed `.env` — fail-fast is correct behavior, no action needed.
- Alembic crash-loop on persistent migration failure — intentional fail-fast design.
- Webhook logs full payload — pre-existing behavior moved from main.py, may expose sensitive data.
- No `updated_at` column on User — out of scope for this story, add when user data becomes mutable.
- `ValueError` used as domain exception instead of custom exception types — refactor when error handling grows.
- IntegrityError retry path untested — concurrent-insert edge case for `get_or_create_user`.
- Cookie attributes (`httponly`, `secure`, `samesite`, `max_age`) not asserted in integration tests.

## Deferred from: code review of 1-3-sign-in-page-application-shell (2026-05-07)

- `get_or_create_user` crashes on duplicate-email IntegrityError from a different `google_id` — the `except IntegrityError` handler re-selects by `google_id` which doesn't exist, causing unhandled `NoResultFound`. Pre-existing from story 1-2.
- No test coverage for `auth_callback` endpoint — the most security-sensitive endpoint (validates Google tokens, creates users, sets session cookies). Pre-existing from story 1-2.

## Deferred from: code review of 2-1-organisation-creation-management (2026-05-07)

- Redundant double-fetch in orgs_update — router fetches org for auth check, then service re-fetches for update. Low priority optimization. [thagid/routers/orgs.py:42, thagid/services/organisation.py:28]
- initializeScope concurrent calls on rapid reactive cycles — layout $effect guards with `!$scope.initialized` but async gap could allow duplicate calls. Unlikely in practice. [web/src/routes/+layout.svelte:24]
- Org settings silent no-op when scope.org is null — handleSave returns silently with no user feedback. Layout normally guards against this state. [web/src/routes/org/settings/+page.svelte:14]

## Deferred from: code review of 2-2-org-dashboard-project-cards (2026-05-07)

- URL format validation for github_project_url/github_repo_url — not required by spec, prototype phase. [thagid/schemas/project.py:10-11]
- Race condition in loadProjects / no $effect cleanup — prototype phase, low risk of stale response overwriting. [web/src/routes/+page.svelte:36-38]
- No index on created_at used in ORDER BY — premature optimization for prototype. [thagid/services/project.py:35]
- Cannot clear nullable fields to null via PATCH — standard PATCH None-as-skip pattern, not required by spec. [thagid/services/project.py:68-73]

## Deferred from: code review of 3-1-project-crud-github-configuration (2026-05-07)

- Stale form initialization in settings if project loads async — `$state()` captures value at mount; layout's scope resolution is async but typically completes before child renders. Architectural pattern used in existing pages. [web/src/routes/project/[id]/settings/+page.svelte:11-14]
- No client-side max_length validation — backend returns 422 handled by generic toast. Not required by spec. [both form pages]
- No URL format validation beyond browser `type="url"` — not required by spec for prototype phase. [both form pages]
- Post-create navigation race with scope resolution — goto fires before layout's async scope load. Pre-existing architectural pattern. [web/src/routes/org/create-project/+page.svelte:41]

## Deferred from: code review of 3-2-mock-brief-auto-generation-display (2026-05-07)

- No `ondelete` cascade on `briefs.project_id` FK — pre-existing pattern, no project deletion flow exists yet. [thagid/models/brief.py:14]
- `project_id` typed as `str` instead of `uuid.UUID` in router — pre-existing pattern from projects router, consistent across codebase. [thagid/routers/briefs.py:16]
- Test uses `__import__("sqlalchemy")` inline — pre-existing test pattern, functional. [thagid/tests/test_briefs.py:64]

## Deferred from: code review of 3-3-project-dashboard-package-list (2026-05-07)

- Package rows use `<button>` + `goto()` instead of `<a href>` — pre-existing accessibility pattern, not introduced by this change.
- NotFoundError pattern fragility across services (bare Exception per module) — pre-existing architectural concern, defer to refactor cycle.

## Deferred from: code review of 2-3-scope-aware-sidebar-breadcrumb-navigation (2026-05-07)

- loadProjects race on rapid dropdown toggle — no abort/stale guard. Low risk at prototype scale. [TopBar.svelte:16-29]
- initializeScope has no try/catch — getMyOrg failure leaves initialized=false forever. Pre-existing from story 2-1. [scope.ts:16-18]

## Deferred from: code review of 4-1-package-creation (2026-05-07)

- goto inside try block shows misleading toast on navigation failure — if package creation succeeds but goto throws, user sees "Failed to create package". Pre-existing pattern from create-project page. [+page.svelte:39]
- No accessibility attributes on validation errors — `<p>` error elements lack `aria-describedby`/`aria-invalid`. Pre-existing pattern across all forms. [+page.svelte:62-63,75-76]
- Tests cover API function, not component behavior — test file is colocated with page but only tests `createPackage` from `$lib/api/packages`. Thin but intentional per completion notes. [create-package.test.ts]
 - No error-path tests — no test coverage for non-2xx, network failures, or invalid JSON. Coverage gap, not a code bug. [create-package.test.ts]
 - Double error toast on 5xx responses — `apiFetch` already toasts on 5xx (client.ts:30), page's catch block toasts again. Pre-existing pattern across all forms. [+page.svelte:41]
 - URL route param [id] ignored in favor of scope store — page at `/project/[id]/package/create` never reads URL param. Pre-existing architectural pattern. [+page.svelte:33]

## Deferred from: code review of 4-2-chat-interface-echo-service (2026-05-08)

- No max_length on message content — unbounded Text in DB, str with only min_length=1 in Pydantic. Deferred per user decision.
- Assistant bubble text uses text-slate-900 instead of spec text-cyan-900 — deferred per user preference. [ChatBubble.svelte:23]
- Chat header title uses text-slate-900 instead of spec text-cyan-900 — deferred per user preference. [ChatInterface.svelte:63]
- No pagination on list endpoint — not in spec, prototype phase.
- $effect fires two parallel async ops without coordination — low impact, if pkg load fails messages may still populate silently. [+page.svelte:38-44]
- No test for invalid-UUID 422 path — verify_package_access returns 422 on ValueError but all tests use valid UUIDs. [test_messages.py]
- send_message commits in service layer — matches existing pattern (package.py:create_package). Architectural decision, not a bug.
- FK violation race if package deleted between verify_package_access and send_message — extremely unlikely, would return raw 500.
- Unrelated changes (icon.svg viewBox, vite.config.ts import split) mixed in changeset — commit hygiene concern.

## Deferred from: code review of 1-1-brainstorm-runtime-foundation (2026-05-09)

- Timing-unsafe key comparison in `verify_agent_key` — uses `!=` instead of `hmac.compare_digest`. Low risk for internal-only service behind compose networking. [agent/main.py:11]
- `ensure_schema()` crashes agent on DB unavailability — lifespan has no error handling for psycopg connection failure, but restart policy loops correctly. Intentional fail-fast behavior. [agent/main.py:17, agent/checkpoint.py:7]
- `_can_connect()` evaluated at module import time in test_db_extensions — skipif condition runs at pytest collection phase, not test execution. Minor flakiness risk but gated behind `RUN_EXTENSION_TESTS=1`. [agent/tests/test_db_extensions.py:24-26]
- `DATABASE_URL` not URL-encoded — special chars in password break connection string. Same pre-existing pattern in `thagid/config.py`. [agent/config.py:15-16]

## Deferred from: code review of 4-1-retrieve-brainstorm-session-results (2026-05-11)

- Versioned KG nodes are not surfaced in retrieved results — retrieval follows direct Session/Theme/Idea/ContextChunk relationships and does not resolve `VERSION_OF` current nodes. Existing node-versioning behavior; defer until result retrieval needs editable/current KG views. [thagid/services/knowledge_graph.py:191]
