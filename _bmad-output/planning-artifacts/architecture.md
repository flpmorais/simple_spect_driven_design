---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
inputDocuments:
  - _bmad-output/planning-artifacts/prd.md
  - _bmad-output-old/0_scaffolding/planning-artifacts/architecture.md
  - _bmad-output-old/0_scaffolding/project-context.md
  - docs/getting-started.md
  - docs/api.md
  - docs/development.md
  - docs/configuration.md
  - docs/business-rules.md
  - docs/architecture.md
workflowType: 'architecture'
project_name: 'Thagid'
user_name: 'Fmorais'
date: '2026-05-07'
lastStep: 8
status: 'complete'
completedAt: '2026-05-07'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**

36 FRs across 8 domains. The architecture must support:

- **Session Management (FR1-5):** Create, abandon/resume, detect existing, conclude brainstorm sessions within a package. Conversation/workflow state includes messages, ideas, active technique, and documents — owned by LangGraph and persisted across sessions via LangGraph checkpointing.
- **Ideation (FR6-16):** Technique recommendation and selection (62 techniques from reference table), mid-session technique swapping, file upload + URL ingestion for context, real-time idea management with deduplication/contradiction resolution, anti-bias domain pivoting, rolling conversation summary.
- **Output Pipeline (FR17-23):** Theme grouping (facilitator presents, user confirms), extraction to structured data, validation, atomic node writes to KG (Session, Theme, Idea, ContextChunk), BMAD markdown rendering from structured data, async embedding computation.
- **KG Storage (FR24-27):** Atomic graph nodes with typed relationships, node versioning with audit trail, multi-tenant scoping (org → project → graph), domain-specific API (no raw Cypher/SQL).
- **KG Retrieval (FR28-30):** Theme-based idea lookup, vector similarity search, session metadata retrieval.
- **Frontend - Chat (FR31-33):** Text chat with brainstorm agent, file upload, URL sharing — extends existing package chat interface.
- **Frontend - Dashboard (FR34-36):** Brainstorm summary card (session date, technique count, idea count), detail tab with themed ideas, theme/idea browsing.

**Non-Functional Requirements:**

- **NFR1 (Performance):** Facilitator token overhead per turn ~3.5-7.7K tokens — constrains how much state is loaded per agent turn.
- **NFR2 (Performance):** Chat responses within LLM provider's standard response time — no additional processing bottleneck.
- **NFR3 (Performance):** Async embeddings — must not block KG node writes. Background worker pattern required.
- **NFR4 (Performance):** Rolling summarization every ~20 messages — must not disrupt facilitation loop.
- **NFR5 (Integration):** LLM API failure retry logic — resilience pattern required.
- **NFR6 (Integration):** KG operates within existing PostgreSQL container infrastructure — extensions (AGE, pgvector) installed in same container.
- **NFR7 (Integration):** Brainstorm agent compatible with existing SvelteKit chat interface — no new frontend framework.

**Scale & Complexity:**

- Primary domain: Backend-heavy system (knowledge graph + agent runtime/orchestration + embedding pipeline)
- Complexity level: Medium — novel architecture (AGE + pgvector + LangGraph + PydanticAI) but bounded scope (one agent, one pipeline)
- Estimated architectural components: 6-8 new components on top of existing 4-container topology

### Technical Constraints & Dependencies

- **Existing system:** FastAPI backend with JWT auth, PostgreSQL in podman-compose, SvelteKit SPA frontend, nginx reverse proxy, Cloudflare tunnel for dev
- **Existing architecture patterns:** Router → Service → Model, multi-tenant org scoping, URL-driven scope resolution, HTTP-only cookie auth
- **New extensions required:** Apache AGE (graph queries via Cypher on PostgreSQL), pgvector (vector similarity search on PostgreSQL)
- **LangGraph:** Python framework for conversation/thread orchestration, workflow state, approval pauses, resume, retry loops between nodes, long-running workflow state, and checkpoint history
- **PydanticAI:** Python agent runtime for individual agent node execution: LLM call, tool registration, typed outputs, tool argument validation, agent-level retry, and structured result parsing
- **No LangChain application APIs:** Application code must not use LangChain agents, chains, tools, memory, prompts, message classes, or Runnable/RunnableConfig
- **BMAD markdown:** Existing skill (`.agents/skills/bmad-brainstorming/`) provides the output format specification
- **brain-methods.csv:** 62 brainstorming techniques — stored as database reference table, not in KG
- **Agent container:** PRD flags agent should run in separate container from FastAPI backend
- **No new frontend framework** — brainstorm UI extends existing SvelteKit chat and dashboard

### Cross-Cutting Concerns Identified

1. **Multi-tenant data isolation** — KG nodes must be scoped by org → project → graph, consistent with existing `org_id` filtering pattern (FR26)
2. **Auth propagation** — New agent-facing API endpoints need the same JWT auth guard as existing `/api/*` routes
3. **Container topology expansion** — Adding agent container + dev tools (pgAdmin, AGE Viewer) to existing 4-container setup
4. **Error handling across boundaries** — LLM API failures (NFR5), embedding service failures (deferred), KG write failures — need consistent error patterns
5. **Agent-API interface pattern** — How LangGraph-orchestrated PydanticAI agent nodes call the KG API (module import vs HTTP) is the key integration decision
6. **State management** — LangGraph workflow state (messages, ideas, technique) vs frontend state (Svelte stores) vs persistent business/audit records (KG nodes) — clear boundaries needed

## Starter Template Evaluation

### Primary Technology Domain

Brownfield backend extension — adding knowledge graph (AGE + pgvector), agent runtime (PydanticAI), and agent orchestration/checkpointing (LangGraph) to an existing FastAPI + SvelteKit + PostgreSQL system. No new frontend framework needed.

### Starter Options Considered

**Option 1: Extend existing PostgreSQL container with AGE + pgvector extensions**

- Build a custom PostgreSQL image from `postgres:16` adding AGE and pgvector extensions
- Keeps single PostgreSQL container — consistent with NFR6 (KG operates within existing PostgreSQL container infrastructure)
- Requires custom `Containerfile` for postgres

**Option 2: Separate PostgreSQL container for graph data**

- Run a second postgres container with AGE + pgvector for graph workloads
- Cleaner separation of concerns
- Rejected — violates NFR6 and adds operational complexity for MVP

**Option 3: Use an existing AGE + pgvector Docker image (e.g., community images)**

- Community images exist but are not officially maintained by Apache AGE
- Risk: unmaintained, version conflicts between AGE and pgvector
- Rejected for MVP — building from official sources is more reliable

**Agent Runtime Options:**

**Option A: LangGraph-orchestrated PydanticAI agent service runs inside the existing FastAPI process**

- Agent code lives in `thagid/agents/` as a Python module
- Agent calls KG API as direct function calls (module import)
- Simpler deployment — no new container
- Tighter coupling — agent lifecycle tied to FastAPI process

**Option B: LangGraph-orchestrated PydanticAI agent service runs in a separate container (PRD recommendation)**

- Agent code in separate directory/package (e.g., `agent/`)
- Agent calls KG API via HTTP (internal network)
- Independent scaling and deployment
- Matches PRD explicit flag: "Agent should run in a separate container from FastAPI backend"

### Selected Starter: Custom PostgreSQL image + Separate agent container

**Rationale for Selection:**

1. **PostgreSQL:** Build custom image from `postgres:16` with AGE + pgvector extensions compiled/installed. Full control over versions, NFR6 satisfied (single PG container).
2. **Agent:** Follow PRD recommendation — separate container. The agent service is a long-running workflow process (LangGraph orchestration/checkpointing) that executes individual nodes through PydanticAI, with different lifecycle requirements than the request/response API server.
3. **Frontend:** No starter needed — extend existing `web/` SvelteKit project with brainstorm-specific components and routes.

**PostgreSQL Containerfile (postgres/Containerfile):**

```dockerfile
FROM postgres:16
# Install build dependencies, Apache AGE, pgvector
# Exact build steps defined in implementation
```

**Extension initialization:**

```sql
CREATE EXTENSION IF NOT EXISTS age;
CREATE EXTENSION IF NOT EXISTS vector;
LOAD 'age';
SET search_path = ag_catalog, "$user", public;
```

**New Python Dependencies (pyproject.toml):**

```
langgraph>=1.1.10
langgraph-checkpoint-postgres
pydantic-ai
pgvector>=0.4.2
```

**Architectural Decisions Provided by Starter:**

**Database Extensions:**
- Apache AGE for graph queries (Cypher on PostgreSQL)
- pgvector for vector similarity search (HNSW indexing)
- Both extensions in the same postgres container
- Async access via asyncpg (already in stack) with pgvector's asyncpg registration

**Agent Runtime & Orchestration:**
- LangGraph 1.1.x (stable) for conversation thread state, workflow orchestration, approval pauses, resume, node-to-node retry loops, long-running workflow state, and checkpoint history
- PydanticAI for individual agent node execution: LLM calls, tool registration, typed outputs, tool argument validation, agent-level retry, and structured result parsing
- Separate container (`thagid-agent`) in podman-compose
- Internal HTTP communication with FastAPI backend (KG API)
- LangGraph checkpointing for session persistence (replaces custom session storage)
- Application code may use PydanticAI `Agent`, Pydantic models, and LangGraph `StateGraph`/checkpointing/orchestration primitives; it must not use LangChain agents, chains, tools, memory, prompts, message classes, or Runnable/RunnableConfig

**pgvector Integration:**
- SQLAlchemy Vector column type via `pgvector.sqlalchemy.Vector`
- asyncpg driver support via `pgvector.asyncpg.register_vector`
- HNSW indexing for approximate nearest neighbor search

**Note:** PostgreSQL image build and extension setup should be one of the first implementation stories.

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**
- KG data model (graph schema — nodes, edges, scoping)
- KG API interface (~10 methods for brainstorm MVP)
- Agent ↔ Backend communication pattern (HTTP)
- LangGraph orchestration design (5 nodes, edges, state shape, PydanticAI node execution boundaries)
- Session persistence (PostgreSQL checkpointer)

**Important Decisions (Shape Architecture):**
- Embedding pipeline (model, async pattern, storage)
- Frontend integration pattern (agent proxy through FastAPI)
- Validation failure handling (auto-correct with fallback)

**Deferred Decisions (Post-MVP):**
- Multiple brainstorm sessions per package
- Additional skills reusing KG API
- Embedding pipeline failure handling strategy
- Context-aware re-embedding with similarity thresholds

### Data Architecture

**Graph Database:** Apache AGE extension on existing PostgreSQL container. One graph per project, created on project initialization.

**Graph schema (AGE Cypher labels):**

```
Graph namespace: "project_{normalized_project_id}" (one AGE graph per project; UUID hyphens replaced with underscores)

Nodes (labels + properties):
- Session: {id: UUID, package_id: UUID, status: str, technique: str, created_at: timestamp, concluded_at: timestamp}
- Theme: {id: UUID, title: str, summary: str, position: int}
- Idea: {id: UUID, category: str, title: str, concept: str, novelty: str}
- ContextChunk: {id: UUID, source_type: str, source_ref: str, content: str}

Vector columns (pgvector, stored alongside graph nodes in relational tables):
- idea_embeddings: {node_id: UUID, embedding: vector(1536)}
- chunk_embeddings: {node_id: UUID, embedding: vector(1536)}

Edges (AGE relationship types):
- HAS_THEME: Session → Theme
- CONTAINS_IDEA: Theme → Idea
- USES_CONTEXT: Session → ContextChunk
- VERSION_OF: Node → Node (versioning chain — new version per update)

Versioning (FR25):
- Every update creates a new node linked via VERSION_OF to the previous version
- Each version records: agent_id, change_description, created_at
- Original node preserved, new node is the current version
```

**Multi-tenant scoping (FR26):** Each project gets its own AGE graph. The graph name encodes the project_id. The KG API resolves project_id → graph name, ensuring data isolation at the graph level.

**Embedding storage:** pgvector `vector(1536)` columns in relational tables mapped to graph nodes. HNSW index with `vector_cosine_ops` for approximate nearest neighbor search. Embeddings stored separately from graph properties to keep AGE queries clean.

### Knowledge Graph API

**Location:** `thagid/services/knowledge_graph.py` — follows existing Router → Service → Model pattern.

**KG API surface (brainstorm MVP — ~10 methods):**

```python
class KnowledgeGraphService:
    async def create_graph(self, project_id: str) -> None
    async def delete_graph(self, project_id: str) -> None
    async def write_session(self, project_id: str, session_data: SessionCreate) -> str
    async def write_themes(self, project_id: str, session_id: str, themes: list[ThemeCreate]) -> list[str]
    async def write_ideas(self, project_id: str, theme_id: str, ideas: list[IdeaCreate]) -> list[str]
    async def write_context_chunks(self, project_id: str, session_id: str, chunks: list[ChunkCreate]) -> list[str]
    async def get_session(self, project_id: str, session_id: str) -> SessionData
    async def get_themes_with_ideas(self, project_id: str, session_id: str) -> list[ThemeWithIdeas]
    async def search_ideas_by_vector(self, project_id: str, embedding: list[float], limit: int = 10) -> list[IdeaData]
    async def update_node(self, project_id: str, node_id: str, properties: dict) -> str
```

**update_node (FR25):** Creates a new version of an existing node. Returns the new node_id. The previous version is preserved and linked via VERSION_OF edge. Enables future skills to modify brainstorm data while maintaining audit trail.

**Internal implementation:** Service executes Cypher queries via AGE's SQL integration. Asyncpg driver handles the async PostgreSQL calls. pgvector operations use asyncpg with `register_vector`.

### Agent ↔ Backend Communication

**Pattern:** HTTP over internal podman network.

**Decision:** The brainstorm agent runs in a separate container (`thagid-agent`) and calls the FastAPI backend's KG API via internal HTTP endpoints.

**Internal KG API endpoints exposed by FastAPI:**

```
POST   /internal/kg/projects/{project_id}/sessions
POST   /internal/kg/projects/{project_id}/sessions/{session_id}/themes
POST   /internal/kg/projects/{project_id}/themes/{theme_id}/ideas
POST   /internal/kg/projects/{project_id}/sessions/{session_id}/chunks
GET    /internal/kg/projects/{project_id}/sessions/{session_id}
GET    /internal/kg/projects/{project_id}/sessions/{session_id}/themes-with-ideas
POST   /internal/kg/projects/{project_id}/ideas/search
PATCH  /internal/kg/projects/{project_id}/nodes/{node_id}
```

**Rationale:** Separates agent lifecycle from API server while keeping KG writes behind FastAPI. Browser traffic never calls KG write endpoints directly; frontend traffic goes through JWT-authenticated package/brainstorm endpoints. Internal network latency in podman is negligible.

**Authentication for agent:** Internal API key (shared secret between FastAPI and agent container). Agent requests to `/internal/kg/*` include `X-Agent-Key`. These endpoints are separate from user JWT auth — the agent is a system service, not a user.

### Embedding Pipeline

**Model:** OpenAI `text-embedding-3-small` — 1536 dimensions, cost-effective, good quality for idea-level text.

**Async pattern:** FastAPI `BackgroundTasks` — node writes complete immediately, then a background task computes the embedding and updates the node's embedding column.

**Flow:**
1. KG API writes node to graph (no embedding yet)
2. Response returns immediately to caller
3. Background task: call OpenAI embedding API → update embedding column
4. If embedding fails: node exists without embedding (deferred to future failure handling)

**Vector storage:** `vector(1536)` columns with HNSW index (`vector_cosine_ops`) for cosine similarity search.

### LangGraph Orchestration + PydanticAI Agent Nodes

**Ownership rule:** LangGraph owns conversation/workflow state. PydanticAI owns individual agent execution. The database owns business records and audit records.

**Call path:**

```
FastAPI chat API
  ↓
LangGraph thread/session
  ↓
LangGraph orchestration + checkpointing
  ↓
PydanticAI agent nodes
  ↓
tools / MCP / git / shell / project APIs
```

**Use LangGraph for:** conversation thread state, approval pauses, resume after user input, retry loops between nodes, long-running workflow state, and checkpoint history.

**Use PydanticAI for:** LLM call, tool registration, typed outputs, tool argument validation, agent-level retry, and structured result parsing.

**State definition:**

```python
class BrainstormState(TypedDict):
    package_id: str
    technique: str | None
    messages: Annotated[list[dict[str, str]], append_messages_reducer]
    ideas: Annotated[list[Idea], add_ideas_reducer]
    themes: list[Theme]
    active_documents: list[ContextChunk]
    summary: str | None
    session_id: str | None
```

**Orchestration topology:**

```
START → initiate → facilitate → extract → validate → markdown → END
                      ↑             ↑                        |
                      |_____________|    (validation failure) |
                                          auto-correct →     |
                                          fatal → facilitate__|
```

**Nodes:**

- **initiate:** Reads package description from KG, recommends techniques in opening message, sets technique on state
- **facilitate:** Main ideation loop. LangGraph owns the thread state and calls a PydanticAI agent with 4 tools: `swap_technique`, `upload_file`, `share_url`, `conclude_session`. Ideas accumulate via `add_ideas` reducer. Rolling summary triggers every ~20 messages.
- **extract:** Groups ideas into themes, prepares structured data. Calls KG API to write Session, Theme, Idea, ContextChunk nodes.
- **validate:** Checks structural completeness. Auto-corrects fixable issues (orphan ideas → "General" theme, missing summaries → generate). If fundamental data missing (no ideas), routes back to `facilitate` with explanation.
- **markdown:** Renders BMAD-compatible markdown from structured data via Python renderer. Returns final output.

**Tools (facilitate node):**

- `swap_technique(new_technique)` — loads technique from reference table, preserves existing ideas
- `upload_file(file)` — reads file content, creates ContextChunk, adds to active_documents
- `share_url(url)` — fetches URL content, creates ContextChunk, adds to active_documents
- `conclude_session()` — signals transition from facilitate → extract

### Session Persistence (Checkpointing)

**Checkpointer:** `langgraph-checkpoint-postgres` — stores LangGraph state in PostgreSQL.

**Storage:** Same postgres container, separate schema (`agent_checkpoints`). Agent container connects to the same PG instance.

**Boundary:** Checkpoints store workflow/conversation state only. Final brainstorm sessions, themes, ideas, context chunks, node versions, and audit history are business records owned by the KG/database layer.

**Session lifecycle:**
- First message → creates checkpoint
- Every turn → updates checkpoint (messages, ideas, technique, summary)
- User abandons → checkpoint persists (FR2/FR5)
- User returns → loads checkpoint, resumes from last state
- Session concludes → final state preserved as completed

### Frontend Integration

**Pattern:** FastAPI acts as gateway/proxy to the agent.

**New endpoint:**

```
POST /api/packages/{package_id}/brainstorm/message
```

**Flow:**
1. Frontend sends message to FastAPI (same pattern as existing chat)
2. FastAPI authenticates user, verifies package ownership
3. FastAPI checks if active brainstorm session exists for package
4. FastAPI forwards message to agent container (`thagid-agent`) via HTTP
5. Agent service resumes the LangGraph thread, routes through LangGraph orchestration, executes PydanticAI agent nodes as needed, and returns response
6. FastAPI saves message pair to existing Message model
7. Response returns to frontend

**Existing chat preserved:** `POST /api/packages/{package_id}/messages` continues to work for non-brainstorm chat. The brainstorm endpoint is separate — the frontend decides which to call based on package state (has active brainstorm session → use brainstorm endpoint).

**Brainstorm session detection (FR3):** When a package is opened, frontend calls `GET /api/packages/{package_id}/brainstorm/status`. If active session exists, UI shows brainstorm mode (technique picker, idea count, etc.).

### Decision Impact Analysis

**Implementation Sequence:**

1. Build custom PostgreSQL image with AGE + pgvector
2. Add KG service layer (`thagid/services/knowledge_graph.py`) + KG router
3. Add embedding pipeline (OpenAI integration, background tasks)
4. Build agent container with LangGraph orchestration and PydanticAI brainstorm agent nodes
5. Add brainstorm proxy endpoint in FastAPI
6. Add frontend brainstorm UI extensions (technique picker, summary card, detail tab)
7. Add pgAdmin + AGE Viewer to compose for dev monitoring

**Cross-Component Dependencies:**

- KG service depends on PostgreSQL image with AGE + pgvector (step 1 before 2)
- Agent depends on KG API endpoints existing (steps 1-2 before 4)
- Frontend depends on brainstorm proxy endpoint (step 5 before 6)
- Embedding pipeline depends on KG service (step 2 before 3)
- Agent checkpointing depends on PostgreSQL connection (step 1 before 4)

## Implementation Patterns & Consistency Rules

### Pattern Categories Defined

**Critical Conflict Points Identified:** 6 areas where AI agents could make different choices specific to the new data pipeline components.

All existing scaffold architecture patterns (naming, structure, formats, communication, process) remain in effect. The patterns below are **additive** — they cover new components only.

### Naming Patterns

**Graph Naming (AGE):**

- Graph names: `project_{normalized_uuid}` — lowercase, prefixed, UUID hyphens replaced with underscores (e.g., `project_550e8400_e29b_41d4_a716_446655440000`). Use one helper in `KnowledgeGraphService` to normalize and validate graph names; never build graph names ad hoc.
- Node labels: PascalCase — `Session`, `Theme`, `Idea`, `ContextChunk`
- Edge/relationship types: UPPER_SNAKE_CASE — `HAS_THEME`, `CONTAINS_IDEA`, `USES_CONTEXT`, `VERSION_OF`
- Node properties: snake_case — same as database column conventions (e.g., `package_id`, `created_at`)
- Cypher variable names in queries: snake_case — `s` for session, `t` for theme, `i` for idea, `c` for context_chunk

**Agent Container Naming:**

- Container name: `thagid-agent`
- Package directory: `agent/` at project root
- Module naming: `agent.brainstorm`, `agent.tools`, `agent.state`

**New API Route Naming:**

- Internal KG endpoints: `/internal/kg/projects/{project_id}/...` — internal service namespace for agent-called KG operations
- Brainstorm endpoints: `/api/packages/{package_id}/brainstorm/...` — brainstorm namespace under existing package routes
- Agent internal endpoints: `/internal/agent/...` — separate from user-facing API

### Structure Patterns

**Agent Package Organization:**

```
agent/
├── __init__.py
├── main.py                  # FastAPI app (agent HTTP server)
├── brainstorm/
│   ├── __init__.py
│   ├── graph.py             # LangGraph orchestration graph definition
│   ├── state.py             # BrainstormState TypedDict + reducers
│   ├── nodes/
│   │   ├── __init__.py
│   │   ├── initiate.py
│   │   ├── facilitate.py
│   │   ├── extract.py
│   │   ├── validate.py
│   │   └── markdown.py
│   └── tools/
│       ├── __init__.py
│       ├── swap_technique.py
│       ├── upload_file.py
│       ├── share_url.py
│       └── conclude_session.py
├── config.py                # Agent settings (API keys, backend URL)
├── Containerfile            # Agent container image
└── tests/
    ├── __init__.py
    └── test_brainstorm.py
```

**New Backend Files:**

```
thagid/
├── services/
│   └── knowledge_graph.py   # KG service (~10 methods)
├── routers/
│   ├── kg.py                # KG API endpoints
│   └── brainstorm.py        # Brainstorm proxy endpoints
├── schemas/
│   ├── kg.py                # KG request/response schemas
│   └── brainstorm.py        # Brainstorm request/response schemas
└── models/
    └── embeddings.py        # pgvector embedding tables
```

**One LangGraph node function per file** in `agent/brainstorm/nodes/` — mirrors the one-router-per-resource pattern in the existing backend. Node functions may call PydanticAI `Agent` instances for individual LLM/tool execution, but they must return serializable LangGraph state deltas.

### Format Patterns

**AGE Cypher Query Pattern:**

All Cypher queries use parameterized form via AGE's `cypher()` SQL function. Never string-concatenate values into Cypher. Cypher parameters are passed through AGE's third `agtype` argument; SQLAlchemy bind params only bind the graph name and JSON parameter payload.

```python
# Good — parameterized
await db.execute(
    text("""
        SELECT *
        FROM cypher(
            :graph,
            $$ CREATE (s:Session {id: $id, status: $status}) RETURN s $$,
            :params::agtype
        ) AS (s agtype)
    """),
    {
        "graph": graph_name,
        "params": json.dumps({"id": str(uuid4()), "status": "active"}),
    },
)

# Anti-pattern — string interpolation
await db.execute(
    text(f"SELECT * FROM cypher('project_123', $$ CREATE (s:Session {{id: '{uuid4()}'}}) RETURN s $$) AS (s agtype)")
)
```

**Agent ↔ Backend HTTP Contract:**

Request (agent receives from FastAPI):
```json
{
    "message": "user message text",
    "package_id": "uuid",
    "project_id": "uuid",
    "session_id": "uuid or null",
    "context": {
        "technique": "string or null",
        "idea_count": 0,
        "message_count": 0
    }
}
```

Response (agent returns to FastAPI):
```json
{
    "reply": "agent response text",
    "session_id": "uuid",
    "state_change": "facilitate|extract|validate|markdown|complete",
    "ideas": [{"category": "", "title": "", "concept": "", "novelty": ""}],
    "themes": [{"title": "", "summary": ""}],
    "markdown": "string or null"
}
```

**Embedding Column Convention:**

- Column name: `embedding` — always lowercase
- Type: `vector(1536)` — 1536 dimensions (OpenAI text-embedding-3-small)
- Index: HNSW with `vector_cosine_ops`, named `{table}_embedding_hnsw`
- Null: embedding can be NULL (async write, not yet computed)

### Communication Patterns

**Agent-FastAPI Communication:**

- Agent authenticates via `X-Agent-Key` header (shared secret)
- All requests are synchronous HTTP (agent processes and returns immediately)
- FastAPI handles timeout (configurable, default 120s for LLM calls)
- Errors: agent returns `{"error": "message"}` with appropriate HTTP status

**LangGraph State Reducer Pattern:**

Ideas use a custom reducer that deduplicates by title similarity:

```python
def add_ideas_reducer(existing: list[Idea], new: list[Idea]) -> list[Idea]:
    # Deduplicate: if new idea title is similar to existing, merge
    # Otherwise append
    ...
```

All other state fields use LangGraph state reducers (for messages list, implemented as a project-owned reducer over serializable dicts) or direct replacement (for scalar fields like technique, summary). Application code must keep message state as project-owned serializable data and must not use LangChain message classes.

### Process Patterns

**Error Handling — Agent Boundary:**

- Agent internal errors: logged by agent, returned as `{"error": "..."}` to FastAPI
- FastAPI maps agent errors to user-facing messages: `{"detail": "Brainstorm agent encountered an error. Please try again."}`
- LLM API failures: agent retries with exponential backoff (max 3 attempts)
- KG write failures during EXTRACT: agent returns error to FastAPI, FastAPI returns 500 to user

**Validation Failure Pattern:**

- VALIDATE auto-corrects structural issues:
  - Orphan ideas (no theme) → assigned to "General" theme
  - Empty themes (no ideas) → removed from output
  - Missing session summary → generated from themes
- If fundamental data missing (zero ideas, zero themes after correction) → route back to FACILITATE with message: "I wasn't able to extract meaningful ideas. Let's continue brainstorming."
- Max retry loop: EXTRACT → VALIDATE → FACILITATE cycle limited to 2 retries, then save what exists

**Embedding Failure Pattern:**

- Embedding computation is fire-and-forget in BackgroundTasks
- If embedding API fails: node exists without embedding (searchable by graph traversal, not by vector)
- No retry in MVP — deferred to future failure handling strategy
- Log the failure for monitoring

### Enforcement Guidelines

**All AI Agents MUST:**

- Use parameterized Cypher queries — never string-concatenate into AGE queries
- Follow the graph naming convention: `project_{normalized_uuid}` for graph names, PascalCase for labels, UPPER_SNAKE_CASE for edges
- Follow the agent-backend HTTP contract shapes exactly — no ad-hoc request/response formats
- Place one LangGraph node function per file under `agent/brainstorm/nodes/`
- Use LangGraph for conversation/workflow state, approval pauses, resume, retry loops between nodes, long-running workflow state, and checkpoint history
- Use PydanticAI `Agent` plus Pydantic models for individual agent execution, tool registration, typed outputs, tool argument validation, agent-level retry, and structured result parsing
- Do not use LangChain agents, chains, tools, memory, prompts, message classes, or Runnable/RunnableConfig in application code
- Place embedding columns in dedicated tables, not mixed with graph node properties
- Use the `X-Agent-Key` header for all agent → FastAPI calls
- Follow the validation failure pattern (auto-correct → escalate → max retry)
- Agent-called KG endpoints go under `/internal/kg/` and require `X-Agent-Key`; user-facing KG endpoints must be defined separately under `/api/kg/` with JWT auth if needed later
- All brainstorm endpoints go under `/api/packages/{id}/brainstorm/`

**Pattern Verification:**

- Cypher queries: no string interpolation — check for f-strings or format() in AGE calls
- HTTP contract: Pydantic schemas for agent request/response — validated automatically
- Naming: graph names follow `project_{normalized_uuid}` pattern — enforced in KG service
- Structure: one LangGraph node per file — enforced by directory layout; each node calls PydanticAI only for individual agent execution
- LangChain ban: no imports from LangChain APIs/classes in application code

### Pattern Examples

**Good — KG service method:**

```python
async def write_session(self, db: AsyncSession, project_id: str, data: SessionCreate) -> str:
    graph_name = self.graph_name(project_id)
    session_id = str(uuid4())
    await db.execute(
        text("""
            SELECT *
            FROM cypher(
                :graph,
                $$ CREATE (s:Session {id: $id, package_id: $pkg, status: 'active'}) RETURN s $$,
                :params::agtype
            ) AS (s agtype)
        """),
        {
            "graph": graph_name,
            "params": json.dumps({"id": session_id, "pkg": str(data.package_id)}),
        },
    )
    return session_id
```

**Good — LangGraph node using PydanticAI for agent execution:**

```python
from pydantic import BaseModel
from pydantic_ai import Agent


class TechniqueRecommendation(BaseModel):
    reply: str
    technique: str


technique_agent = Agent("openai:gpt-4.1-mini", output_type=TechniqueRecommendation)


async def initiate(state: BrainstormState) -> dict:
    package = await fetch_package_description(state["package_id"])
    result = await technique_agent.run(
        f"Recommend a brainstorm technique for this package description:\n{package['description']}"
    )
    return {
        "messages": [{"role": "assistant", "content": result.output.reply}],
        "technique": result.output.technique,
    }
```

**Anti-Pattern — LangChain application APIs:**

```python
from langchain.agents import initialize_agent
from langchain_core.messages import AIMessage
from langchain_core.runnables import RunnableConfig
```

**Anti-Pattern — Raw Cypher with string interpolation:**

```python
await db.execute(text(f"SELECT * FROM cypher('{graph}', $$ CREATE (s:Session {{id: '{id}'}}) $$) AS (s agtype)"))
```

**Anti-Pattern — Agent calling KG service directly (bypassing HTTP):**

```python
from thagid.services.knowledge_graph import KnowledgeGraphService
kg = KnowledgeGraphService()
await kg.write_session(db, project_id, data)  # Breaks container boundary
```

## Project Structure & Boundaries

### Complete Project Directory Structure (Delta from Scaffold)

New and modified files only. All existing scaffold files remain unchanged.

```
Thagid/
├── compose.yml                       # UPDATED: adds thagid-agent, pgadmin, age-viewer
├── .env.template                     # UPDATED: adds AGENT_KEY, OPENAI_API_KEY
│
├── postgres/                         # NEW: custom PostgreSQL image
│   └── Containerfile                 # postgres:16 + AGE + pgvector
│
├── agent/                            # NEW: brainstorm agent package
│   ├── __init__.py
│   ├── main.py                       # FastAPI app (agent HTTP server)
│   ├── brainstorm/
│   │   ├── __init__.py
│   │   ├── graph.py                  # LangGraph orchestration graph definition
│   │   ├── state.py                  # BrainstormState TypedDict + reducers
│   │   ├── nodes/
│   │   │   ├── __init__.py
│   │   │   ├── initiate.py
│   │   │   ├── facilitate.py
│   │   │   ├── extract.py
│   │   │   ├── validate.py
│   │   │   └── markdown.py
│   │   └── tools/
│   │       ├── __init__.py
│   │       ├── swap_technique.py
│   │       ├── upload_file.py
│   │       ├── share_url.py
│   │       └── conclude_session.py
│   ├── config.py
│   ├── Containerfile
│   └── tests/
│       ├── __init__.py
│       └── test_brainstorm.py
│
├── migrations/                       # UPDATED: new migration for embedding tables + technique reference
│   └── versions/
│       └── 002_kg_embeddings_and_techniques.py
│
├── thagid/                           # UPDATED: new files in existing package
│   ├── models/
│   │   └── embeddings.py             # NEW: pgvector embedding tables
│   │   └── technique.py              # NEW: brainstorm technique reference table
│   ├── schemas/
│   │   └── kg.py                     # NEW: KG request/response schemas
│   │   └── brainstorm.py             # NEW: brainstorm request/response schemas
│   ├── routers/
│   │   └── kg.py                     # NEW: KG API endpoints
│   │   └── brainstorm.py             # NEW: brainstorm proxy endpoints
│   ├── services/
│   │   └── knowledge_graph.py        # NEW: KG service (~10 methods)
│   │   └── embedding.py              # NEW: embedding computation service
│   └── tests/
│       └── test_kg.py                # NEW: KG service tests
│       └── test_brainstorm.py        # NEW: brainstorm proxy tests
│
└── web/                              # UPDATED: new frontend files
    └── src/
        ├── routes/
        │   └── project/[id]/
        │       └── package/[pkgId]/
        │           └── +page.svelte  # UPDATED: brainstorm mode detection
        └── lib/
            ├── api/
            │   └── brainstorm.ts     # NEW: brainstorm API client
            ├── types/
            │   └── brainstorm.ts     # NEW: brainstorm TypeScript types
            └── components/custom/
                ├── TechniquePicker.svelte    # NEW: technique picker modal
                ├── BrainstormSummary.svelte  # NEW: summary card for dashboard
                └── BrainstormDetail.svelte   # NEW: detail tab with themes/ideas
```

### Container Topology (Updated)

```
podman-compose
├── thagid        (FastAPI, port 8000 internal)
├── thagid-web    (nginx, port 3000→80, serves SPA + proxies to thagid)
├── thagid-agent  (FastAPI, port 8001 internal, brainstorm agent)
├── postgres      (PostgreSQL 16 + AGE + pgvector, port 5432 internal)
├── pgadmin       (pgAdmin 4, port 5050, dev only)
├── age-viewer    (Apache AGE Viewer, port 3001, dev only)
└── cloudflared   (network_mode: host, routes to localhost:3000)
```

**Network:** All containers on internal network except cloudflared. Agent reaches FastAPI via `http://thagid:8000`. FastAPI reaches agent via `http://thagid-agent:8001`.

### Architectural Boundaries

**API Boundaries:**

- Existing endpoints: `/api/*`, `/auth/*`, `/webhook` — unchanged
- Brainstorm chat: `/api/packages/{package_id}/brainstorm/...` — new, JWT-authenticated, proxies to agent
- Internal KG API: `/internal/kg/projects/{project_id}/...` — new, `X-Agent-Key` authenticated, not exposed through nginx/Vite
- Agent internal: agent only accepts requests from FastAPI (validated by `X-Agent-Key`), never directly from frontend

**Container Boundaries:**

- `thagid` → `postgres`: asyncpg connection (SQL + AGE Cypher + pgvector)
- `thagid` → `thagid-agent`: HTTP (brainstorm request endpoint)
- `thagid-agent` → `thagid`: HTTP (internal KG API)
- `thagid-agent` → `postgres`: asyncpg connection (LangGraph checkpointing only)
- `thagid-agent` → OpenAI API: HTTPS (LLM + embeddings)
- Frontend → `thagid-agent`: **never** — all traffic proxied through FastAPI

**Service Boundaries:**

- `KnowledgeGraphService`: owns all AGE + pgvector operations. Receives AsyncSession, raises domain exceptions.
- `EmbeddingService`: owns embedding computation. Called by KG service as background task.
- `BrainstormRouter`: owns HTTP proxy logic. Authenticates user, forwards to agent, saves messages.
- LangGraph: owns agent conversation/workflow state, approval pauses, resume, checkpointing, and retry loops between nodes.
- PydanticAI agent nodes: own individual LLM calls, tool registration/execution, typed outputs, tool argument validation, agent-level retry, and structured result parsing. Call FastAPI KG API via HTTP when tools need project data.
- Database/KG: owns business records, node versions, and audit records.

### Requirements to Structure Mapping

**Session Management (FR1-5):**

- Backend: `thagid/routers/brainstorm.py`, `thagid/services/knowledge_graph.py` (session detection)
- Agent: `agent/brainstorm/nodes/initiate.py`, `agent/brainstorm/state.py` (LangGraph state + checkpointing, PydanticAI node execution)
- Frontend: `web/src/lib/api/brainstorm.ts` (session status check)

**Ideation (FR6-16):**

- Agent: `agent/brainstorm/nodes/facilitate.py`, `agent/brainstorm/tools/*.py` (PydanticAI tool registration/execution inside LangGraph node)
- Backend: `thagid/routers/kg.py` (technique reference table endpoint)
- Frontend: `web/src/lib/components/custom/TechniquePicker.svelte`

**Output Pipeline (FR17-23):**

- Agent: `agent/brainstorm/nodes/extract.py`, `validate.py`, `markdown.py` (LangGraph routing, PydanticAI structured extraction/validation where LLM-backed)
- Backend: `thagid/services/knowledge_graph.py` (node writes), `thagid/services/embedding.py` (async embeddings)
- Frontend: `web/src/lib/components/custom/BrainstormSummary.svelte`, `BrainstormDetail.svelte`

**KG Storage (FR24-27):**

- Backend: `thagid/services/knowledge_graph.py`, `thagid/routers/kg.py`
- Database: `postgres/Containerfile` (AGE + pgvector), `migrations/002_kg_embeddings_and_techniques.py`

**KG Retrieval (FR28-30):**

- Backend: `thagid/services/knowledge_graph.py` (get_themes_with_ideas, search_ideas_by_vector, get_session_summary)

**Frontend Chat (FR31-33):**

- Backend: `thagid/routers/brainstorm.py` (proxy endpoint)
- Frontend: existing chat components + `web/src/lib/api/brainstorm.ts`

**Frontend Dashboard (FR34-36):**

- Backend: `thagid/routers/brainstorm.py` (status + results endpoints)
- Frontend: `BrainstormSummary.svelte`, `BrainstormDetail.svelte`

### Integration Points

**Internal Communication:**

- Frontend → Backend: REST over HTTP (existing pattern, new brainstorm endpoints)
- Backend → Agent: HTTP over internal podman network (new)
- Agent → Backend: HTTP over internal podman network (KG API calls)
- Backend → Database: SQLAlchemy async via asyncpg (existing + AGE + pgvector)
- Agent → Database: asyncpg for LangGraph checkpointing only (new)

**External Integrations:**

- OpenAI API: LLM calls via PydanticAI agent nodes (agent → OpenAI) + embedding API (backend → OpenAI)
- Google OAuth: unchanged from scaffold
- GitHub Webhooks: unchanged from scaffold

**Data Flow:**

```
Browser → nginx (prod) / Vite (dev) → FastAPI → PostgreSQL (AGE + pgvector)
                                    ↕
                              FastAPI ← → Agent Container
                                    ↕           ↕
                              PostgreSQL    OpenAI API
```

### Development Workflow Integration

**Development:**

```bash
podman-compose up thagid thagid-agent postgres   # Backend + Agent + DB
cd web && npm run dev                             # Frontend
```

**Dev monitoring:**

```bash
podman-compose up pgadmin age-viewer              # Optional dev tools
```

**Database Migration:**

```bash
alembic revision --autogenerate -m "add embedding tables and technique reference"
alembic upgrade head
```

**Testing:**

```bash
pytest                              # Backend tests (includes KG + brainstorm)
cd agent && pytest                  # Agent tests
cd web && npx vitest                # Frontend unit tests
cd web && npx playwright test       # E2E tests
```

## Architecture Validation Results

### Coherence Validation

**Decision Compatibility:**
All technology choices are compatible. PostgreSQL 16 + AGE + pgvector is a supported combination (Apache AGE compatible with PG16, pgvector installs as independent extension). LangGraph 1.1.x (stable) requires Python >=3.10 — compatible with existing Python 3.12+ stack. PydanticAI runs on the existing Python/Pydantic stack and owns individual agent execution inside LangGraph nodes. Application code avoids the LangChain programming model; LangGraph may still bring internal/transitive dependencies. pgvector 0.4.2 supports asyncpg — already in the stack. FastAPI in agent container uses same framework as backend — consistent. OpenAI embeddings (text-embedding-3-small) standard HTTP API — no compatibility concerns.

**Pattern Consistency:**
Naming is consistent — graph naming (`project_{normalized_uuid}`), node labels (PascalCase), edges (UPPER_SNAKE_CASE) align with existing conventions. KG API follows Router → Service → Model pattern. Agent uses one LangGraph node per file mirroring one-router-per-resource, with PydanticAI handling individual agent execution inside those nodes. HTTP contract between agent and backend uses same JSON snake_case convention. Container boundary respected — agent calls backend via HTTP, never imports modules directly.

**Structure Alignment:**
Agent package at `agent/` mirrors `thagid/` structure. New backend files fit into existing `services/`, `routers/`, `schemas/`, `models/` directories. Frontend additions go into existing `lib/api/`, `lib/types/`, `lib/components/custom/`. Container topology extends cleanly from 4 to 7 containers.

### Requirements Coverage Validation

**Functional Requirements Coverage:**

| FR Category | FRs | Architecture Support |
|---|---|---|
| Session Management | FR1-5 | Brainstorm router (session status), LangGraph checkpointing (conversation/workflow state persistence), KG service (session business record) |
| Ideation | FR6-16 | LangGraph facilitate node (main loop), PydanticAI agent execution with 4 tools (swap_technique, upload_file, share_url, conclude), technique reference table, rolling summary in state |
| Output Pipeline | FR17-23 | Extract node (theme grouping), validate node (auto-correct), KG service (node writes), embedding service (async), markdown node (BMAD renderer) |
| KG Storage | FR24-27 | AGE graph per project, typed edges, update_node for versioning, KG service (domain API) |
| KG Retrieval | FR28-30 | KG service (get_themes_with_ideas, search_ideas_by_vector, get_session_summary) |
| Frontend - Chat | FR31-33 | Brainstorm proxy endpoint, existing chat components, brainstorm API client |
| Frontend - Dashboard | FR34-36 | BrainstormSummary component, BrainstormDetail component, brainstorm status/results endpoints |

All 36 FRs are architecturally supported.

**Non-Functional Requirements Coverage:**

| NFR | Architecture Support |
|---|---|
| NFR1 (Token budget ~3.5-7.7K) | LangGraph state design loads only technique + ideas + summary per turn; PydanticAI node inputs are bounded and typed |
| NFR2 (Response within LLM time) | No processing bottleneck — FastAPI proxies synchronously, agent processes and returns |
| NFR3 (Async embeddings) | BackgroundTasks in FastAPI, node writes complete immediately |
| NFR4 (Rolling summary ~20 msgs) | LangGraph state reducer triggers summarization in facilitate node |
| NFR5 (LLM retry logic) | PydanticAI agent retries with exponential backoff (max 3 attempts); LangGraph handles retry loops between nodes |
| NFR6 (KG in existing PG) | Custom postgres image with AGE + pgvector in same container |
| NFR7 (Compatible with SvelteKit) | Brainstorm extends existing chat via new API endpoint, same frontend framework |

All 7 NFRs are architecturally supported.

### Implementation Readiness Validation

**Decision Completeness:**
All critical decisions documented with versions (LangGraph 1.1.10, pgvector 0.4.2, PostgreSQL 16; PydanticAI version pinned during implementation). KG API surface defined (~10 methods). Agent orchestration fully specified (5 LangGraph nodes, edges, state shape, PydanticAI execution boundaries, tools). HTTP contract between agent and backend defined with request/response schemas. Container topology expanded with network details. Embedding model chosen (text-embedding-3-small, 1536 dims).

**Structure Completeness:**
Complete directory delta from scaffold with all new files defined. Requirements-to-structure mapping shows where each FR lives. Integration points documented with data flow diagram. Development, build, and test workflows specified.

**Pattern Completeness:**
Naming conventions cover all new layers (graph, agent, KG API). AGE Cypher parameterization pattern defined. Agent-backend HTTP contract specified. Error handling patterns defined for agent boundary, validation failure, and embedding failure. LangGraph/PydanticAI/LangChain boundary rules documented. Enforcement guidelines with verification methods documented.

### Gap Analysis Results

**Critical Gaps:** None

**Important Gaps (addressed):**
- Validation failure auto-correct pattern defined with max retry loop
- Agent authentication via `X-Agent-Key` (shared secret) specified

**Nice-to-Have (deferred to implementation):**
- Exact AGE Cypher query syntax for each KG service method (implementation detail)
- LangGraph checkpointer configuration (schema, table names — implementation detail)
- PydanticAI model/provider configuration and exact package version (implementation detail)
- Agent system prompt content (implementation detail)
- BMAD markdown template structure (implementation detail)
- nginx proxy config update for agent internal access (not needed — internal network only)

### Architecture Completeness Checklist

**Requirements Analysis**

- [x] Project context thoroughly analyzed
- [x] Scale and complexity assessed
- [x] Technical constraints identified
- [x] Cross-cutting concerns mapped

**Architectural Decisions**

- [x] Critical decisions documented with versions
- [x] Technology stack fully specified
- [x] Integration patterns defined
- [x] Performance considerations addressed

**Implementation Patterns**

- [x] Naming conventions established
- [x] Structure patterns defined
- [x] Communication patterns specified
- [x] Process patterns documented

**Project Structure**

- [x] Complete directory structure defined
- [x] Component boundaries established
- [x] Integration points mapped
- [x] Requirements to structure mapping complete

### Architecture Readiness Assessment

**Overall Status:** READY FOR IMPLEMENTATION

**Confidence Level:** High — all decisions consistent, all requirements covered, patterns comprehensive, structure complete.

**Key Strengths:**
- Clean separation between backend (data management) and agent (LLM orchestration)
- KG API as domain-specific layer prevents raw Cypher/SQL leakage to agents
- One graph per project provides natural multi-tenant isolation
- Existing scaffold patterns (Router → Service → Model, API client) extended naturally to new components
- Agent-backend HTTP contract enables independent deployment and testing
- Validation failure pattern (auto-correct → escalate → save what exists) is pragmatic for MVP

**Areas for Future Enhancement:**
- Additional skills (PRD, architecture, UX agents) will reuse KG API and agent container pattern
- Multiple brainstorm sessions per package will require session management changes
- Context-aware re-embedding with similarity thresholds for idea deduplication
- Neo4j migration path if graph complexity outgrows AGE

### Implementation Handoff

**AI Agent Guidelines:**

- Follow all architectural decisions exactly as documented in this file
- Follow the existing scaffold architecture patterns for all shared components
- Use implementation patterns consistently — no deviations without explicit approval
- Respect container boundaries — agent never imports from thagid package directly
- Refer to `design-system/thagid/MASTER.md` for all UI decisions
- Parameterize all AGE Cypher queries — never string-concatenate

**First Implementation Priority:**

1. Build custom PostgreSQL image with AGE + pgvector
2. Set up KG service + router in backend
3. Build agent container with LangGraph orchestration and PydanticAI agent nodes
