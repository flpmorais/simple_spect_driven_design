---
stepsCompleted:
  - step-01-validate-prerequisites
  - step-02-design-epics
  - step-03-create-stories
  - step-04-final-validation
inputDocuments:
  - _bmad-output/planning-artifacts/prd.md
  - _bmad-output/planning-artifacts/architecture.md
  - _bmad-output/planning-artifacts/ux-design-specification.md
---

# Thagid - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for Thagid, decomposing the requirements from the PRD, UX Design if it exists, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR1: User can start a brainstorm session within a package.

FR2: User can abandon a brainstorm session and resume it later with full state preserved.

FR3: System can detect an existing brainstorm session for a package and offer to continue it.

FR4: User can conclude a brainstorm session by indicating completion.

FR5: System persists session state (messages, ideas, active technique, documents) across sessions.

FR6: System can recommend brainstorming techniques based on the package description.

FR7: User can accept, adjust, or replace recommended techniques.

FR8: User can swap techniques mid-session without losing existing ideas.

FR9: User can browse all available techniques (62) via a technique picker.

FR10: User can upload text-based files during a brainstorm session.

FR11: User can share URLs during a brainstorm session.

FR12: System can ingest uploaded files and incorporate their content into ideation.

FR13: System can fetch and extract text content from shared URLs.

FR14: System maintains a real-time list of ideas during facilitation, resolving duplicates and contradictions as they arise.

FR15: System applies anti-bias domain pivoting during ideation to prevent semantic clustering.

FR16: System maintains a rolling summary of earlier conversation to keep context bounded.

FR17: System can present all ideas grouped into themes to the user before conclusion.

FR18: User can review and adjust theme groupings before finalizing.

FR19: System can extract a session summary and key insights from the finalized brainstorm state.

FR20: System can validate extracted data for completeness and structural correctness.

FR21: System can write session, theme, idea, and context chunk data as atomic nodes to the knowledge graph.

FR22: System can render BMAD-compatible markdown from the structured brainstorm data.

FR23: System can compute embeddings for ideas asynchronously on write to the knowledge graph.

FR24: System can store atomic graph nodes with typed relationships (Session, Theme, Idea, ContextChunk).

FR25: System can version nodes - every update creates a new version with agent and change metadata.

FR26: System supports multi-tenant scoping (organization -> project -> graph).

FR27: System exposes a domain-specific API for knowledge graph operations - agents never write Cypher/SQL directly.

FR28: System can retrieve ideas by theme membership.

FR29: System can retrieve ideas by vector similarity search.

FR30: System can retrieve session metadata and summary.

FR31: User can interact with the brainstorm agent through a text chat within a package.

FR32: User can upload files via the chat interface.

FR33: User can share URLs via the chat interface.

FR34: User can see a brainstorm summary card on the package dashboard showing session date, technique count, and idea count.

FR35: User can drill into a brainstorm detail tab showing ideas grouped by theme, session metadata, and key insights.

FR36: User can browse themes and drill into specific ideas within the detail tab.

### NonFunctional Requirements

NFR1: Facilitator token overhead per turn stays within approximately 3.5K-7.7K tokens (system prompt + technique + ideas + summary + messages).

NFR2: Chat responses return within the LLM provider's standard response time, with no additional processing bottleneck.

NFR3: Embedding computation is asynchronous and must not block node writes to the knowledge graph.

NFR4: Rolling summarization triggers every approximately 20 messages without disrupting the facilitation loop.

NFR5: System handles LLM API failures with standard retry logic.

NFR6: Knowledge graph operates within the existing PostgreSQL container infrastructure.

NFR7: Brainstorm agent is compatible with the existing package chat interface (SvelteKit frontend).

### Additional Requirements

- Build a custom PostgreSQL 16 image with Apache AGE and pgvector installed in the existing PostgreSQL container topology.

- Initialize PostgreSQL extensions with `CREATE EXTENSION IF NOT EXISTS age`, `CREATE EXTENSION IF NOT EXISTS vector`, `LOAD 'age'`, and the required AGE search path.

- Add Python dependencies for `langgraph>=1.1.10`, `pgvector>=0.4.2`, and LangGraph PostgreSQL checkpointing.

- Run the brainstorm agent in a separate `thagid-agent` container with its own FastAPI app and internal HTTP communication to the backend.

- Use Apache AGE graph namespaces named `project_{normalized_project_id}` with Session, Theme, Idea, and ContextChunk node labels.

- Store embeddings in relational pgvector tables separate from AGE graph node properties, with `vector(1536)` columns and HNSW cosine indexes.

- Implement `KnowledgeGraphService` in `thagid/services/knowledge_graph.py` with domain-specific methods for graph lifecycle, session writes, theme writes, idea writes, context chunk writes, retrieval, vector search, and node versioning.

- Expose agent-called KG endpoints under `/internal/kg/projects/{project_id}/...` and browser-facing brainstorm endpoints under `/api/packages/{package_id}/brainstorm/...`.

- Authenticate agent-to-backend calls with an internal `X-Agent-Key` shared secret; keep user-facing endpoints JWT-authenticated.

- Implement LangGraph state with package_id, technique, messages, ideas, themes, active_documents, summary, and session_id.

- Implement the LangGraph topology START -> initiate -> facilitate -> extract -> validate -> markdown -> END, including validation retry routing back to facilitation when needed.

- Implement facilitate tools for `swap_technique`, `upload_file`, `share_url`, and `conclude_session`.

- Persist LangGraph checkpoints in PostgreSQL under a separate `agent_checkpoints` schema.

- Render BMAD-compatible markdown using deterministic Python code from structured brainstorm data, not freeform LLM output.

- Use OpenAI `text-embedding-3-small` with 1536 dimensions for idea and chunk embeddings.

- Add development compose services for pgAdmin and Apache AGE Viewer for database and graph inspection.

- Follow the defined project structure: `agent/` package for the brainstorm agent, new backend files under `thagid/services`, `thagid/routers`, `thagid/schemas`, and `thagid/models`, and frontend additions under `web/src/lib`.

- Parameterize all AGE Cypher queries; never interpolate values directly into Cypher strings.

- Preserve container boundaries: the agent calls the backend through HTTP and never imports from the `thagid` backend package directly.

### UX Design Requirements

UX-DR1: Implement package chat as the defining workspace with a sticky chat header, scrollable message log, sticky bottom textarea, send button, and auto-scroll to latest message.

UX-DR2: Preserve always-visible scope clarity through top-bar breadcrumbs and scope-aware sidebar state for organization, project, and package navigation.

UX-DR3: Implement breadcrumb dropdowns with search, current item indication, create action, keyboard navigation, Escape-to-close, and accessible list semantics.

UX-DR4: Implement scope-aware sidebar content switching between organization and project scope, with active item highlighting and section labels.

UX-DR5: Implement empty states with centered Lucide icon, heading, description, and single CTA for organization/project/package list gaps.

UX-DR6: Implement StatusBadge variants for package statuses: new, planning, in-progress, finished, released, and cancelled.

UX-DR7: Implement BrainstormPhaseBadge variants for initiate, facilitate, extract, validate, markdown, and concluded phases.

UX-DR8: Implement ChatBubble variants for user and assistant messages, with right-aligned primary user bubbles and left-aligned neutral assistant bubbles.

UX-DR9: Implement StreamingIndicator with dot-pulse and streaming-text states for brainstorm responses.

UX-DR10: Implement TechniquePickerModal with searchable/filterable technique list, two-column detail panel, keyboard accessibility, and selection CTA.

UX-DR11: Implement inline technique recommendation cards with a "Use this" action and a browse-all path to the technique picker.

UX-DR12: Implement file upload interaction in chat using a paperclip action, pending file chips, removable pending state, and attached-file display in sent messages.

UX-DR13: Implement URL sharing interaction in chat using a link action, URL popover, pending URL chips, removable pending state, and attached-URL display in sent messages.

UX-DR14: Disable file and URL attachment controls outside the Facilitate phase.

UX-DR15: Implement IdeaCard with title, description, category tag, novelty indicator, inline and detail variants, and article accessibility semantics.

UX-DR16: Implement ThemeCard with collapsible header, idea count, idea list, and `aria-expanded` behavior.

UX-DR17: Implement theme grouping review flow where user says done, agent presents grouped theme cards, user can request adjustments, and user can confirm final groupings.

UX-DR18: Implement BrainstormSummaryCard on the project dashboard for concluded sessions, showing date, technique count, idea count, theme pills, and View Details link.

UX-DR19: Implement brainstorm detail view with session summary, key insights, collapsible theme cards, idea browsing, and return-to-package navigation.

UX-DR20: Follow the Thagid design system tokens: Plus Jakarta Sans, navy primary, neutral slate surfaces, 4px spacing base, shadcn-svelte components, and Lucide icons.

UX-DR21: Enforce desktop-only MVP constraints with minimum 1024px viewport support and no mobile or tablet-specific responsive layouts.

UX-DR22: Implement accessibility requirements: WCAG AA contrast, visible focus rings, semantic landmarks, keyboard navigation, screen reader labels, and `prefers-reduced-motion` support.

UX-DR23: Implement form patterns with max-w-lg centered layout, label/input/helper order, inline validation, and right-aligned CTA with secondary cancel.

UX-DR24: Implement feedback patterns for create/save success toasts, inline form validation errors, network error toasts, skeleton loading, chat bubble animation, phase badge transitions, and invisible session checkpointing.

UX-DR25: Implement project dashboard package and brainstorm entry points so concluded brainstorm sessions are discoverable from package rows and detail pages.

### FR Coverage Map

FR1: Epic 1 - Brainstorm session workspace start.

FR2: Epic 1 - Session abandonment and resume.

FR3: Epic 1 - Existing session detection.

FR4: Epic 3 - User-triggered brainstorm conclusion.

FR5: Epic 1 - Persisted brainstorm session state.

FR6: Epic 2 - Technique recommendation.

FR7: Epic 2 - Technique acceptance, adjustment, or replacement.

FR8: Epic 2 - Mid-session technique swapping.

FR9: Epic 2 - Technique picker for all available techniques.

FR10: Epic 2 - Text file upload during brainstorm.

FR11: Epic 2 - URL sharing during brainstorm.

FR12: Epic 2 - Uploaded file ingestion into ideation.

FR13: Epic 2 - Shared URL text extraction.

FR14: Epic 2 - Real-time idea list management.

FR15: Epic 2 - Anti-bias domain pivoting.

FR16: Epic 2 - Rolling conversation summary.

FR17: Epic 3 - Theme grouping presentation.

FR18: Epic 3 - Theme grouping review and adjustment.

FR19: Epic 3 - Session summary and key insight extraction.

FR20: Epic 3 - Extracted data validation.

FR21: Epic 3 - Atomic KG writes for session, themes, ideas, and context chunks.

FR22: Epic 3 - BMAD-compatible markdown rendering.

FR23: Epic 3 - Async idea embedding computation.

FR24: Epic 3 - Atomic graph nodes and typed relationships.

FR25: Epic 3 - Node versioning and audit metadata.

FR26: Epic 3 - Multi-tenant organization/project/graph scoping.

FR27: Epic 3 - Domain-specific KG API.

FR28: Epic 4 - Retrieve ideas by theme membership.

FR29: Epic 4 - Retrieve ideas by vector similarity search.

FR30: Epic 4 - Retrieve session metadata and summary.

FR31: Epic 1 - Package chat interaction with brainstorm agent.

FR32: Epic 2 - File upload through chat interface.

FR33: Epic 2 - URL sharing through chat interface.

FR34: Epic 4 - Brainstorm summary card on package dashboard.

FR35: Epic 4 - Brainstorm detail tab.

FR36: Epic 4 - Theme and idea browsing.

## Epic List

### Epic 1: Brainstorm Session Workspace

Users can start, detect, abandon, and resume brainstorm sessions inside package chat with persisted state and a visible brainstorm mode.

**FRs covered:** FR1, FR2, FR3, FR5, FR31

### Epic 2: Guided Ideation and Context Ingestion

Users can choose brainstorming techniques, swap techniques mid-session, upload files, share URLs, and collaborate with the facilitator while ideas accumulate in bounded context.

**FRs covered:** FR6, FR7, FR8, FR9, FR10, FR11, FR12, FR13, FR14, FR15, FR16, FR32, FR33

### Epic 3: Structured Brainstorm Conclusion and Knowledge Capture

Users can conclude a brainstorm, review and adjust themed ideas, then generate validated structured knowledge and BMAD-compatible markdown.

**FRs covered:** FR4, FR17, FR18, FR19, FR20, FR21, FR22, FR23, FR24, FR25, FR26, FR27

### Epic 4: Brainstorm Results Review and Retrieval

Users can revisit brainstorm outcomes through dashboards and detail views, browse themes and ideas, and retrieve stored brainstorm knowledge.

**FRs covered:** FR28, FR29, FR30, FR34, FR35, FR36

## Epic 1: Brainstorm Session Workspace

Users can start, detect, abandon, and resume brainstorm sessions inside package chat with persisted state and a visible brainstorm mode.

### Story 1.1: Brainstorm Runtime Foundation

As a platform maintainer,
I want the brainstorm runtime services available in local development,
So that package users can reach a stateful brainstorm agent through the existing application.

**Requirements Covered:** NFR6, Architecture runtime requirements

**Acceptance Criteria:**

**Given** the developer starts the compose stack
**When** the application services boot
**Then** PostgreSQL runs with AGE and pgvector available in the existing database container
**And** `thagid-agent` starts as a separate internal FastAPI service.

**Given** the backend needs to communicate with the brainstorm agent
**When** it sends an internal request to the agent service
**Then** the request uses the configured internal service URL and `X-Agent-Key`
**And** the agent rejects requests without a valid agent key.

**Given** the agent needs checkpoint storage
**When** the agent initializes
**Then** it can connect to PostgreSQL and use a dedicated checkpoint schema
**And** no frontend traffic goes directly to the agent container.

### Story 1.2: Start Brainstorm From Package Chat

As a package user,
I want to start a brainstorm session from package chat,
So that I can begin ideating without leaving the scoped package workspace.

**Requirements Covered:** FR1, FR31, NFR2, NFR7, UX-DR1, UX-DR7, UX-DR8, UX-DR9

**Acceptance Criteria:**

**Given** I am viewing an authenticated package chat
**When** I send a message that starts a brainstorm session
**Then** the frontend calls `/api/packages/{package_id}/brainstorm/message`
**And** the backend verifies package access before forwarding to the agent.

**Given** no active brainstorm session exists for the package
**When** the agent receives the first brainstorm message
**Then** it creates a new brainstorm state with package id, messages, empty ideas, empty documents, and no active technique
**And** the response includes a session id and current phase.

**Given** a brainstorm session has started
**When** the chat renders the agent response
**Then** the package chat shows brainstorm mode with the correct phase badge
**And** the message log remains accessible with `role="log"` and `aria-live="polite"`.

### Story 1.3: Detect Existing Brainstorm Session

As a returning package user,
I want the package chat to detect an existing brainstorm session,
So that I can continue work without guessing whether a session already exists.

**Requirements Covered:** FR3, UX-DR1, UX-DR24

**Acceptance Criteria:**

**Given** a package has an active brainstorm checkpoint
**When** I open the package chat
**Then** the frontend can request brainstorm status for that package
**And** the response identifies the active session id, phase, technique if any, idea count, and message count.

**Given** no active brainstorm session exists
**When** I open the package chat
**Then** the brainstorm status response indicates that no session is active
**And** the regular package chat remains usable.

**Given** the status request fails because the user lacks package access
**When** the backend validates the request
**Then** it returns the existing authorization error format
**And** no agent request is sent.

### Story 1.4: Resume Persisted Brainstorm State

As a returning package user,
I want an interrupted brainstorm session to resume exactly where it left off,
So that I do not lose ideation context when I leave and return later.

**Requirements Covered:** FR2, FR5, NFR4, UX-DR24

**Acceptance Criteria:**

**Given** I have an active brainstorm session with messages, ideas, active technique, documents, and summary state
**When** I leave and later reopen the package
**Then** the agent loads the latest checkpoint for that package session
**And** the chat reflects the persisted phase, message history, active technique, and idea count.

**Given** a brainstorm message is processed
**When** the agent response completes
**Then** the updated LangGraph state is checkpointed to PostgreSQL
**And** persistence happens without requiring a visible save button.

**Given** checkpoint loading fails unexpectedly
**When** the backend handles the brainstorm request
**Then** the user receives the standard error response
**And** the failure is logged without corrupting existing checkpoints.

### Story 1.5: Brainstorm Chat Shell UX Alignment

As a package user,
I want brainstorm mode to fit the existing Thagid chat shell,
So that I always understand my organization, project, package, and brainstorm state.

**Requirements Covered:** FR31, UX-DR2, UX-DR3, UX-DR4, UX-DR5, UX-DR6, UX-DR20, UX-DR21, UX-DR22, UX-DR23

**Acceptance Criteria:**

**Given** I am in package chat
**When** brainstorm mode is active
**Then** the top bar breadcrumbs and scope-aware sidebar continue to show the current organization, project, and package
**And** the active package remains highlighted in the sidebar.

**Given** I navigate with keyboard only
**When** I tab through breadcrumbs, sidebar, chat messages, and the input area
**Then** focus order follows visual order
**And** visible focus rings are present on all interactive elements.

**Given** reduced motion is enabled in the browser
**When** new brainstorm messages or phase badges render
**Then** animations are disabled or reduced according to `prefers-reduced-motion`
**And** the content remains readable and usable.

## Epic 2: Guided Ideation and Context Ingestion

Users can choose brainstorming techniques, swap techniques mid-session, upload files, share URLs, and collaborate with the facilitator while ideas accumulate in bounded context.

### Story 2.1: Technique Recommendation at Session Initiation

As a package user,
I want the brainstorm agent to recommend relevant techniques when a session begins,
So that I can start ideating with useful guidance instead of choosing blindly.

**Requirements Covered:** FR6, FR7, UX-DR11

**Acceptance Criteria:**

**Given** a brainstorm session enters the initiate phase
**When** the agent reads the package context available to it
**Then** it recommends one or more techniques with concise reasons
**And** the recommendation appears in the first brainstorm response.

**Given** recommended techniques are shown in chat
**When** I choose a recommendation
**Then** the selected technique is stored in brainstorm state
**And** the session can move into the facilitate phase.

**Given** the recommendation cannot be generated
**When** the agent handles the initiation
**Then** it falls back to a safe default technique
**And** explains that the user can change it.

### Story 2.2: Technique Picker and Mid-Session Swap

As a package user,
I want to browse and swap brainstorming techniques during facilitation,
So that I can change ideation direction without losing existing ideas.

**Requirements Covered:** FR8, FR9, UX-DR10, UX-DR11

**Acceptance Criteria:**

**Given** I open the technique picker
**When** the modal loads
**Then** I can search and filter the 62 available techniques
**And** selecting a technique shows its details before confirmation.

**Given** I select a technique from the picker
**When** I confirm selection
**Then** the modal closes, the active technique updates, and the agent acknowledges the change
**And** existing ideas remain in state.

**Given** I ask to swap techniques in natural language during facilitation
**When** the agent handles the request
**Then** it can call the swap technique tool
**And** the phase remains Facilitate.

### Story 2.3: Facilitation Loop With Real-Time Idea Management

As a package user,
I want the facilitator to build on my input and maintain ideas in real time,
So that the brainstorm feels productive and accumulates structured output.

**Requirements Covered:** FR14, FR15, NFR1, UX-DR15

**Acceptance Criteria:**

**Given** the session is in Facilitate phase
**When** I send an ideation message
**Then** the agent responds using the active technique
**And** any new ideas are added to brainstorm state with category, title, concept, and novelty.

**Given** a new idea duplicates or contradicts an existing idea
**When** the idea reducer processes it
**Then** it merges, updates, or preserves the idea consistently
**And** the resulting idea list contains no avoidable duplicates.

**Given** several similar ideas are accumulating
**When** the facilitator continues ideation
**Then** it applies anti-bias domain pivoting when appropriate
**And** prompts the user toward a different angle without discarding prior ideas.

### Story 2.4: Rolling Summary for Bounded Context

As a package user,
I want long brainstorm sessions to stay coherent without loading the full conversation every turn,
So that responses remain timely and context-aware.

**Requirements Covered:** FR16, NFR1, NFR4, NFR5

**Acceptance Criteria:**

**Given** a brainstorm session reaches the configured summary threshold of approximately 20 messages
**When** the next agent turn is processed
**Then** the agent updates the rolling summary
**And** preserves key decisions, active technique, documents, and important ideas.

**Given** the rolling summary exists
**When** the facilitator prepares a response
**Then** it uses the summary instead of relying on the full conversation history
**And** token overhead remains within the documented target range.

**Given** summary generation fails
**When** the agent handles the turn
**Then** the user still receives a response if possible
**And** the failure is logged for diagnosis.

### Story 2.5: Text File Context Ingestion

As a package user,
I want to upload text-based files during brainstorm facilitation,
So that existing notes can influence ideation without manual copy-paste.

**Requirements Covered:** FR10, FR12, FR32, UX-DR12, UX-DR14

**Acceptance Criteria:**

**Given** the session is in Facilitate phase
**When** I select a supported text file from the chat input
**Then** the file appears as a removable pending attachment chip
**And** it is sent with my next message.

**Given** a file attachment is sent
**When** the agent processes the message
**Then** it extracts text content into an active context chunk
**And** acknowledges the file in chat with a concise summary.

**Given** the session is not in Facilitate phase
**When** the chat input renders
**Then** file upload controls are disabled
**And** the disabled state is visually and programmatically clear.

### Story 2.6: URL Context Ingestion

As a package user,
I want to share URLs during brainstorm facilitation,
So that external references can influence ideation while preserving session flow.

**Requirements Covered:** FR11, FR13, FR33, UX-DR13, UX-DR14

**Acceptance Criteria:**

**Given** the session is in Facilitate phase
**When** I add a valid URL through the chat input URL action
**Then** the URL appears as a removable pending attachment chip
**And** it is sent with my next message.

**Given** a URL attachment is sent
**When** the agent processes the message
**Then** it fetches and extracts readable text content into an active context chunk
**And** acknowledges the URL in chat with a concise summary.

**Given** URL fetching or extraction fails
**When** the agent handles the attachment
**Then** it reports the issue in chat without ending the brainstorm session
**And** existing ideas and technique state are preserved.

## Epic 3: Structured Brainstorm Conclusion and Knowledge Capture

Users can conclude a brainstorm, review and adjust themed ideas, then generate validated structured knowledge and BMAD-compatible markdown.

### Story 3.1: Theme Grouping Review and Confirmation

As a package user,
I want the agent to group my brainstorm ideas into reviewable themes before finalization,
So that I can shape the final structure before it is persisted.

**Requirements Covered:** FR4, FR17, FR18, UX-DR16, UX-DR17

**Acceptance Criteria:**

**Given** the session is in Facilitate phase with one or more ideas
**When** I indicate that brainstorming is done
**Then** the session enters the Extract phase
**And** the agent presents ideas grouped into theme cards.

**Given** theme cards are shown
**When** I expand or collapse a theme
**Then** the idea list toggles visibility
**And** the control exposes the correct `aria-expanded` state.

**Given** I request a theme adjustment
**When** the agent handles the adjustment
**Then** it updates theme names or idea membership and presents the revised grouping
**And** no knowledge graph write occurs until I confirm the grouping.

### Story 3.2: Knowledge Graph Domain API and Atomic Writes

As a package user,
I want confirmed brainstorm results stored as structured knowledge,
So that future agents and views can retrieve specific ideas and themes.

**Requirements Covered:** FR21, FR24, FR26, FR27

**Acceptance Criteria:**

**Given** I confirm the final theme grouping
**When** extraction writes brainstorm data
**Then** the backend creates Session, Theme, Idea, and ContextChunk graph nodes as needed
**And** relationships use HAS_THEME, CONTAINS_IDEA, and USES_CONTEXT edge types.

**Given** graph data is written for a project
**When** the KG service resolves the graph namespace
**Then** it uses the `project_{normalized_project_id}` graph naming pattern
**And** enforces organization and project scoping through the backend service layer.

**Given** the agent needs KG operations
**When** it persists brainstorm output
**Then** it calls the FastAPI internal KG endpoints over HTTP with `X-Agent-Key`
**And** it never imports or directly calls backend service classes.

### Story 3.3: Extraction Validation and Node Versioning

As a package user,
I want extracted brainstorm data validated and versioned,
So that final output is structurally complete and future changes have an audit trail.

**Requirements Covered:** FR20, FR25

**Acceptance Criteria:**

**Given** extraction produces themes and ideas
**When** validation runs
**Then** it detects missing summaries, orphan ideas, empty themes, and missing required fields
**And** it auto-corrects issues that match the architecture validation pattern.

**Given** extraction has no meaningful ideas after correction
**When** validation fails fundamentally
**Then** the workflow routes back to Facilitate with an explanation
**And** the retry loop is limited according to the architecture pattern.

**Given** an existing graph node must be changed
**When** the KG service updates it
**Then** it creates a new version linked by VERSION_OF
**And** stores agent id, change description, and created timestamp metadata.

### Story 3.4: Async Embeddings for Brainstorm Ideas

As a package user,
I want brainstorm ideas embedded after they are saved,
So that semantic retrieval can work later without slowing down finalization.

**Requirements Covered:** FR23, NFR3

**Acceptance Criteria:**

**Given** an idea node is written to the knowledge graph
**When** the write succeeds
**Then** the API response returns without waiting for embedding computation
**And** a background task computes the embedding asynchronously.

**Given** an embedding is computed
**When** it is stored
**Then** it uses a `vector(1536)` pgvector column in a relational table linked to the graph node id
**And** the embedding index uses HNSW cosine search configuration.

**Given** embedding computation fails
**When** the background task handles the failure
**Then** the graph node remains available for graph traversal
**And** the failure is logged without rolling back the node write.

### Story 3.5: BMAD Markdown Rendering and Final Session Summary

As a package user,
I want a BMAD-compatible markdown artifact from my finalized brainstorm,
So that the session produces a usable output document without manual formatting.

**Requirements Covered:** FR19, FR22

**Acceptance Criteria:**

**Given** validated brainstorm data exists
**When** the markdown phase runs
**Then** Python renders BMAD-compatible markdown from structured Session, Theme, Idea, and ContextChunk data
**And** the LLM does not freeform-generate the markdown document.

**Given** the session summary and key insights are generated
**When** markdown rendering completes
**Then** the artifact includes session overview, techniques used, themes, ideas, and key insights
**And** the session phase becomes Concluded.

**Given** markdown rendering fails
**When** the agent handles the failure
**Then** the structured KG data remains saved
**And** the user receives a clear error response that can be retried.

## Epic 4: Brainstorm Results Review and Retrieval

Users can revisit brainstorm outcomes through dashboards and detail views, browse themes and ideas, and retrieve stored brainstorm knowledge.

### Story 4.1: Retrieve Brainstorm Session Results

As a package user,
I want completed brainstorm sessions to load their themes, ideas, metadata, and summary,
So that I can review previous ideation work after the session ends.

**Requirements Covered:** FR28, FR30

**Acceptance Criteria:**

**Given** a brainstorm session has concluded
**When** the frontend requests session results
**Then** the backend returns session metadata, summary, themes, and ideas grouped by theme
**And** the response follows the existing API JSON conventions.

**Given** a user requests results for a package outside their organization or project scope
**When** the backend authorizes the request
**Then** it returns the existing forbidden or not found response
**And** no graph data is exposed.

**Given** a concluded session has context chunks
**When** results are loaded
**Then** the response can include source metadata needed by the UI
**And** raw unsupported file content is not exposed unnecessarily.

### Story 4.2: Vector Similarity Search for Ideas

As a future agent or authorized client,
I want to retrieve brainstorm ideas by vector similarity,
So that relevant ideas can be reused without scanning whole documents.

**Requirements Covered:** FR29

**Acceptance Criteria:**

**Given** idea embeddings exist for a project
**When** an authorized vector search request is made with an embedding and limit
**Then** the KG API returns the closest matching ideas for that project
**And** results do not cross project graph boundaries.

**Given** some ideas do not yet have embeddings
**When** vector search runs
**Then** it skips non-embedded ideas without failing the whole request
**And** graph traversal retrieval remains available separately.

**Given** a caller requests an invalid limit or malformed embedding
**When** the endpoint validates input
**Then** it returns the existing validation error format
**And** no query is executed.

### Story 4.3: Brainstorm Summary Card on Project Dashboard

As a project user,
I want concluded brainstorms summarized on the project dashboard,
So that I can discover and reopen useful ideation results quickly.

**Requirements Covered:** FR34, UX-DR18, UX-DR25

**Acceptance Criteria:**

**Given** a package has a concluded brainstorm session
**When** I view the project dashboard
**Then** a BrainstormSummaryCard appears under or near the package row
**And** it shows session date, technique count, idea count, theme count, and theme pills.

**Given** more themes exist than fit in the summary card
**When** the card renders theme pills
**Then** it shows the configured maximum number of theme pills
**And** displays a `+N more` indicator for hidden themes.

**Given** I click View Details on the summary card
**When** navigation completes
**Then** I arrive at the brainstorm detail view for that package session
**And** focus moves to the main content heading.

### Story 4.4: Brainstorm Detail Theme and Idea Browsing

As a package user,
I want a detailed brainstorm results page with themes and ideas,
So that I can inspect final outputs without reopening the active chat flow.

**Requirements Covered:** FR35, FR36, UX-DR15, UX-DR16, UX-DR19, UX-DR20, UX-DR22

**Acceptance Criteria:**

**Given** I open a brainstorm detail page
**When** results load successfully
**Then** I see the session summary, key insights, theme cards, and idea cards
**And** the page uses Thagid design system tokens and shadcn-svelte primitives.

**Given** a theme card is collapsed
**When** I activate the theme header
**Then** the theme expands to show its ideas
**And** each idea card shows title, concept description, category, and novelty.

**Given** I want to return to the package conversation
**When** I use the Back to Package action
**Then** I navigate back to the package chat route
**And** the org, project, and package scope remains consistent in breadcrumbs and sidebar.
