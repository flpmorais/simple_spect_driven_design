# Deferred Work Tracker

_Tracks triage and execution state for items originally recorded in `deferred-work.md`. Do not delete raw source history from `deferred-work.md`._

## Status Definitions

- `new`: normalized, not triaged.
- `triaging`: currently under review.
- `needs-user-decision`: user decision required.
- `accepted-risk`: real issue intentionally accepted.
- `no-action`: no work needed.
- `obsolete`: already fixed or no longer relevant.
- `duplicate`: same as another tracked item.
- `planned`: executable plan exists.
- `in-progress`: execution started by deferred runner.
- `blocked`: execution or planning blocked.
- `done`: completed.

## Items

### DW-0001: Production proxy for API and auth

- Status: obsolete
- Source: Deferred from: code review of 1-1-frontend-scaffold-design-system-setup (2026-05-06)
- Raw item: No production proxy for `/api/` and `/auth/` — Vite proxy only works in dev. Production needs nginx reverse proxy (already architected). Pre-existing infrastructure concern.
- Plan artifact:
- Decision: Marked obsolete by user; production nginx proxy now exists for API/auth routes.
- Notes: `nginx/nginx.conf` proxies `/(api|auth|webhook)` to `thagid:8000`, and `compose.yml` builds `thagid-web` from the nginx container.

### DW-0002: components.json baseColor mismatch

- Status: obsolete
- Source: Deferred from: code review of 1-1-frontend-scaffold-design-system-setup (2026-05-06)
- Raw item: `components.json` baseColor `neutral` mismatches cyan theme — shadcn CLI may generate clashing defaults for new components. Low risk, tokens override at runtime.
- Plan artifact:
- Decision: Auto-classified obsolete; the referenced cyan-theme mismatch no longer applies to current project context.
- Notes: `web/components.json` still uses `baseColor: neutral`, but current design context defines navy primary with neutral/slate surfaces, and runtime tokens in `web/src/app.css` provide the project colors.

### DW-0003: Negative radius calculation risk

- Status: no-action
- Source: Deferred from: code review of 1-1-frontend-scaffold-design-system-setup (2026-05-06)
- Raw item: Negative radius risk with `calc()` — `--radius-sm` could go negative if `--radius` < 4px. Default is safe.
- Plan artifact:
- Decision: Approved no-action; current radius default is safe and the risk only appears if the base token is changed below 4px.
- Notes: `web/src/app.css` sets `--radius: 0.625rem` and derives `--radius-sm` with `calc(var(--radius) - 4px)`.

### DW-0004: CTA accent token semantic conflation

- Status: obsolete
- Source: Deferred from: code review of 1-1-frontend-scaffold-design-system-setup (2026-05-06)
- Raw item: CTA mapped to `accent` token — semantic conflation risk but functional. Will be addressed when building actual UI.
- Plan artifact:
- Decision: Auto-classified obsolete; CTA styling is now mapped to the primary token, not the accent token.
- Notes: `web/src/app.css` sets `--primary: #0A3B85` and `--accent: #F1F5F9`; `design-system/thagid/MASTER.md` defines Primary as the CTA button color.

### DW-0005: Healthcheck retries may be insufficient

- Status: accepted-risk
- Source: Deferred from: code review of 1-2-backend-infrastructure-user-authentication (2026-05-07)
- Raw item: Healthcheck retries may be insufficient for slow first-time DB init (25s total). Increase retries or interval if needed in production.
- Plan artifact:
- Decision: Approved accepted-risk; slow first-time DB initialization remains a possible production concern but no immediate work is required.
- Notes: `compose.yml` uses PostgreSQL healthcheck `interval: 5s`, `timeout: 5s`, and `retries: 5`.

### DW-0006: Settings crash on malformed env

- Status: no-action
- Source: Deferred from: code review of 1-2-backend-infrastructure-user-authentication (2026-05-07)
- Raw item: `Settings()` crash on malformed `.env` — fail-fast is correct behavior, no action needed.
- Plan artifact:
- Decision: Approved no-action; fail-fast configuration validation is intentional.
- Notes: `thagid/config.py` instantiates `Settings()` at import time.

### DW-0007: Alembic crash-loop on migration failure

- Status: no-action
- Source: Deferred from: code review of 1-2-backend-infrastructure-user-authentication (2026-05-07)
- Raw item: Alembic crash-loop on persistent migration failure — intentional fail-fast design.
- Plan artifact:
- Decision: Approved no-action; migration failure should fail fast instead of starting the app in an unknown schema state.
- Notes: `Containerfile` runs `alembic upgrade head && exec uvicorn`; compose restart policy may retry on failure.

### DW-0008: Webhook logs full payload

- Status: no-action
- Source: Deferred from: code review of 1-2-backend-infrastructure-user-authentication (2026-05-07)
- Raw item: Webhook logs full payload — pre-existing behavior moved from main.py, may expose sensitive data.
- Plan artifact:
- Decision: User override approved no-action; webhook is currently a stub.
- Notes: `thagid/routers/webhook.py` logs the payload, but user confirmed this does not need work while the webhook remains a stub.

### DW-0009: Missing User updated_at column

- Status: no-action
- Source: Deferred from: code review of 1-2-backend-infrastructure-user-authentication (2026-05-07)
- Raw item: No `updated_at` column on User — out of scope for this story, add when user data becomes mutable.
- Plan artifact:
- Decision: Approved no-action; add `updated_at` only when user data becomes mutable.
- Notes: `thagid/models/user.py` currently has `created_at` only, and current code does not expose a user profile update flow.

### DW-0010: ValueError domain exception pattern

- Status: done
- Source: Deferred from: code review of 1-2-backend-infrastructure-user-authentication (2026-05-07)
- Raw item: `ValueError` used as domain exception instead of custom exception types — refactor when error handling grows.
- Plan artifact: _bmad-output/implementation-artifacts/deferred/deferred-DW-0010-valueerror-domain-exception-pattern.md
- Decision: User approved plan-work; create a small auth-focused domain exception refactor.
- Notes: Completed by adding auth-specific service exceptions for Google token and JWT subject failures, preserving existing router/middleware HTTP behavior, and validating with `pytest thagid/tests/test_auth.py thagid/tests/test_middleware.py`.

### DW-0011: IntegrityError retry path untested

- Status: done
- Source: Deferred from: code review of 1-2-backend-infrastructure-user-authentication (2026-05-07)
- Raw item: IntegrityError retry path untested — concurrent-insert edge case for `get_or_create_user`.
- Plan artifact: _bmad-output/implementation-artifacts/deferred/deferred-DW-0011-integrityerror-retry-path-untested.md
- Decision: Approved plan-work; add focused coverage for the `get_or_create_user` IntegrityError retry branch.
- Notes: Completed by adding focused async coverage for the `get_or_create_user()` concurrent-insert `IntegrityError` retry branch; validated with `pytest thagid/tests/test_auth.py`.

### DW-0012: Cookie attributes not asserted in integration tests

- Status: done
- Source: Deferred from: code review of 1-2-backend-infrastructure-user-authentication (2026-05-07)
- Raw item: Cookie attributes (`httponly`, `secure`, `samesite`, `max_age`) not asserted in integration tests.
- Plan artifact: _bmad-output/implementation-artifacts/deferred/deferred-DW-0012-cookie-attributes-not-asserted.md
- Decision: Approved plan-work; add auth callback integration assertions for session cookie security attributes.
- Notes: Completed by extending `test_auth_callback_success` to assert the `thagid_session` `Set-Cookie` header includes `HttpOnly`, `Secure`, `SameSite=lax`, and `Max-Age=604800`; validated with `pytest thagid/tests/test_middleware.py`.

### DW-0013: Duplicate-email IntegrityError crash

- Status: done
- Source: Deferred from: code review of 1-3-sign-in-page-application-shell (2026-05-07)
- Raw item: `get_or_create_user` crashes on duplicate-email IntegrityError from a different `google_id` — the `except IntegrityError` handler re-selects by `google_id` which doesn't exist, causing unhandled `NoResultFound`. Pre-existing from story 1-2.
- Plan artifact: _bmad-output/implementation-artifacts/deferred/deferred-DW-0013-duplicate-email-integrityerror-crash.md
- Decision: Approved plan-work; fix duplicate-email IntegrityError handling so auth fails predictably instead of raising `NoResultFound`/500.
- Notes: Completed by adding service and route regression coverage for duplicate email with different Google ID, preserving the concurrent same-google-id retry path, and mapping the email conflict to a controlled auth error; validated with `pytest thagid/tests/test_auth.py thagid/tests/test_middleware.py`.

### DW-0014: Missing auth_callback endpoint coverage

- Status: obsolete
- Source: Deferred from: code review of 1-3-sign-in-page-application-shell (2026-05-07)
- Raw item: No test coverage for `auth_callback` endpoint — the most security-sensitive endpoint (validates Google tokens, creates users, sets session cookies). Pre-existing from story 1-2.
- Plan artifact:
- Decision: Auto-classified obsolete; current tests include auth callback endpoint coverage.
- Notes: `thagid/tests/test_middleware.py` has `test_auth_callback_success`, which posts to `/api/auth/callback` and asserts success response data and the session cookie.

### DW-0015: Redundant double-fetch in orgs_update

- Status: accepted-risk
- Source: Deferred from: code review of 2-1-organisation-creation-management (2026-05-07)
- Raw item: Redundant double-fetch in orgs_update — router fetches org for auth check, then service re-fetches for update. Low priority optimization. [thagid/routers/orgs.py:42, thagid/services/organisation.py:28]
- Plan artifact:
- Decision: Approved accepted-risk; redundant fetch remains a low-priority optimization, not a correctness issue.
- Notes: `thagid/routers/orgs.py` fetches the org for auth, then `thagid/services/organisation.py:update_org` fetches again before updating.

### DW-0016: initializeScope concurrent calls

- Status: accepted-risk
- Source: Deferred from: code review of 2-1-organisation-creation-management (2026-05-07)
- Raw item: initializeScope concurrent calls on rapid reactive cycles — layout $effect guards with `!$scope.initialized` but async gap could allow duplicate calls. Unlikely in practice. [web/src/routes/+layout.svelte:24]
- Plan artifact:
- Decision: Approved accepted-risk; duplicate initialization calls are possible during an async gap but low impact at prototype scale.
- Notes: `web/src/routes/+layout.svelte` guards on `$scope.initialized`, while `web/src/lib/stores/scope.ts:initializeScope` sets initialized only after `getMyOrg()` resolves.

### DW-0017: Org settings silent no-op without scope org

- Status: no-action
- Source: Deferred from: code review of 2-1-organisation-creation-management (2026-05-07)
- Raw item: Org settings silent no-op when scope.org is null — handleSave returns silently with no user feedback. Layout normally guards against this state. [web/src/routes/org/settings/+page.svelte:14]
- Plan artifact:
- Decision: Approved no-action; layout normally prevents this route state.
- Notes: `web/src/routes/org/settings/+page.svelte` returns silently when `$scope.org` is missing, but the authenticated shell initializes scope before rendering full routes.

### DW-0018: Project URL format validation

- Status: accepted-risk
- Source: Deferred from: code review of 2-2-org-dashboard-project-cards (2026-05-07)
- Raw item: URL format validation for github_project_url/github_repo_url — not required by spec, prototype phase. [thagid/schemas/project.py:10-11]
- Plan artifact:
- Decision: Approved accepted-risk; stronger backend URL validation is not required by current spec/prototype scope.
- Notes: `thagid/schemas/project.py` enforces max length, while project forms use browser `type="url"` fields.

### DW-0019: loadProjects race without cleanup

- Status: accepted-risk
- Source: Deferred from: code review of 2-2-org-dashboard-project-cards (2026-05-07)
- Raw item: Race condition in loadProjects / no $effect cleanup — prototype phase, low risk of stale response overwriting. [web/src/routes/+page.svelte:36-38]
- Plan artifact:
- Decision: Approved accepted-risk; stale-response overwrite remains possible but low risk for prototype usage.
- Notes: `web/src/routes/+page.svelte` calls `loadProjects()` from effect/search debounce without abort or stale-response guards.

### DW-0020: Missing created_at index for ordering

- Status: done
- Source: Deferred from: code review of 2-2-org-dashboard-project-cards (2026-05-07)
- Raw item: No index on created_at used in ORDER BY — premature optimization for prototype. [thagid/services/project.py:35]
- Plan artifact: _bmad-output/implementation-artifacts/deferred/deferred-DW-0020-missing-created-at-index.md
- Decision: User override approved plan-work; add an index supporting project list ordering by `created_at`.
- Notes: Completed by adding a composite `(org_id, created_at)` project index in the model and Alembic migration, with focused model-shape coverage; validated with `pytest thagid/tests/test_projects.py` and migration syntax compilation.

### DW-0021: Cannot clear nullable PATCH fields

- Status: accepted-risk
- Source: Deferred from: code review of 2-2-org-dashboard-project-cards (2026-05-07)
- Raw item: Cannot clear nullable fields to null via PATCH — standard PATCH None-as-skip pattern, not required by spec. [thagid/services/project.py:68-73]
- Plan artifact:
- Decision: Approved accepted-risk; clearing nullable project fields through PATCH is not required by current spec.
- Notes: `thagid/services/project.py` treats `None` as skip for nullable fields, which matches the current standard PATCH pattern in this codebase.

### DW-0022: Stale project settings form initialization

- Status: accepted-risk
- Source: Deferred from: code review of 3-1-project-crud-github-configuration (2026-05-07)
- Raw item: Stale form initialization in settings if project loads async — `$state()` captures value at mount; layout's scope resolution is async but typically completes before child renders. Architectural pattern used in existing pages. [web/src/routes/project/[id]/settings/+page.svelte:11-14]
- Plan artifact:
- Decision: Approved accepted-risk; stale form initialization remains possible but low risk under the current route/scope loading pattern.
- Notes: `web/src/routes/project/[id]/settings/+page.svelte` initializes local state from `$scope.project`; root layout resolves project scope from the URL.

### DW-0023: Missing client-side max_length validation

- Status: done
- Source: Deferred from: code review of 3-1-project-crud-github-configuration (2026-05-07)
- Raw item: No client-side max_length validation — backend returns 422 handled by generic toast. Not required by spec. [both form pages]
- Plan artifact: _bmad-output/implementation-artifacts/deferred/deferred-DW-0023-missing-client-side-max-length-validation.md
- Decision: User override approved plan-work; add client-side max-length validation for project forms.
- Notes: Completed by adding client-side max-length validation for project name and GitHub project/repo URL fields on project create and settings forms, preserving existing required-field handling and backend validation behavior; validated with `npm run test:unit` and `npm run check` from `web/`.

### DW-0024: Missing URL format validation beyond browser type

- Status: duplicate
- Source: Deferred from: code review of 3-1-project-crud-github-configuration (2026-05-07)
- Raw item: No URL format validation beyond browser `type="url"` — not required by spec for prototype phase. [both form pages]
- Plan artifact:
- Decision: Auto-classified duplicate of DW-0018.
- Notes: Both items cover stronger validation for project GitHub URL fields beyond current max-length/browser `type="url"` behavior; DW-0018 is the canonical tracker item and was accepted as prototype risk.

### DW-0025: Post-create navigation race

- Status: obsolete
- Source: Deferred from: code review of 3-1-project-crud-github-configuration (2026-05-07)
- Raw item: Post-create navigation race with scope resolution — goto fires before layout's async scope load. Pre-existing architectural pattern. [web/src/routes/org/create-project/+page.svelte:41]
- Plan artifact:
- Decision: Approved obsolete; current layout resolves project scope from the `/project/[id]` URL after navigation.
- Notes: `web/src/routes/+layout.svelte` loads the project by URL parameter and calls `setProject(project)`, so post-create navigation no longer depends on pre-populated scope.

### DW-0026: Brief project FK lacks ondelete cascade

- Status: no-action
- Source: Deferred from: code review of 3-2-mock-brief-auto-generation-display (2026-05-07)
- Raw item: No `ondelete` cascade on `briefs.project_id` FK — pre-existing pattern, no project deletion flow exists yet. [thagid/models/brief.py:14]
- Plan artifact:
- Decision: Approved no-action; cascade behavior is not needed while no project deletion flow exists.
- Notes: `thagid/models/brief.py` defines `Brief.project_id` without `ondelete`, but current product flow does not delete projects.

### DW-0027: project_id typed as str in briefs router

- Status: no-action
- Source: Deferred from: code review of 3-2-mock-brief-auto-generation-display (2026-05-07)
- Raw item: `project_id` typed as `str` instead of `uuid.UUID` in router — pre-existing pattern from projects router, consistent across codebase. [thagid/routers/briefs.py:16]
- Plan artifact:
- Decision: Approved no-action; router string parameters with service-level UUID parsing are consistent with current project/org route patterns.
- Notes: `thagid/routers/briefs.py` accepts `project_id: str` and delegates parsing to `get_project()`.

### DW-0028: Inline sqlalchemy import in test

- Status: no-action
- Source: Deferred from: code review of 3-2-mock-brief-auto-generation-display (2026-05-07)
- Raw item: Test uses `__import__("sqlalchemy")` inline — pre-existing test pattern, functional. [thagid/tests/test_briefs.py:64]
- Plan artifact:
- Decision: Approved no-action; inline import is a functional test style issue only.
- Notes: `thagid/tests/test_briefs.py` uses `__import__("sqlalchemy").select(...)` in one test; no runtime behavior is affected.

### DW-0029: Package rows use button navigation

- Status: done
- Source: Deferred from: code review of 3-3-project-dashboard-package-list (2026-05-07)
- Raw item: Package rows use `<button>` + `goto()` instead of `<a href>` — pre-existing accessibility pattern, not introduced by this change.
- Plan artifact: _bmad-output/implementation-artifacts/deferred/deferred-DW-0029-package-rows-use-button-navigation.md
- Decision: Approved plan-work; replace package row button navigation with link semantics.
- Notes: Completed by replacing package row button navigation with anchor link semantics while preserving visual row styling and adding visible focus ring styling; validated with `npm run check`, `npm run test:unit`, and `npm run build` from `web/`.

### DW-0030: NotFoundError pattern fragility

- Status: done
- Source: Deferred from: code review of 3-3-project-dashboard-package-list (2026-05-07)
- Raw item: NotFoundError pattern fragility across services (bare Exception per module) — pre-existing architectural concern, defer to refactor cycle.
- Plan artifact: _bmad-output/implementation-artifacts/deferred/deferred-DW-0030-notfounderror-pattern-fragility.md
- Decision: User approved plan-work; create a shared backend service exception cleanup for NotFoundError-style domain exceptions.
- Notes: Completed by adding shared service exception types and updating project, package, brief, and organisation services to use the shared `NotFoundError` while preserving existing router HTTP behavior; validated with required project/package/brief/org tests plus KG/brainstorm import coverage.

### DW-0031: TopBar loadProjects race

- Status: accepted-risk
- Source: Deferred from: code review of 2-3-scope-aware-sidebar-breadcrumb-navigation (2026-05-07)
- Raw item: loadProjects race on rapid dropdown toggle — no abort/stale guard. Low risk at prototype scale. [TopBar.svelte:16-29]
- Plan artifact:
- Decision: Approved accepted-risk; stale dropdown project-list responses are possible but low impact.
- Notes: `web/src/lib/components/custom/TopBar.svelte` loads projects when the project dropdown opens without abort or stale-response guarding.

### DW-0032: initializeScope missing error handling

- Status: accepted-risk
- Source: Deferred from: code review of 2-3-scope-aware-sidebar-breadcrumb-navigation (2026-05-07)
- Raw item: initializeScope has no try/catch — getMyOrg failure leaves initialized=false forever. Pre-existing from story 2-1. [scope.ts:16-18]
- Plan artifact:
- Decision: Approved accepted-risk; unexpected `getMyOrg()` failures can leave scope uninitialized, but this remains low risk for prototype usage.
- Notes: `web/src/lib/stores/scope.ts` awaits `getMyOrg()` without local try/catch; the no-org 404 case is already normalized in `web/src/lib/api/orgs.ts`.

### DW-0033: Misleading toast on navigation failure

- Status: accepted-risk
- Source: Deferred from: code review of 4-1-package-creation (2026-05-07)
- Raw item: goto inside try block shows misleading toast on navigation failure — if package creation succeeds but goto throws, user sees "Failed to create package". Pre-existing pattern from create-project page. [+page.svelte:39]
- Plan artifact:
- Decision: Approved accepted-risk; navigation failure after successful package creation is rare and low impact.
- Notes: `web/src/routes/project/[id]/package/create/+page.svelte` calls `goto()` inside the try block after showing success.

### DW-0034: Missing accessibility attributes on validation errors

- Status: done
- Source: Deferred from: code review of 4-1-package-creation (2026-05-07)
- Raw item: No accessibility attributes on validation errors — `<p>` error elements lack `aria-describedby`/`aria-invalid`. Pre-existing pattern across all forms. [+page.svelte:62-63,75-76]
- Plan artifact: _bmad-output/implementation-artifacts/deferred/deferred-DW-0034-missing-accessibility-attributes-on-validation-errors.md
- Decision: Approved plan-work; add accessibility attributes connecting validation errors to form controls.
- Notes: Completed by adding conditional `aria-invalid` and `aria-describedby` links between form controls and visible validation errors on package creation, project creation, project settings, and organisation creation forms; validated with `npm run check` and `npm run test:unit` from `web/`.

### DW-0035: Package creation tests cover API only

- Status: no-action
- Source: Deferred from: code review of 4-1-package-creation (2026-05-07)
- Raw item: Tests cover API function, not component behavior — test file is colocated with page but only tests `createPackage` from `$lib/api/packages`. Thin but intentional per completion notes. [create-package.test.ts]
- Plan artifact:
- Decision: Approved no-action; the original colocated `create-package.test.ts` concern is no longer directly applicable.
- Notes: No current `create-package.test.ts` was found; component coverage can be revisited when frontend page testing patterns are added.

### DW-0036: Missing error-path tests

- Status: accepted-risk
- Source: Deferred from: code review of 4-1-package-creation (2026-05-07)
- Raw item: No error-path tests — no test coverage for non-2xx, network failures, or invalid JSON. Coverage gap, not a code bug. [create-package.test.ts]
- Plan artifact:
- Decision: Approved accepted-risk; missing package creation error-path tests remain a coverage gap, not a code bug.
- Notes: Current frontend tests are component-focused elsewhere; no package API error-path test file was found.

### DW-0037: Double error toast on 5xx responses

- Status: done
- Source: Deferred from: code review of 4-1-package-creation (2026-05-07)
- Raw item: Double error toast on 5xx responses — `apiFetch` already toasts on 5xx (client.ts:30), page's catch block toasts again. Pre-existing pattern across all forms. [+page.svelte:41]
- Plan artifact: _bmad-output/implementation-artifacts/deferred/deferred-DW-0037-double-error-toast-on-5xx-responses.md
- Decision: Approved plan-work; prevent duplicate user-facing error toasts for 5xx responses.
- Notes: Completed by marking globally-toasted 5xx API failures with `ServerError`, skipping duplicate form-level notifications for that error type across matching forms, and adding focused API-client coverage; validated with `npm run test:unit -- src/lib/api/client.test.ts`, `npm run test:unit`, and `npm run check` from `web/`.

### DW-0038: Route param ignored in create package page

- Status: done
- Source: Deferred from: code review of 4-1-package-creation (2026-05-07)
- Raw item: URL route param [id] ignored in favor of scope store — page at `/project/[id]/package/create` never reads URL param. Pre-existing architectural pattern. [+page.svelte:33]
- Plan artifact: _bmad-output/implementation-artifacts/deferred/deferred-DW-0038-route-param-ignored-in-create-package-page.md
- Decision: Approved plan-work; use the route project ID parameter for package creation instead of relying only on scope store state.
- Notes: Completed by updating `web/src/routes/project/[id]/package/create/+page.svelte` to use the route project ID from `page.params.id` for package creation and navigation instead of the scope store; validated with `npm run check` and `npm run test:unit` from `web/`.

### DW-0039: Missing max_length on message content

- Status: accepted-risk
- Source: Deferred from: code review of 4-2-chat-interface-echo-service (2026-05-08)
- Raw item: No max_length on message content — unbounded Text in DB, str with only min_length=1 in Pydantic. Deferred per user decision.
- Plan artifact:
- Decision: Approved accepted-risk; unbounded message content remains accepted for prototype per prior user decision.
- Notes: `thagid/schemas/message.py` enforces `min_length=1` and blank rejection only; `thagid/models/message.py` stores content as `Text`.

### DW-0040: Assistant bubble color differs from spec

- Status: obsolete
- Source: Deferred from: code review of 4-2-chat-interface-echo-service (2026-05-08)
- Raw item: Assistant bubble text uses text-slate-900 instead of spec text-cyan-900 — deferred per user preference. [ChatBubble.svelte:23]
- Plan artifact:
- Decision: User override approved obsolete; the older cyan-specific spec has been superseded by the current design system.
- Notes: Current design system uses slate/navy text direction and `ChatBubble.svelte` assistant text uses `text-slate-900`, consistent with current chat message text guidance.

### DW-0041: Chat header color differs from spec

- Status: obsolete
- Source: Deferred from: code review of 4-2-chat-interface-echo-service (2026-05-08)
- Raw item: Chat header title uses text-slate-900 instead of spec text-cyan-900 — deferred per user preference. [ChatInterface.svelte:63]
- Plan artifact:
- Decision: User override approved obsolete; the older cyan-specific spec has been superseded by the current design system.
- Notes: Current design context no longer requires `text-cyan-900` for this chat header concern.

### DW-0042: Message list lacks pagination

- Status: done
- Source: Deferred from: code review of 4-2-chat-interface-echo-service (2026-05-08)
- Raw item: No pagination on list endpoint — not in spec, prototype phase.
- Plan artifact: _bmad-output/implementation-artifacts/deferred/deferred-DW-0042-message-list-loads-more-on-scroll-up.md
- Decision: User override approved plan-work; message history should load the latest 20 messages first, then load older messages as the user scrolls up.
- Notes: Completed by adding default latest-20 backend pagination with offset-based older-page loading, frontend scroll-up loading that prepends older messages while preserving position, and focused backend/frontend coverage; validated with `pytest thagid/tests/test_messages.py`, `npm run check`, and `npm run test:unit` from `web/`.

### DW-0043: Parallel async page effects lack coordination

- Status: accepted-risk
- Source: Deferred from: code review of 4-2-chat-interface-echo-service (2026-05-08)
- Raw item: $effect fires two parallel async ops without coordination — low impact, if pkg load fails messages may still populate silently. [+page.svelte:38-44]
- Plan artifact:
- Decision: Approved accepted-risk; remaining async coordination concern is low impact with the current stale guard.
- Notes: Package page starts package, message, and brainstorm status loads together; current code guards stale responses for route changes.

### DW-0044: Missing invalid-UUID test path

- Status: done
- Source: Deferred from: code review of 4-2-chat-interface-echo-service (2026-05-08)
- Raw item: No test for invalid-UUID 422 path — verify_package_access returns 422 on ValueError but all tests use valid UUIDs. [test_messages.py]
- Plan artifact: _bmad-output/implementation-artifacts/deferred/deferred-DW-0044-missing-invalid-uuid-test-path.md
- Decision: Approved plan-work; add backend coverage for invalid package UUID 422 behavior.
- Notes: Completed by adding focused GET and POST message endpoint coverage for malformed package IDs returning 422; validated with `pytest thagid/tests/test_messages.py`.

### DW-0045: send_message commits in service layer

- Status: no-action
- Source: Deferred from: code review of 4-2-chat-interface-echo-service (2026-05-08)
- Raw item: send_message commits in service layer — matches existing pattern (package.py:create_package). Architectural decision, not a bug.
- Plan artifact:
- Decision: Approved no-action; service-layer commits match existing project patterns.
- Notes: `send_message()` commits in `thagid/services/message.py`, consistent with `create_package()` in `thagid/services/package.py`.

### DW-0046: Package deletion FK violation race

- Status: no-action
- Source: Deferred from: code review of 4-2-chat-interface-echo-service (2026-05-08)
- Raw item: FK violation race if package deleted between verify_package_access and send_message — extremely unlikely, would return raw 500.
- Plan artifact:
- Decision: Approved no-action; no package deletion flow currently exists, so the race is not actionable.
- Notes: The concern only applies if a package is deleted after access verification but before message creation.

### DW-0047: Unrelated changes mixed in changeset

- Status: obsolete
- Source: Deferred from: code review of 4-2-chat-interface-echo-service (2026-05-08)
- Raw item: Unrelated changes (icon.svg viewBox, vite.config.ts import split) mixed in changeset — commit hygiene concern.
- Plan artifact:
- Decision: Approved obsolete; historical changeset hygiene cannot be meaningfully fixed after the fact.
- Notes: Current `icon.svg` and `vite.config.ts` simply contain the already-landed changes.

### DW-0048: Timing-unsafe agent key comparison

- Status: done
- Source: Deferred from: code review of 1-1-brainstorm-runtime-foundation (2026-05-09)
- Raw item: Timing-unsafe key comparison in `verify_agent_key` — uses `!=` instead of `hmac.compare_digest`. Low risk for internal-only service behind compose networking. [agent/main.py:11]
- Plan artifact: _bmad-output/implementation-artifacts/deferred/deferred-DW-0048-timing-unsafe-agent-key-comparison.md
- Decision: Approved plan-work; harden agent key comparison with constant-time comparison.
- Notes: Completed by switching `agent/main.py:verify_agent_key` to `hmac.compare_digest` while preserving missing/empty key rejection and existing 401 behavior; validated with `pytest agent/tests/test_agent_key.py` and `pytest agent/tests`.

### DW-0049: Agent schema init fails fast on DB outage

- Status: no-action
- Source: Deferred from: code review of 1-1-brainstorm-runtime-foundation (2026-05-09)
- Raw item: `ensure_schema()` crashes agent on DB unavailability — lifespan has no error handling for psycopg connection failure, but restart policy loops correctly. Intentional fail-fast behavior. [agent/main.py:17, agent/checkpoint.py:7]
- Plan artifact:
- Decision: Approved no-action; startup fail-fast on schema initialization failure is intentional.
- Notes: Agent lifespan calls `settings.require_agent_key()` and `ensure_schema()` directly; container restart policy handles retry.

### DW-0050: DB extension test skip condition runs at collection

- Status: accepted-risk
- Source: Deferred from: code review of 1-1-brainstorm-runtime-foundation (2026-05-09)
- Raw item: `_can_connect()` evaluated at module import time in test_db_extensions — skipif condition runs at pytest collection phase, not test execution. Minor flakiness risk but gated behind `RUN_EXTENSION_TESTS=1`. [agent/tests/test_db_extensions.py:24-26]
- Plan artifact:
- Decision: Approved accepted-risk; optional extension-test collection-time DB probe remains acceptable.
- Notes: `agent/tests/test_db_extensions.py` gates the probe behind `RUN_EXTENSION_TESTS=1`; risk is limited to optional extension test runs.

### DW-0051: DATABASE_URL is not URL-encoded

- Status: done
- Source: Deferred from: code review of 1-1-brainstorm-runtime-foundation (2026-05-09)
- Raw item: `DATABASE_URL` not URL-encoded — special chars in password break connection string. Same pre-existing pattern in `thagid/config.py`. [agent/config.py:15-16]
- Plan artifact: _bmad-output/implementation-artifacts/deferred/deferred-DW-0051-database-url-not-url-encoded.md
- Decision: Approved plan-work; build database URLs with URL-encoded credentials/components.
- Notes: Completed by URL-encoding PostgreSQL username, password, and database components in backend and agent settings while preserving existing schemes and host/port behavior; validated with `pytest thagid/tests/test_config.py` and `pytest agent/tests/test_config.py`.

### DW-0052: Versioned KG nodes not surfaced in results

- Status: accepted-risk
- Source: Deferred from: code review of 4-1-retrieve-brainstorm-session-results (2026-05-11)
- Raw item: Versioned KG nodes are not surfaced in retrieved results — retrieval follows direct Session/Theme/Idea/ContextChunk relationships and does not resolve `VERSION_OF` current nodes. Existing node-versioning behavior; defer until result retrieval needs editable/current KG views. [thagid/services/knowledge_graph.py:191]
- Plan artifact:
- Decision: Approved accepted-risk; current results retrieval can continue using direct KG relationships until editable/current KG views are needed.
- Notes: `thagid/services/knowledge_graph.py:get_brainstorm_results` follows direct Session/Theme/Idea/ContextChunk relationships and does not resolve `VERSION_OF` current nodes.
