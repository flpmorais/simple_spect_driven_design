# Story 2.6: URL Context Ingestion

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a package user,
I want to share URLs during brainstorm facilitation,
so that external references can influence ideation while preserving session flow.

## Acceptance Criteria

1. Given the session is in Facilitate phase, when I add a valid URL through the chat input URL action, then the URL appears as a removable pending attachment chip, and it is sent with my next message.
2. Given a URL attachment is sent, when the agent processes the message, then it fetches and extracts readable text content into an active context chunk, and acknowledges the URL in chat with a concise summary.
3. Given URL fetching or extraction fails, when the agent handles the attachment, then it reports the issue in chat without ending the brainstorm session, and existing ideas and technique state are preserved.

## Tasks / Subtasks

- [x] Define a URL attachment contract that extends the existing brainstorm JSON message path (AC: 1, 2, 3)
  - [x] Add a `BrainstormUrlAttachment` shape in frontend/backend/agent contracts with at least `url` and optional display metadata if needed.
  - [x] Keep `POST /api/packages/{package_id}/brainstorm/message` JSON-based; do not add multipart, websocket, browser-side URL fetching, or a new endpoint.
  - [x] Add `urls: list[BrainstormUrlAttachment] = []` alongside the existing `files` list. Preserve all existing callers that omit both fields.
  - [x] Enforce exactly one pending/sent URL for this story, matching the one-file MVP limit from Story 2.5. Do not allow mixed file+URL sends unless explicitly implemented and tested; the smallest safe path is to reject mixed attachments with a validation/toast message.
  - [x] Preserve existing brainstorm response fields: `message`, `session_id`, `phase`, `technique`, `idea_count`, `message_count`, and `ideas`.
  - [x] If the user sends a URL with no typed message, generate deterministic transcript content such as `Shared URL: {url}` to preserve non-blank `Message.content` assumptions.
- [x] Add URL sharing UI to package chat (AC: 1, UX-DR13, UX-DR14)
  - [x] Update `ChatInterface.svelte` with a Lucide `Link` ghost icon button (`w-9 h-9`) beside the existing paperclip button.
  - [x] Add a small URL popover/input with `type="url"`, an Add action, Escape/blur-safe close behavior if practical, visible focus states, and no layout shift.
  - [x] Accept only absolute `http://` and `https://` URLs. Normalize by trimming whitespace; preserve the submitted URL for transcript readability.
  - [x] Show pending URLs as removable chips above the textarea using the design-system URL chip style: `bg-blue-50`, link icon, domain text, max width, and remove button.
  - [x] Render sent URL chips on the optimistic current-session user message, similar to Story 2.5 sent-file chips. They may be transient and do not need to survive reload.
  - [x] Allow send when either trimmed text exists or one pending URL exists, but only during `brainstormPhase === 'facilitate'` for URL-only sends.
  - [x] Disable the URL control outside Facilitate, while sending, and when no brainstorm session is active. Disabled state must use `disabled`, a clear accessible label, and must not open the popover.
  - [x] Preserve existing file upload behavior, pending file retention on failure, Enter/Shift+Enter behavior, auto-scroll, `role="log"`, `aria-live="polite"`, reduced-motion handling, technique picker, idea cards, phase badge, and message counts.
  - [x] Do not implement drag-and-drop URLs, URL preview cards, bookmark metadata, multiple URL chips, or URL persistence in the messages table for this story.
- [x] Extend browser types, API client, and route state (AC: 1, 3)
  - [x] Update `web/src/lib/types/brainstorm.ts` with `BrainstormUrlAttachment`; consider a shared attachment display type only if it stays simpler than separate file/url arrays.
  - [x] Update `web/src/lib/api/brainstorm.ts` so `sendBrainstormMessage` can include `urls` while preserving the existing `files` argument and current callers.
  - [x] Update `web/src/lib/types/message.ts` and `ChatBubble.svelte` so optimistic user messages can render URL chips without changing persisted backend message shape.
  - [x] Update `web/src/routes/project/[id]/package/[pkgId]/+page.svelte` so brainstorm sends pass URLs only through the brainstorm path. Regular package chat must remain unaffected.
  - [x] On send failure, remove only the optimistic user message and restore pending URL state in `ChatInterface.svelte`, matching Story 2.5 failure behavior.
- [x] Validate and forward URL attachments in FastAPI (AC: 1, 2, 3)
  - [x] Extend `BrainstormMessageCreate` in `thagid/schemas/brainstorm.py` to accept `urls: list[BrainstormUrlAttachment] = []` with max length `1`.
  - [x] Validate URL presence, absolute scheme, allowed scheme (`http` or `https`), and no blank content before calling the agent.
  - [x] Reject more than one URL and mixed file+URL attachments unless the implementation explicitly supports and tests both in one send.
  - [x] Continue verifying package access in `thagid/routers/brainstorm.py` before forwarding any URL to the agent.
  - [x] Update `thagid/services/brainstorm.py` and `thagid/services/agent_client.py` to forward `urls` to the agent in the existing JSON payload.
  - [x] Do not store fetched URL text in the `messages` table. Do not add migrations, URL tables, or background jobs in this story.
- [x] Fetch and extract URL content inside the agent boundary (AC: 2, 3)
  - [x] Extend `BrainstormMessageRequest` in `agent/main.py` to accept `urls` alongside existing `files`.
  - [x] Reject URL attachments when the loaded session phase is not `facilitate`; frontend should prevent this, but the agent must guard the boundary.
  - [x] Fetch URLs from the agent using existing dependencies only, preferably `httpx.AsyncClient`; do not introduce a new scraping/readability library.
  - [x] Use a short deterministic timeout and bounded download size. Set an explicit max extracted text size, recommended `BRAINSTORM_URL_MAX_BYTES = 262_144` to match Story 2.5 file content bounds.
  - [x] Follow redirects only if each resolved target remains safe and allowed. Cap redirects; reject redirect loops or unsafe final destinations.
  - [x] Accept text-like responses only: `text/plain`, `text/markdown`, `text/csv`, `application/json`, and `text/html`. Reject images, PDFs, DOCX, binaries, and empty responses with a user-facing acknowledgement rather than mutating checkpoint state.
  - [x] Extract readable text deterministically. For HTML, strip scripts/styles/tags with a small stdlib helper; for text/JSON/CSV, normalize whitespace enough to produce useful context without freeform LLM summarization.
  - [x] Convert successful fetches into active context chunks stored in `state["active_documents"]` with stable future-KG-friendly fields: `id`, `source_type: "url"`, `source_ref` as canonical URL, `content`, and `summary`.
  - [x] Deduplicate active documents by `source_type`, canonical URL, and content hash or exact content so resending the same URL does not create avoidable duplicates.
  - [x] Include an acknowledgement in the assistant reply, for example `I've pulled content from {domain}. {summary}`.
  - [x] If an ideation text message accompanies the URL, preserve Story 2.3 idea extraction/reducer behavior in the same turn.
- [x] Add SSRF and network-safety guardrails before URL fetching (AC: 2, 3)
  - [x] Reject non-HTTP(S) schemes including `file:`, `ftp:`, `data:`, `javascript:`, and protocol-relative URLs.
  - [x] Resolve the hostname with stdlib `socket`/`ipaddress` before fetching and reject localhost, loopback, link-local, private, multicast, unspecified, and reserved IP ranges.
  - [x] Re-run the same safety check after redirects before reading the response body.
  - [x] Do not send cookies, auth headers, user credentials, or internal service headers to external URLs.
  - [x] Do not allow the agent to fetch internal podman service names, `localhost`, `127.0.0.0/8`, `::1`, RFC1918 private ranges, or metadata IPs such as `169.254.169.254`.
  - [x] Log technical fetch failures for diagnosis, but return concise user-facing failure text in the assistant reply.
- [x] Preserve existing brainstorm behavior and Story 2.5 file ingestion (AC: 1, 2, 3)
  - [x] Existing file upload controls, validation, active document chunks, deduplication, checkpoint merge behavior, and tests must continue to pass.
  - [x] Existing `active_documents` with `source_type: "file"` must remain untouched when adding URL chunks.
  - [x] Story 2.4 rolling summary must continue to include active document refs and summaries after URL chunks exist.
  - [x] Technique recommendation, technique picker, initiate selection, facilitate technique swaps, idea extraction, duplicate reduction, contradiction handling, anti-bias pivoting, status/resume, and regular package chat must remain unaffected.
  - [x] Epic 3 KG `ContextChunk` writes remain out of scope; URL chunks live only in agent checkpoint state for this story.
- [x] Add focused tests and verification (AC: 1, 2, 3)
  - [x] Add agent tests for successful URL ingestion during Facilitate, active document chunk shape, acknowledgement text, deduplication, and preserving existing ideas/files.
  - [x] Add agent tests for non-Facilitate rejection and for fetch/extraction failure returning an acknowledgement without mutating `active_documents` or ending the session.
  - [x] Add agent tests for SSRF protections: localhost, private IP, link-local/metadata IP, unsupported scheme, and unsafe redirect if practical.
  - [x] Add backend tests for URL validation, forwarding `urls` to the agent client, unsupported scheme, more than one URL, mixed file+URL behavior, authenticated success, unauthenticated rejection, and cross-org forbidden.
  - [x] Add frontend tests for URL popover open/add/remove, disabled link control outside Facilitate, URL-only send behavior, optimistic URL chip rendering, invalid URL validation toast if practical, and pending URL retention on send failure.
- [x] Run `rtk pytest agent/tests/test_brainstorm.py`.
- [x] Run `rtk pytest thagid/tests/test_brainstorm.py thagid/tests/test_internal.py` or the full backend suite if practical.
- [x] Run `rtk npm run check` from `web/`; run `rtk npm run test:unit` if frontend tests are added.

### Review Findings

- [x] [Review][Patch] URL fetch failure still mutates checkpoint state [agent/main.py:479]
- [x] [Review][Patch] DNS rebinding can bypass the SSRF preflight [agent/url_context.py:68]
- [x] [Review][Patch] URL fetch has no total deadline for slow streams [agent/url_context.py:102]
- [x] [Review][Patch] Synchronous DNS resolution can block the async worker [agent/url_context.py:68]
- [x] [Review][Patch] Malformed URL ports escape the expected fetch-error path [agent/url_context.py:42]
- [x] [Review][Patch] Required SSRF and redirect tests are incomplete [agent/tests/test_brainstorm.py:1991]
- [x] [Review][Patch] Valid public IPv6 URL literals are rejected [agent/url_context.py:60]

## Dev Notes

### Scope Boundaries

- This story implements URL sharing and text extraction during the existing Facilitate phase only.
- Do not implement visual document ingestion, PDFs, DOCX, images, authenticated pages, JavaScript-rendered scraping, bookmark previews, URL metadata cards, or crawling multiple pages.
- Do not implement Epic 3 KG ContextChunk writes. URL context chunks live only in checkpoint `state["active_documents"]` until extraction/KG stories write them later.
- Do not add a general crawler, storage service, database attachment table, cache table, queue, or migration for this MVP story.
- Do not introduce new libraries unless explicitly approved. Existing `httpx`, Python stdlib URL parsing, `socket`, `ipaddress`, and a small HTML text extraction helper are sufficient for the prototype.

### Current Codebase State

- `ChatInterface.svelte` already supports one pending text file, a hidden file input, a paperclip button enabled only during Facilitate, file validation to `.md/.txt/.csv/.json`, pending file chips, and failure-safe retention.
- `ChatInterface.svelte` currently has no URL/link button, URL input popover, pending URL state, or URL chip rendering.
- `ChatBubble.svelte` currently renders optimistic `message.files` chips for user messages only. It does not render URL chips yet.
- `web/src/routes/project/[id]/package/[pkgId]/+page.svelte` sends file attachments through `sendBrainstormMessage(pkgId, content, brainstormSessionId, files)` and blocks files outside Facilitate.
- `web/src/lib/api/brainstorm.ts` currently serializes `{ content, session_id, files }` through `apiFetch`; add `urls` without breaking existing call sites.
- `BrainstormMessageCreate` currently has `content`, optional `session_id`, and `files: list[BrainstormFileAttachment]` with max length `1`.
- `thagid/services/brainstorm.py` persists only user/assistant message text and forwards file model dumps to `agent_client`. Keep that pattern for URLs.
- `agent/main.py` currently implements file ingestion in-place with `_append_active_file_documents`, deterministic file summaries, Facilitate-only guard, and active document checkpoint mutation.
- `agent/checkpoint.py` merges `active_documents` by `(source_type, source_ref, content_hash or content)` and preserves concurrent ideas/summary state.
- `agent/summary.py` already includes active document refs in rolling summaries through `source`, `name`, `title`, or `id`; URL chunks should include fields that summary can identify, preferably `source_ref` and `summary`. If necessary, update `_document_refs` to read `source_ref`.

### Required Implementation Behavior

- URL attachment state is pending UI state until send. Removing a URL chip before send must prevent that URL from being sent.
- Pending URL chips are cleared only after successful send. On send failure, restore the pending URL so the user can retry.
- Sent URL chips are current-session UI state only for this story. The persisted transcript must remain readable through deterministic message text such as `Shared URL: https://example.com/page` and the assistant acknowledgement.
- The browser must never call `thagid-agent` directly and should not fetch external URLs. Browser calls FastAPI; FastAPI forwards URL metadata to the agent; the agent fetches externally with guardrails.
- The agent must store successful URL context chunks in checkpoint `active_documents`, not in `ideas`, `themes`, `summary`, or the messages table.
- URL chunks should use stable fields: `id`, `source_type`, `source_ref`, `content`, and `summary`; optional `content_hash` is acceptable and helps dedupe.
- Fetch/extraction failure should not end the brainstorm session, should not mutate `active_documents`, and should preserve existing `ideas`, `themes`, `summary`, `technique`, `phase`, message counters, and existing documents.
- For failure turns, append normal user/assistant messages only if that matches current brainstorm error semantics. Do not partially save fetched content on failure.
- If the URL is sent with ideation text and fetch succeeds, process the ideation text through Story 2.3 idea extraction/reduction in the same turn.
- If the URL is sent with ideation text and fetch fails, the assistant should report the URL problem but the session should continue; preserve existing ideas and technique state.

### URL Fetching And Extraction Guardrails

- Use `urllib.parse.urlparse` for initial validation and canonicalization.
- Use stdlib `socket.getaddrinfo` plus `ipaddress.ip_address` to reject unsafe network targets before fetching.
- Treat DNS resolution failures, timeouts, oversized responses, unsupported content type, empty extracted text, and unsafe redirects as recoverable URL ingestion failures.
- Use no user credentials, cookies, or auth headers. A generic user-agent header is acceptable if needed for basic compatibility.
- Bound response processing. Do not load unbounded response bodies into memory; if streaming is practical, stop once the configured max bytes is exceeded.
- HTML extraction should remove scripts/styles and tags deterministically. Do not run JavaScript and do not attempt browser automation.
- Summary should be deterministic, for example domain plus first non-empty extracted line and line/character count. Do not add an LLM call for URL summarization.

### UX Requirements

- Follow `design-system/thagid/MASTER.md` and `design-system/thagid/pages/package-chat.md` because this story edits chat UI.
- Link action: ghost button, `w-9 h-9`, Lucide `link`, accessible label such as `Share URL` or `Share URL (available during Facilitate)` when disabled.
- URL popover: compact input plus Add button; visible focus ring; `type="url"`; invalid values should show a toast and remain editable.
- Pending URL chip: `bg-blue-50 rounded-lg px-3 py-1.5`, link icon, domain text in primary color, truncate to max width, remove button with `aria-label="Remove {domain}"` or `Remove URL {url}`.
- Sent URL chip: same visual treatment where practical, rendered with the optimistic user message in the current session only.
- File and URL controls should sit left of the textarea. Preserve no horizontal scroll and desktop-only layout.
- URL controls are enabled only during `brainstormPhase === 'facilitate'` and disabled during initiate, extract, validate, markdown, concluded, no active brainstorm, and sending.
- Preserve visible focus rings, no emoji icons, reduced-motion behavior, current chat bubble distinctions, and existing file chip styling.

### Backend And Agent Contract Guardrails

- Keep JSON request/response compatibility. Existing callers that omit `urls` must continue working unchanged.
- Do not expose internal `/internal/agent/...` endpoints to the browser.
- `X-Agent-Key` remains required for backend-to-agent calls.
- Continue using `verify_package_access` before forwarding brainstorm requests.
- Do not leak SQLAlchemy models in API responses; use Pydantic schemas.
- Do not import `thagid.*` backend services/models into `agent/`; container boundary remains strict.
- If active documents are ever added to browser-facing responses, make them defaulted and validated. They are not needed for UI in this story.

### Architecture And Product Context

- PRD FR11/FR13/FR33 require sharing URLs during brainstorm and extracting text content from shared URLs.
- UX-DR13 requires link action, URL popover, pending URL chips, removable pending state, and attached-URL display in sent messages.
- UX-DR14 requires file and URL attachment controls disabled outside Facilitate.
- Architecture defines `active_documents: list[ContextChunk]` in brainstorm state and `share_url(url)` as a Facilitate tool that fetches URL content, creates a ContextChunk, and adds it to active documents.
- Architecture also defines future KG `ContextChunk` nodes, but this story should only populate checkpoint state so Epic 3 can later write chunks to KG.

### Previous Story Intelligence

- Story 2.5 is in review and implemented JSON-based file attachment contracts across frontend, FastAPI, and agent boundaries with one-file and 256 KiB UTF-8 content validation.
- Story 2.5 added package chat paperclip upload UI, pending/removable file chips, file-only send transcript text, optimistic sent-file chips, and pending file retention on send failure.
- Story 2.5 added agent active document ingestion for Facilitate phase with deterministic summaries, normalized content, duplicate suppression, acknowledgement replies, and active document checkpoint merge preservation.
- Story 2.4 is done and implemented deterministic rolling summary state with `message_count_total`, `summarized_message_count`, checkpoint message compaction, and bounded facilitation context. URL ingestion must preserve those counters and active document references.
- Story 2.3 is done and implemented deterministic structured idea extraction, cumulative idea state, `IdeaCard`, backend/frontend `ideas` response fields, duplicate reduction, contradiction handling, and anti-bias pivoting.
- Story 2.2 implemented technique picker and facilitate-phase technique swaps. The picker sends `Use {technique_name}` through the same brainstorm message path.
- Story 2.1 established `SCAMPER Method` fallback and exact technique matching for initiate-phase selection.
- Story 1.4 established displayed transcript persistence in `messages` and agent continuity in `agent_checkpoints`.
- Recent git history includes `feat: add brainstorm idea management and summaries`, `feat: add technique picker and swaps`, `feat: recommend brainstorm techniques`, `fix: align brainstorm chat accessibility`, and `fix: harden brainstorm resume checkpoints`.

### File Structure Requirements

- Likely frontend updates: `web/src/lib/types/brainstorm.ts`, `web/src/lib/types/message.ts`, `web/src/lib/api/brainstorm.ts`, `web/src/routes/project/[id]/package/[pkgId]/+page.svelte`, `web/src/lib/components/custom/ChatInterface.svelte`, `web/src/lib/components/custom/ChatBubble.svelte`, and `web/src/lib/components/custom/ChatInterface.test.ts`.
- Likely backend updates: `thagid/schemas/brainstorm.py`, `thagid/services/brainstorm.py`, `thagid/services/agent_client.py`, `thagid/routers/brainstorm.py` only if route wiring needs explicit URL data handling, and `thagid/tests/test_brainstorm.py`.
- Likely agent updates: `agent/main.py`, `agent/tests/test_brainstorm.py`, and optionally a small helper module such as `agent/url_context.py` if URL validation/fetch/extraction makes `main.py` too large.
- Possible summary helper update: `agent/summary.py` if URL context chunks need `source_ref` support in document references.
- Possible checkpoint update: `agent/checkpoint.py` only if URL dedupe needs `content_hash`; do not break existing file document merge behavior.
- Avoid modifying shadcn-managed files under `web/src/lib/components/ui/`.
- Avoid migrations and new database models.

### Testing Requirements

- Build agent URL tests in `agent/tests/test_brainstorm.py`, near existing Story 2.5 file ingestion tests.
- Mock URL fetching in tests; do not hit the public internet.
- Add an agent test where a Facilitate session receives one safe URL, extracts text, saves one active document chunk with `source_type: "url"`, keeps phase `facilitate`, and replies with `I've pulled content from`.
- Add an agent test where a URL plus ideation text both appends active document and preserves Story 2.3 idea extraction.
- Add agent tests for fetch failure, unsupported content type, empty extraction, unsafe scheme, localhost/private IP, and unsafe redirect if practical.
- Add backend tests proving `urls` are forwarded to `agent_client.agent_brainstorm_message` and invalid URLs return validation errors before agent call.
- Add frontend tests for URL popover add/remove, disabled link button outside Facilitate, URL-only send, optimistic URL chip display, and pending URL restoration after send failure if current Svelte Testing Library setup supports it.
- Run the verification commands listed in Tasks.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-2.6-URL-Context-Ingestion]
- [Source: _bmad-output/planning-artifacts/prd.md#Brainstorm-Ideation]
- [Source: _bmad-output/planning-artifacts/prd.md#Frontend-Chat-Interface]
- [Source: _bmad-output/planning-artifacts/architecture.md#LangGraph-State-Machine]
- [Source: _bmad-output/planning-artifacts/architecture.md#Agent-Backend-HTTP-Contract]
- [Source: _bmad-output/planning-artifacts/architecture.md#Architectural-Boundaries]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#URL-Sharing-FR11-FR13]
- [Source: design-system/thagid/MASTER.md#Chat-Input]
- [Source: design-system/thagid/MASTER.md#FileURL-Attachment-Chips]
- [Source: design-system/thagid/pages/package-chat.md#URL-Sharing]
- [Source: _bmad-output/implementation-artifacts/2-5-text-file-context-ingestion.md#Completion-Notes-List]

## Project Structure Notes

- The architecture target names this as a future `share_url` tool, but the current prototype still routes brainstorm behavior through `agent/main.py`. Extend the current prototype unless a tiny helper module is needed for URL safety/extraction clarity.
- Story 2.5 established JSON attachment payloads and active document checkpoint chunks. Reuse that pattern instead of building upload/storage infrastructure.
- URL fetching must happen server-side in the agent with SSRF guardrails; browser-side fetching would be blocked by CORS and would bypass the architecture boundary.
- Active context chunks are checkpoint state only in this story. Epic 3 owns KG ContextChunk nodes and relationships.
- Latest technical research was not required because this story can use existing `httpx`, FastAPI/Pydantic, Svelte, and Python stdlib primitives without adding dependencies.

## Dev Agent Record

### Agent Model Used

gpt-5.5

### Debug Log References

- `rtk pytest agent/tests/test_brainstorm.py` - 79 passed.
- `rtk pytest thagid/tests/test_brainstorm.py thagid/tests/test_internal.py` - 50 passed.
- `rtk npm run check` - 0 errors, 0 warnings.
- `rtk npm run test:unit` - 8 files passed, 33 tests passed.
- `rtk pytest` - 203 passed.

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created.
- Added JSON URL attachment contracts across frontend, FastAPI, backend agent client, and agent request validation while preserving existing file attachment callers.
- Added package chat URL sharing UI, pending/removable URL chips, URL-only sends in Facilitate, optimistic sent URL chips, mixed attachment prevention, and pending URL retention on send failure.
- Added agent-side URL fetching/extraction with stdlib SSRF guardrails, bounded downloads, text-like content filtering, deterministic HTML/text extraction, URL active document chunks, deduplication, and concise success/failure acknowledgements.
- Added focused agent, backend, agent-client, and frontend tests covering URL forwarding, validation, UI behavior, successful ingestion, dedupe, failure handling, and SSRF rejection.
- Addressed code review findings for URL failure checkpoint preservation, DNS-safe connection handling, async DNS resolution, total fetch deadlines, invalid port handling, IPv6 literals, and SSRF redirect coverage.

### File List

- `_bmad-output/implementation-artifacts/2-6-url-context-ingestion.md`
- `_bmad-output/implementation-artifacts/sprint-status.yaml`
- `agent/main.py`
- `agent/url_context.py`
- `agent/tests/test_brainstorm.py`
- `thagid/routers/brainstorm.py`
- `thagid/schemas/brainstorm.py`
- `thagid/services/agent_client.py`
- `thagid/services/brainstorm.py`
- `thagid/tests/test_agent_client.py`
- `thagid/tests/test_brainstorm.py`
- `web/src/lib/api/brainstorm.ts`
- `web/src/lib/components/custom/ChatBubble.svelte`
- `web/src/lib/components/custom/ChatInterface.svelte`
- `web/src/lib/components/custom/ChatInterface.test.ts`
- `web/src/lib/types/brainstorm.ts`
- `web/src/lib/types/message.ts`
- `web/src/routes/project/[id]/package/[pkgId]/+page.svelte`

### Change Log

- 2026-05-11: Implemented URL context ingestion and moved story to review.
