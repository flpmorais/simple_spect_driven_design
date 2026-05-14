---
stepsCompleted:
  - step-01-init
  - step-02-discovery
  - step-02b-vision
  - step-02c-executive-summary
  - step-03-success
  - step-04-journeys
  - step-05-domain-skipped
  - step-06-innovation-skipped
  - step-07-project-type
  - step-08-scoping
  - step-09-functional
  - step-10-nonfunctional
  - step-11-polish
  - step-12-complete
inputDocuments:
  - _bmad-output/brainstorming/brainstorming-session-2026-05-06-0952.md
  - _bmad-output/brainstorming/brainstorming-session-2026-05-07-0930.md
  - _bmad-output-old/0_scaffolding/project-context.md
  - docs/getting-started.md
  - docs/development.md
  - docs/configuration.md
  - docs/business-rules.md
  - docs/architecture.md
  - docs/api.md
documentCounts:
  briefs: 0
  research: 0
  brainstorming: 2
  projectDocs: 6
  projectContext: 1
classification:
  projectType: developer_tool
  domain: general
  complexity: medium
  projectContext: brownfield
  prdScope: data_pipeline_and_brainstorm_agent
workflowType: 'prd'
---

# Product Requirements Document - Thagid

**Author:** Fmorais
**Date:** 2026-05-07

## Executive Summary

Thagid replaces monolithic document-per-skill patterns with atomic graph nodes stored in PostgreSQL + AGE + pgvector. The system retrieves only what an agent needs per turn — achieving token efficiency through selective retrieval, not compression.

This PRD covers the barebones data pipeline (knowledge graph storage, embedding pipeline, retrieval API, BMAD markdown renderer) and the brainstorming agent — the first LangGraph skill that validates the architecture end-to-end. The existing Thagid webhook backend and PostgreSQL container form the brownfield foundation.

### What Makes This Special

**Agents don't need documents, they need specific data points.** Dissolving monolithic documents into atomic graph nodes enables role-based retrieval — creator agents use vector search, executor agents use graph traversal. The brainstorm agent proves this with real-time idea management via LangGraph state reducers, where LLMs produce structured data and Python produces markdown.

## Project Classification

- **Project Type:** Developer tool — AI-powered SDLC automation
- **Domain:** General (no regulatory constraints)
- **Complexity:** Medium — novel architecture (knowledge graph + RAG + LangGraph), bounded scope
- **Project Context:** Brownfield — existing webhook backend, PostgreSQL container, GitHub Projects integration

## Success Criteria

### User Success

- User creates a package, runs a brainstorm session, and ends with structured ideas stored as atomic graph nodes
- Technique selection happens in the opening message, not as a separate step
- User can upload files, share URLs, and swap techniques mid-session without breaking flow
- Session persists via checkpointing — user can leave and return
- Final output is a BMAD-compatible markdown document rendered from structured data

### Project Success

- Brainstorm agent validates that atomic-node storage + selective retrieval is viable
- No monolithic document reads — agent loads only its prompt, active technique, and current state
- Data pipeline is minimal but extensible — future skills reuse the same KG API without rework

### Technical Success

- KG API exposes domain-specific methods — agents never write Cypher/SQL directly
- LLM produces structured data (Pydantic), Python produces markdown — deterministic, not freeform
- Node versioning provides audit trail for every change

### Measurable Outcomes

- End-to-end brainstorm session completes: initiate → facilitate → theme grouping → conclude → KG write → markdown render
- Ideas stored as individual nodes with embeddings, grouped by themes
- BMAD markdown output is valid and readable without manual intervention
- Graph schema supports Session, Theme, Idea, ContextChunk node types and edge types

## Product Scope

### MVP - Minimum Viable Product

- PostgreSQL + AGE + pgvector in single container
- pgAdmin and Apache AGE Viewer in podman-compose for dev (monitoring and graph visualization)
- KG API with brainstorm-specific methods (~10 methods)
- Async embedding pipeline for ideas (on-write)
- BMAD markdown renderer (Python script)
- Brainstorm agent: INITIATE → FACILITATE (with 4 tools) → EXTRACT → VALIDATE → MARKDOWN
- Theme grouping before conclusion (facilitator presents, user confirms)
- Technique reference table seeded with 61 techniques
- One brainstorm session per package
- Frontend: technique picker modal, summary card, detail tab

### Deferred

- Embedding pipeline failure handling strategy
- Visual file ingestion (images, PDFs, PPT via vision LLM)

### Growth Features (Post-MVP)

- Multiple brainstorm sessions per package
- Additional skills (PRD, architecture, UX) using the same pipeline

### Vision (Future)

- Full skill ecosystem with creator/executor agent roles
- Graph traversal for executor agents
- Context-aware re-embedding with similarity threshold checks
- Neo4j migration path (if scale demands it)

## User Journeys

### Journey 1: First Brainstorm Session

Fmorais creates a new package for the Thagid data pipeline. He opens the package chat and the brainstorm agent activates. The initiator reads the package description and recommends techniques. Fmorais accepts and the facilitator begins.

Over the next 20 minutes, Fmorais and the facilitator exchange ideas. He uploads a markdown file with existing notes. The facilitator ingests it and weaves the content into ideation. He swaps techniques mid-flow. Ideas accumulate in real-time via the state reducer.

When Fmorais says "done," the facilitator presents all ideas grouped into themes. Fmorais reviews and adjusts the groupings. Once confirmed, the extractor writes a Session node, Theme nodes, Idea nodes, and ContextChunk nodes to the knowledge graph. Each idea gets embedded asynchronously. A Python script renders BMAD-compatible markdown. Fmorais sees the brainstorm summary on the dashboard.

### Journey 2: Session Abandoned and Resumed

Fmorais starts a brainstorm session but gets pulled into a meeting. He closes the browser tab. Two days later he reopens the package and continues chatting with the facilitator exactly as if he never left. Chat history, ideas, and active technique are preserved.

### Journey 3: Embedding Pipeline Resilience

During extraction, the embedding service is temporarily down. Nodes write to the graph successfully — ideas exist without embeddings for now. Pending embeddings process asynchronously later. *(Failure handling strategy deferred.)*

### Journey 4: Reviewing Brainstorm Results

A week later, Fmorais opens the package and sees his brainstorm results on the dashboard — ideas grouped by theme, session metadata, key insights. He browses themes and drills into specific ideas.

### Journey Requirements Summary

| Capability Area | Journeys |
|----------------|----------|
| Session lifecycle (create, run, abandon, resume, conclude) | 1, 2 |
| Brainstorm state machine (initiate, facilitate, extract) | 1 |
| Real-time idea management via state reducer | 1 |
| File upload + technique swapping tools | 1 |
| Theme grouping (facilitator presents, user confirms) | 1 |
| KG write (Session, Theme, Idea, ContextChunk nodes) | 1 |
| Async embedding for ideas | 1, 3 |
| BMAD markdown rendering | 1 |
| Session persistence via checkpointing | 2 |
| Dashboard display of themes and ideas | 4 |

## Developer Tool Specific Requirements

### Migration Source: BMAD Brainstorming Skill

The brainstorming agent migrates the existing BMAD brainstorming skill (`.agents/skills/bmad-brainstorming/`) from a token-heavy, file-based workflow to a LangGraph state machine. Source skill characteristics:

- **4-step workflow:** Session setup → Technique selection (4 approaches) → Technique execution → Idea organization
- **61 techniques** in `brain-methods.csv` — loaded on-demand
- **Idea format:** Category, mnemonic title, concept description, novelty
- **Anti-bias protocol:** Domain pivot every 10 ideas to prevent semantic clustering
- **Quantity goal:** 100+ ideas before organization
- **Output:** Markdown file with session overview, technique results, themed ideas, action plans

### Migration Mapping

| BMAD Step | LangGraph Equivalent |
|-----------|---------------------|
| Step 1: Session setup | INITIATE — reads package description, recommends techniques in opening message |
| Step 2: Technique selection | Folded into INITIATE — technique picker is a tool, not a phase |
| Step 3: Technique execution | FACILITATE — agent + tools pattern with real-time idea management |
| Step 4: Idea organization | Conclude — facilitator presents themed ideas, user confirms, EXTRACT writes to KG |

### Architecture Deferrals

- **KG API surface:** ~10 brainstorm-specific methods (exact interface deferred to architecture)
- **Agent interface:** How agents call the KG API (module import vs HTTP vs other) — deferred to architecture
- **Container topology:** Agent should run in a separate container from FastAPI backend — flag for architecture review
- **Brain-methods.csv:** Stored as reference table in database, not in KG

### Implementation Considerations

- Migration collapses 4 steps to 3 states by folding technique selection into the opening message
- Anti-bias protocol and domain pivoting preserved in facilitator system prompt
- 100+ ideas quantity goal replaced by user-driven conclusion (user says "done")
- Theme grouping replaces BMAD's full idea organization step — facilitator presents themes, user confirms
- BMAD markdown produced by Python renderer from structured data, not by the LLM

## Functional Requirements

### Brainstorm Session Management

- FR1: User can start a brainstorm session within a package
- FR2: User can abandon a brainstorm session and resume it later with full state preserved
- FR3: System can detect an existing brainstorm session for a package and offer to continue it
- FR4: User can conclude a brainstorm session by indicating completion
- FR5: System persists session state (messages, ideas, active technique, documents) across sessions

### Brainstorm Ideation

- FR6: System can recommend brainstorming techniques based on the package description
- FR7: User can accept, adjust, or replace recommended techniques
- FR8: User can swap techniques mid-session without losing existing ideas
- FR9: User can browse all available techniques (61) via a technique picker
- FR10: User can upload text-based files during a brainstorm session
- FR11: User can share URLs during a brainstorm session
- FR12: System can ingest uploaded files and incorporate their content into ideation
- FR13: System can fetch and extract text content from shared URLs
- FR14: System maintains a real-time list of ideas during facilitation, resolving duplicates and contradictions as they arise
- FR15: System applies anti-bias domain pivoting during ideation to prevent semantic clustering
- FR16: System maintains a rolling summary of earlier conversation to keep context bounded

### Brainstorm Output

- FR17: System can present all ideas grouped into themes to the user before conclusion
- FR18: User can review and adjust theme groupings before finalizing
- FR19: System can extract a session summary and key insights from the finalized brainstorm state
- FR20: System can validate extracted data for completeness and structural correctness
- FR21: System can write session, theme, idea, and context chunk data as atomic nodes to the knowledge graph
- FR22: System can render BMAD-compatible markdown from the structured brainstorm data
- FR23: System can compute embeddings for ideas asynchronously on write to the knowledge graph

### Knowledge Graph Storage

- FR24: System can store atomic graph nodes with typed relationships (Session, Theme, Idea, ContextChunk)
- FR25: System can version nodes — every update creates a new version with agent and change metadata
- FR26: System supports multi-tenant scoping (organization → project → graph)
- FR27: System exposes a domain-specific API for knowledge graph operations — agents never write Cypher/SQL directly

### Knowledge Graph Retrieval

- FR28: System can retrieve ideas by theme membership
- FR29: System can retrieve ideas by vector similarity search
- FR30: System can retrieve session metadata and summary

### Frontend — Chat Interface

- FR31: User can interact with the brainstorm agent through a text chat within a package
- FR32: User can upload files via the chat interface
- FR33: User can share URLs via the chat interface

### Frontend — Brainstorm Dashboard

- FR34: User can see a brainstorm summary card on the package dashboard showing session date, technique count, and idea count
- FR35: User can drill into a brainstorm detail tab showing ideas grouped by theme, session metadata, and key insights
- FR36: User can browse themes and drill into specific ideas within the detail tab

## Non-Functional Requirements

### Performance

- NFR1: Facilitator token overhead per turn stays within ~3.5-7.7K tokens (system prompt + technique + ideas + summary + messages)
- NFR2: Chat responses return within the LLM provider's standard response time — no additional processing bottleneck
- NFR3: Embedding computation is asynchronous and must not block node writes to the knowledge graph
- NFR4: Rolling summarization triggers every ~20 messages without disrupting the facilitation loop

### Integration

- NFR5: System handles LLM API failures with standard retry logic (specifics deferred to architecture)
- NFR6: Knowledge graph operates within the existing PostgreSQL container infrastructure
- NFR7: Brainstorm agent is compatible with the existing package chat interface (SvelteKit frontend)
