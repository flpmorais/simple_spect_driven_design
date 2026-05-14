# Story 2.5: Text File Context Ingestion

Status: done

<!-- Note: Validation is optional. Run validate-create-story for quality check before dev-story. -->

## Story

As a package user,
I want to upload text-based files during brainstorm facilitation,
so that existing notes can influence ideation without manual copy-paste.

## Acceptance Criteria

1. Given the session is in Facilitate phase, when I select a supported text file from the chat input, then the file appears as a removable pending attachment chip, and it is sent with my next message.
2. Given a file attachment is sent, when the agent processes the message, then it extracts text content into an active context chunk, and acknowledges the file in chat with a concise summary.
3. Given the session is not in Facilitate phase, when the chat input renders, then file upload controls are disabled, and the disabled state is visually and programmatically clear.

## Tasks / Subtasks

- [x] Define a minimal text-file attachment contract (AC: 1, 2)
  - [x] Add a `BrainstormFileAttachment` shape in backend/frontend/agent contracts with `filename`, `content_type`, `size`, and `content` string fields.
  - [x] Keep the existing JSON `POST /api/packages/{package_id}/brainstorm/message` path; do not add multipart upload plumbing for this MVP story.
  - [x] Use browser `File.text()` to read supported text files before calling the existing API helper.
  - [x] Support only `.md`, `.txt`, `.csv`, and `.json` extensions for this story.
  - [x] Allow exactly one pending/sent file for this story. Use a list field for forward compatibility, but enforce max length `1` in UI, backend schema, and agent boundary tests.
  - [x] Add `BRAINSTORM_FILE_MAX_BYTES = 262_144` (256 KiB) as the explicit MVP limit. Validate actual UTF-8 content byte length, not only the browser-provided `File.size` or client-provided `size` field.
  - [x] Preserve existing brainstorm response fields: `message`, `session_id`, `phase`, `technique`, `idea_count`, `message_count`, and `ideas`.
- [x] Extend browser brainstorm API and page state for file attachments (AC: 1)
  - [x] Update `web/src/lib/types/brainstorm.ts` with the attachment type.
  - [x] Update `web/src/lib/api/brainstorm.ts` so `sendBrainstormMessage` can include `files` while preserving existing callers.
  - [x] Update `web/src/routes/project/[id]/package/[pkgId]/+page.svelte` so `sendChatMessage` accepts file attachments and passes them only through the brainstorm path.
  - [x] If the user sends a file with no typed message, send a deterministic transcript content such as `Uploaded file: {filename}` rather than relaxing the persisted `messages.content` non-null/non-blank assumptions.
  - [x] On send failure, restore pending file state and remove only the optimistic user message, matching the current rollback behavior.
- [x] Add file attachment UI in package chat (AC: 1, 3, UX-DR12, UX-DR14)
  - [x] Update `ChatInterface.svelte` with a paperclip ghost icon button (`Paperclip` from lucide-svelte) left of the textarea.
  - [x] Add a hidden file input using accepted extensions `.md,.txt,.csv,.json` and trigger it from the paperclip button.
  - [x] Do not enable `multiple` on the file input in this story.
  - [x] Show pending files as removable chips above the textarea using `bg-slate-100`, filename text, file icon, and `x` remove button.
  - [x] Render a sent-file chip on the optimistic current-session user message after send. This chip may be transient and does not need to survive reload; the generated transcript content must still mention the uploaded filename for reload readability.
  - [x] Allow send when either trimmed text exists or at least one pending file exists, but only during `facilitate` for file-only sends.
  - [x] Disable the paperclip control outside `brainstormPhase === 'facilitate'`, during send, and when no brainstorm session is active.
  - [x] Disabled state must be visually clear and programmatic: `disabled`, accessible label, and no file dialog opening.
  - [x] Drag-and-drop upload is explicitly out of scope for this story even though the design-system mentions it; implement paperclip/native file selection only.
  - [x] Preserve Enter/Shift+Enter behavior, auto-scroll, `role="log"`, `aria-live="polite"`, reduced-motion handling, technique picker, idea cards, phase badge, and message counts.
  - [x] Do not implement URL chips or URL popover in this story; that is Story 2.6.
- [x] Validate and forward file attachments in FastAPI (AC: 1, 2)
  - [x] Extend `BrainstormMessageCreate` in `thagid/schemas/brainstorm.py` to accept `files: list[BrainstormFileAttachment] = []`.
  - [x] Keep existing content validation for no-file messages. Allow generated or explicit content for file messages; do not persist a blank user message.
  - [x] Validate supported extension, content string, filename presence, and configured size limit.
  - [x] Return normal FastAPI/Pydantic 422 validation errors for unsupported extension, empty content, oversized content, or more than one file before calling the agent.
  - [x] Update `thagid/services/brainstorm.py` and `thagid/services/agent_client.py` to forward files to the agent in the existing JSON payload.
  - [x] Continue verifying package access in `thagid/routers/brainstorm.py` before forwarding anything to the agent.
  - [x] Do not store uploaded file content in the `messages` table or add a migration in this story.
- [x] Ingest file content into agent checkpoint active documents (AC: 2)
  - [x] Extend `BrainstormMessageRequest` in `agent/main.py` to accept the same `files` list.
  - [x] Reject or ignore files when the loaded session phase is not `facilitate`; the user-facing frontend should prevent this, but the agent must guard the boundary.
  - [x] Convert each file into an active context chunk stored in `state["active_documents"]` with stable fields: `id`, `source_type: "file"`, `source_ref` filename, `content`, and a concise deterministic `summary`.
  - [x] Generate `id` as a UUID string; do not use integer IDs.
  - [x] Deduplicate active documents by filename plus content hash or exact filename/content match so resending the same file does not create avoidable duplicates.
  - [x] Keep `ideas`, `themes`, `summary`, `technique`, `phase`, and existing `active_documents` intact unless intentionally appending/merging file chunks.
  - [x] Include an acknowledgement in the assistant reply: `I've reviewed your file '{filename}'. {summary}`.
  - [x] If an ideation text message accompanies the file, preserve Story 2.3 idea extraction/reducer behavior in the same turn.
- [x] Keep file content bounded and deterministic (AC: 2)
  - [x] Implement deterministic text summary from content, such as first non-empty line plus line/character count; do not introduce an LLM call for file summarization in this story.
  - [x] Normalize line endings and trim surrounding whitespace before storing content.
  - [x] Reject empty files with a clear validation error before agent processing.
  - [x] Keep unsupported binary/visual files out of scope; images, PDFs, DOCX, and PPT belong to deferred visual/document ingestion work.
  - [x] Frontend validation failures should show a toast and must not add an optimistic message. Backend validation failures after send must rollback the optimistic message and restore the pending file.
- [x] Preserve prior brainstorm behavior (AC: 1, 2, 3)
  - [x] Technique recommendation, technique picker, initiate selection, and facilitate-phase technique swaps still work.
  - [x] Story 2.3 idea extraction, duplicate reduction, contradiction handling, anti-bias pivoting, cumulative idea cards, status/resume, and checkpoint merge behavior still work.
  - [x] Regular non-brainstorm package chat still sends through `/api/packages/{package_id}/messages` and is unaffected by file attachment state.
  - [x] Story 2.4 rolling summary remains out of scope even if active documents increase context size.
- [x] Add focused tests and verification (AC: 1, 2, 3)
  - [x] Add agent tests for file ingestion during `facilitate`, active document chunk shape, acknowledgement text, deduplication, unsupported phase rejection/ignore behavior, and preserving existing ideas.
  - [x] Add backend tests for `BrainstormMessageCreate` file validation, forwarding files to the agent client, authenticated success, unauthenticated rejection, cross-org forbidden, unsupported extension, empty content, and oversized content.
  - [x] Add frontend tests for pending file chip rendering/removal, disabled paperclip outside Facilitate, file-only send behavior, accepted extensions, and rollback preserving pending files on send failure if practical.
  - [x] Run `rtk pytest agent/tests/test_brainstorm.py`.
  - [x] Run `rtk pytest thagid/tests/test_brainstorm.py thagid/tests/test_internal.py` or the full backend suite if practical.
  - [x] Run `rtk npm run check` from `web/`; run `rtk npm run test:unit` if frontend tests are added.

### Review Findings

- [x] [Review][Patch] Uploaded file content is stored but not clearly used to influence facilitation [`agent/main.py`:477]
- [x] [Review][Patch] Pending file state is not cleared on package navigation [`web/src/lib/components/custom/ChatInterface.svelte`:44]
- [x] [Review][Patch] Browser reads selected file before size rejection and does not handle `file.text()` failures [`web/src/lib/components/custom/ChatInterface.svelte`:123]
- [x] [Review][Patch] Rolling summary document refs do not use uploaded file filenames [`agent/summary.py`:118]
- [x] [Review][Patch] Agent file-size validation checks normalized content length instead of submitted UTF-8 content length [`agent/main.py`:322]

## Dev Notes

### Scope Boundaries

- This story implements text file upload and ingestion during the existing Facilitate phase only.
- Do not implement Story 2.6 URL sharing, URL chips, URL popover, URL fetching, or URL extraction.
- Do not implement Story 2.4 rolling summary, even though active documents add context. Keep content bounded and preserve existing summary state.
- Do not implement Epic 3 KG ContextChunk writes. Active context chunks live only in checkpoint `state["active_documents"]` until extraction/KG stories.
- Do not add a general file storage service, object storage, database attachment table, or migration for this MVP story.
- Do not introduce new libraries. Browser `File.text()`, existing JSON API calls, FastAPI/Pydantic validation, and current Svelte state are sufficient.

### Current Codebase State

- `ChatInterface.svelte` currently renders the chat header, technique picker button, technique pill, idea/message counts, phase badge, cumulative idea cards, chat log, textarea, and send button. It does not have file input, paperclip button, or pending attachment state.
- `web/src/routes/project/[id]/package/[pkgId]/+page.svelte` owns package chat state and sends brainstorm messages via `sendBrainstormMessage(pkgId, content, brainstormSessionId)`.
- `web/src/lib/api/brainstorm.ts` sends JSON `{ content, session_id }` through `apiFetch`; `apiFetch` sets `Content-Type: application/json` whenever a body exists.
- `BrainstormMessageCreate` currently has `content` and optional `session_id` only; content is non-blank.
- `thagid/services/agent_client.py` forwards only `message`, `package_id`, `project_id`, `session_id`, and context counts to `/internal/agent/brainstorm/message`.
- `agent/main.py` currently accepts only `message`, `package_id`, `project_id`, `session_id`, and `context` in `BrainstormMessageRequest`.
- `agent/main.py` already validates `active_documents` as a list and returns it to FastAPI, but browser-facing schemas do not currently expose `active_documents`.
- Story 2.3 added structured ideas in `agent/ideas.py` and cumulative `ideas` in backend/frontend contracts. Do not regress those fields.
- `Message.content` is non-null in `thagid/models/message.py`; avoid blank persisted messages.

### Required Implementation Behavior

- The upload is package-scoped and brainstorm-scoped. Browser still calls FastAPI; browser must never call `thagid-agent` directly.
- File attachment state is pending UI state until send. Removing a chip before send must prevent that file from being sent.
- Pending file chips are cleared only after successful send. On send failure, restore the pending files so the user can retry.
- Sent-file chips are current-session UI state only for this story. Do not add message-attachment persistence or a database migration; persist reload-readable file context through deterministic user/assistant message text and checkpoint `active_documents`.
- File-only sends are allowed in Facilitate. Generate deterministic transcript content if needed to satisfy existing backend validation and message persistence.
- Attachments must be sent only with the next brainstorm message. Do not keep stale pending files after a successful send or package navigation.
- The agent must store active context chunks in checkpoint `active_documents`, not in `ideas`, `themes`, `summary`, or the messages table.
- Active document chunk shape should be stable and future-KG-friendly: `id`, `source_type`, `source_ref`, `content`, `summary`.
- The agent acknowledgement must be concise and include the filename so the transcript is understandable after reload.
- File content should influence the current and future facilitation loop by existing in `active_documents`; if the user also sends text, the normal Story 2.3 idea extraction should still process the text.
- Unsupported file types, empty files, and oversized files should fail before checkpoint mutation.
- More than one pending/sent file is out of scope. If the user selects a second file before sending, replace the existing pending file or show a toast; do not send multiple files.

### UX Requirements

- Follow `design-system/thagid/MASTER.md` and `design-system/thagid/pages/package-chat.md` because this story edits chat UI.
- Paperclip action: ghost button, `w-9 h-9`, left of textarea, Lucide `paperclip`, accessible label such as `Attach text file`.
- Pending file chip: `bg-slate-100 rounded-lg px-3 py-1.5`, file icon, filename text truncated to max width, remove `x` button with `aria-label="Remove {filename}"`.
- Sent file chip: same visual treatment as pending file chip where practical, rendered with the optimistic user message in the current session only.
- Accepted formats shown/accepted: `.md`, `.txt`, `.csv`, `.json`.
- File upload controls are enabled only during `brainstormPhase === 'facilitate'` and disabled during initiate, extract, validate, markdown, concluded, no active brainstorm, and sending.
- Disabled controls must not open the native file picker and must be obvious to keyboard and screen-reader users.
- Preserve visible focus rings, no emoji icons, desktop-only layout, no horizontal scroll, reduced-motion behavior, and current chat bubble distinctions.

### Backend And Agent Contract Guardrails

- Keep JSON request/response compatibility. Existing callers that omit `files` must continue working unchanged.
- Do not expose internal `/internal/agent/...` or `/internal/backend/...` endpoints to the browser.
- `X-Agent-Key` remains required for backend-to-agent calls.
- Continue using `verify_package_access` before forwarding brainstorm requests.
- Do not store SQLAlchemy models in API responses; use Pydantic schemas.
- Do not import `thagid.*` backend services/models into `agent/`; container boundary remains strict.
- If active documents are added to browser-facing responses, make them defaulted and validated. If not needed for UI, keep them agent/internal only for this story.

### Architecture And Product Context

- PRD FR10/FR12/FR32 require text file upload during brainstorm and ingestion into ideation.
- UX-DR12 requires paperclip action, pending file chips, removable pending state, and attached-file display in sent messages.
- UX-DR14 requires file controls disabled outside Facilitate.
- Architecture defines `active_documents: list[ContextChunk]` in brainstorm state and `upload_file(file)` as a Facilitate tool that reads file content, creates a ContextChunk, and adds it to active documents.
- Architecture also defines future KG `ContextChunk` nodes, but this story should only populate checkpoint state so Epic 3 can later write chunks to KG.

### Previous Story Intelligence

- Story 2.3 is done and implemented deterministic structured idea extraction, cumulative idea state, `IdeaCard`, and backend/frontend `ideas` response fields.
- Story 2.3 explicitly kept `active_documents` unchanged; this story is the first one to mutate it.
- Story 2.3 checkpoint merge now preserves concurrent structured idea additions. If active documents can be appended concurrently, extend or test merge behavior so document chunks are not lost.
- Story 2.2 implemented technique picker and facilitate-phase technique swaps. The picker sends `Use {technique_name}` through the same brainstorm message path.
- Story 2.2 established that swaps preserve `ideas`, `themes`, `active_documents`, `summary`, messages, and phase.
- Story 2.1 established `SCAMPER Method` fallback and exact technique matching for initiate-phase selection.
- Story 2.4 is in review and implemented deterministic rolling summary state with `message_count_total`, `summarized_message_count`, checkpoint message compaction, and bounded facilitation context. File ingestion must preserve those summary counters and active document references.
- Story 1.4 established displayed transcript persistence in `messages` and agent continuity in `agent_checkpoints`.
- Recent git history includes `feat: add technique picker and swaps`, `feat: recommend brainstorm techniques`, `fix: align brainstorm chat accessibility`, `fix: harden brainstorm resume checkpoints`, and `feat: detect existing brainstorm sessions`.

### File Structure Requirements

- Likely frontend updates: `web/src/lib/types/brainstorm.ts`, `web/src/lib/api/brainstorm.ts`, `web/src/routes/project/[id]/package/[pkgId]/+page.svelte`, and `web/src/lib/components/custom/ChatInterface.svelte`.
- Likely backend updates: `thagid/schemas/brainstorm.py`, `thagid/services/brainstorm.py`, `thagid/services/agent_client.py`, `thagid/routers/brainstorm.py` only if route signature needs explicit file data handling, and `thagid/tests/test_brainstorm.py`.
- Likely agent updates: `agent/main.py`, possibly a small helper module for file validation/summarization if keeping it in `main.py` becomes unclear, and `agent/tests/test_brainstorm.py`.
- Possible checkpoint update: `agent/checkpoint.py` if active document concurrent merges need the same protection as messages/ideas.
- Avoid modifying shadcn-managed files under `web/src/lib/components/ui/`.
- Avoid migrations and new database models.

### Testing Requirements

- Agent tests should build on `agent/tests/test_brainstorm.py`, especially existing facilitate, active document preservation, technique swap, idea extraction, and checkpoint error tests.
- Add an agent test where a facilitate session receives one supported file, saves one active document chunk, keeps phase `facilitate`, and replies with `I've reviewed your file 'name.ext'.`.
- Add an agent test where a file plus ideation text both appends active document and preserves Story 2.3 idea extraction.
- Add an agent test for unsupported phase or unsupported file type that does not mutate checkpoint state.
- Add a backend test proving `files` are forwarded to `agent_client.agent_brainstorm_message` and invalid files return validation errors.
- Add frontend tests for pending chip rendering/removal and disabled paperclip outside Facilitate if current Svelte Testing Library setup supports it.
- Add frontend tests for sent-file chip display on successful optimistic send and pending-file restoration after send failure if current Svelte Testing Library setup supports it.
- Run the verification commands listed in Tasks.

### References

- [Source: _bmad-output/planning-artifacts/epics.md#Story-2.5-Text-File-Context-Ingestion]
- [Source: _bmad-output/planning-artifacts/prd.md#Brainstorm-Ideation]
- [Source: _bmad-output/planning-artifacts/prd.md#Frontend-Chat-Interface]
- [Source: _bmad-output/planning-artifacts/architecture.md#LangGraph-State-Machine]
- [Source: _bmad-output/planning-artifacts/architecture.md#Agent-Backend-HTTP-Contract]
- [Source: _bmad-output/planning-artifacts/ux-design-specification.md#File-Upload-FR10-FR12]
- [Source: design-system/thagid/pages/package-chat.md#Chat-Input-Area]
- [Source: design-system/thagid/pages/package-chat.md#File-Upload]
- [Source: _bmad-output/implementation-artifacts/2-3-facilitation-loop-with-real-time-idea-management.md#Completion-Notes-List]

## Project Structure Notes

- The architecture target names this as an `upload_file` tool in a future LangGraph structure, but the current implementation still routes all brainstorm behavior through `agent/main.py`. Extend the current prototype rather than creating the future tool folder.
- JSON text attachment is the smallest correct implementation because current `apiFetch` and brainstorm APIs are JSON-based. Multipart can be introduced later if binary/large-file storage becomes a requirement.
- Active context chunks are checkpoint state only in this story. Epic 3 owns KG ContextChunk nodes and relationships.
- Latest technical research was not required because this story uses existing browser/File APIs, FastAPI/Pydantic, and Svelte patterns already in the project.

## Dev Agent Record

### Agent Model Used

gpt-5.5 (OpenCode)

### Debug Log References

- Red phase: `rtk pytest agent/tests/test_brainstorm.py -q` failed on missing file ingestion/phase guard as expected.
- Red phase: `rtk pytest thagid/tests/test_brainstorm.py -q` failed on missing file forwarding/validation as expected.
- Red phase: `rtk npm run test:unit -- ChatInterface.test.ts` failed on missing file UI controls as expected.
- Green phase: `rtk pytest agent/tests/test_brainstorm.py -q` passed (67 tests).
- Green phase: `rtk pytest thagid/tests/test_brainstorm.py thagid/tests/test_internal.py -q` passed (46 tests).
- Green phase: `rtk npm run check` passed with 0 errors and 0 warnings.
- Green phase: `rtk npm run test:unit` passed (8 files, 24 tests).

### Completion Notes List

- Ultimate context engine analysis completed - comprehensive developer guide created.
- Implemented JSON-based text file attachment contracts across frontend, FastAPI, and agent boundaries with one-file and 256 KiB UTF-8 content validation.
- Added package chat paperclip upload UI, pending/removable file chips, file-only send transcript text, optimistic sent-file chips, and failure-safe pending file retention.
- Added agent active document ingestion for Facilitate phase with deterministic summaries, normalized content, duplicate suppression, acknowledgement replies, and active document checkpoint merge preservation.
- Preserved regular package chat and existing brainstorm response fields/idea extraction/technique flows.

### File List

- _bmad-output/implementation-artifacts/2-5-text-file-context-ingestion.md
- _bmad-output/implementation-artifacts/sprint-status.yaml
- agent/checkpoint.py
- agent/main.py
- agent/tests/test_brainstorm.py
- thagid/routers/brainstorm.py
- thagid/schemas/brainstorm.py
- thagid/services/agent_client.py
- thagid/services/brainstorm.py
- thagid/tests/test_brainstorm.py
- web/src/lib/api/brainstorm.ts
- web/src/lib/components/custom/ChatBubble.svelte
- web/src/lib/components/custom/ChatInterface.svelte
- web/src/lib/components/custom/ChatInterface.test.ts
- web/src/lib/types/brainstorm.ts
- web/src/lib/types/message.ts
- web/src/routes/project/[id]/package/[pkgId]/+page.svelte

### Change Log

- 2026-05-11: Implemented Story 2.5 text file context ingestion and marked ready for review.
