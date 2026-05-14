---
stepsCompleted: [1, 2, 3, 4]
session_active: false
workflow_completed: true
inputDocuments: []
session_topic: 'Data architecture for Thagid skill pipeline - token-lean storage, retrieval, and data flow'
session_goals: 'Design structured data model, RAG retrieval strategy, and dual-output system compatible with BMAD docs'
selected_approach: 'ai-recommended'
techniques_used: ['First Principles Thinking', 'Constraint Mapping', 'Morphological Analysis']
ideas_generated: []
context_file: ''
---

# Brainstorming Session Results

**Facilitator:** Fmorais
**Date:** 2026-05-06

## Session Overview

**Topic:** Data lifecycle for Thagid skills — what data each skill needs, how to store it, how to retrieve it, how to ensure accuracy and relevance. Replacing BMAD's full-document-per-skill pattern with structured storage + RAG retrieval.

**Goals:**
1. Understand what data each skill needs as input and produces as output
2. Design a storage model that's token-lean (structured data, not monolithic docs)
3. Design a retrieval strategy (RAG-based, fetch what's needed)
4. Ensure dual-output compatibility (BMAD docs + Thagid-optimized data)
5. Address the scaling problem (large PRDs/architecture docs becoming unwieldy)

### Key Constraints

- Must produce BMAD-compatible documents as one output
- Must also produce structured data optimized for downstream Thagid consumption
- Dogfooding: using Thagid to build Thagid
- Hybrid model: some skills still BMAD, some Thagid, coexisting

## Technique Selection

**Approach:** AI-Recommended Techniques
**Analysis Context:** Data architecture for Thagid skill pipeline with focus on token-lean storage, RAG retrieval, dual-output compatibility

**Recommended Techniques:**

- **First Principles Thinking:** Strip away BMAD's assumptions about data flow. Rebuild from fundamental truths about what each skill actually needs as input/output.
- **Constraint Mapping:** Map all real constraints: BMAD doc compat, RAG limitations, token budgets, scaling, hybrid model. Distinguish real vs assumed constraints.
- **Morphological Analysis:** Systematically explore all combinations of storage formats × retrieval strategies × indexing approaches × consistency mechanisms.

**AI Rationale:** This is a complex systems design problem requiring deep analytical thinking. The sequence builds from fundamental understanding (what data is truly needed) through boundary definition (what constraints are real) to systematic solution exploration (all viable architecture combinations).

## Phase 1: First Principles Thinking — Results

### Core Insight: Dissolve the Documents

BMAD's fundamental problem: each skill reads entire upstream documents. But skills only need specific data points. The monolithic document (PRD, Architecture, UX) is a bad abstraction for large products.

**Solution:** Atomic entities stored as graph nodes. No monolithic documents. Each entity is discrete, referenceable, relatable, and independently retrievable.

### Node Types

- **FR** (Functional Requirement) — id, actor, capability, category, priority, scope_phase
- **NFR** (Non-Functional Requirement) — id, category, threshold, measurement_criteria
- **ADR** (Architecture Decision Record) — id, context, decision, consequences, status
- **Epic** — id, title, goal, fr_coverage
- **Story** — id, epic_id, user_story, acceptance_criteria, tasks, dev_notes, status, dependencies
- **Journey** — id, narrative, emotional_arc, actors, journey_requirements
- **Pattern** — id, name, description, type (naming/structure/format/communication/process)
- **DBSchema** — id, entities, relationships, constraints
- **APISpec** — id, endpoints, contracts, versioning
- **Component** — id, name, description, design_tokens, interaction_patterns
- **SuccessCriteria** — id, user_success, business_success, technical_success, measurable_outcomes
- **ContextChunk** — id, text, domain, relevant_roles, work_package (atmospheric, not discretely related)
- **Mandate** — id, text, source, scope

### Two Content Types

1. **Relational entities** — discrete nodes with typed edges to other nodes. FRs, ADRs, Stories, etc.
2. **Contextual chunks** — narrative text retrieved by similarity, not by relationship. Design philosophy, vision statements, emotional arcs. Stored as lightweight nodes with metadata tags and embeddings, but without fine-grained relationship edges.

### Role Directives (Not Graph Nodes)

Design philosophy, coding standards, testing standards, architecture principles — these are **documents**, not graph nodes. Stored separately in a document/config store, loaded per agent role. Like an AGENTS.md for each agent type.

### Edge Types (11 typed relationships)

| Edge | From → To | Meaning |
|------|-----------|---------|
| PART_OF | Story → Epic, FR → WorkPackage | Membership |
| COVERS | Epic → FR | This epic covers these FRs |
| IMPLEMENTS | Story → FR | Story implements this FR |
| IMPACTS | FR → NFR, ADR → FR, Change → Story | Affects |
| DEPENDS_ON | Story → Story, FR → FR | Requires |
| DERIVED_FROM | FR → Journey, NFR → SuccessCriteria | Originates from |
| CONSTRAINS | NFR → FR, Mandate → FR | Limits |
| DECIDES | ADR → Pattern, ADR → TechChoice | Determines |
| REFERENCES | Story → DBSchema, Story → APISpec, Story → Component | Uses |
| SUPERSEDES | ADR → ADR | Replaces |
| INFORMS | ContextChunk → WorkPackage | Provides context for |

### Retrieval Model: Creator vs Executor Agents

| | Creator Agents (Architect, PO, UX) | Executor Agents (Developer, Tester) |
|---|---|---|
| Primary mode | Discovery | Prescription |
| Primary query | Vector search | Graph traversal |
| Creates | New nodes + relationships | Code + test artifacts |
| Consumes | Semantic context, impact analysis | Story → FR → Pattern → Schema path |
| Context shape | Wide, exploratory | Narrow, prescribed |
| Token profile | Higher but targeted | Lower, more deterministic |

### Two-Layer Retrieval

1. **Layer 1: Role config** — always loaded, from document store (design philosophy for UX, coding standards for dev)
2. **Layer 2: Task dynamic** — queried per task. Creators use vector search seeded by task description. Executors follow prescribed graph paths.

### Token Efficiency Mechanism

Not compressing data — **not retrieving what the agent doesn't need.** Agent role determines which subgraph to traverse. Architect gets ADRs, developer doesn't. Developer gets patterns and schemas, architect gets them only when relevant to the task.

## Phase 2: Constraint Mapping — Results

### Hard Constraints

| # | Constraint | Notes |
|---|-----------|-------|
| 1 | BMAD markdown output during hybrid | Downstream unconverted skills need it |
| 2 | Topological conversion order | Can't convert downstream before upstream |
| 3 | Immutable artifacts | No user editing, only skills modify data |
| 4 | Solo developer, operational simplicity | One container, one DB preferred |
| 5 | Token efficiency, measurable | Core value prop |
| 6 | Schema evolution, backwards-compatible | Graph schema grows as skills migrate |
| 7 | Multi-agent concurrency | Postgres MVCC handles isolation |
| 8 | Multi-tenant: graph per project | Organization → Projects → Graph |
| 9 | Graph access layer abstraction | Don't couple agents to AGE specifics |
| 10 | Standard Cypher patterns only | Keep Neo4j migration path open |
| 11 | Python/FastAPI/Podman stack | Given |
| 12 | GitHub Projects for kanban | Given |
| 13 | Webhook events from GitHub | Given |

### Accepted Tradeoffs

| # | Tradeoff | Acceptance |
|---|---------|------------|
| 1 | Postgres + AGE + pgvector | Decided. Design for migration at scale. |
| 2 | Node versioning for auditability | Accepted. Every update = new version. |
| 3 | Embedding model lock-in | Accepted. Re-embed everything if model changes. |
| 4 | Scale ceiling ~100K active nodes | Accepted. Archive old nodes. Migrate if needed. |

### Constraint Evaluation

- Embedding cost: effectively zero (~$0.0005 for full corpus)
- Real cost is LLM calls for relationship evaluation, mitigated by vector similarity proxy
- Concurrency: Postgres MVCC + short-lived agent sessions
- No local LLM decision yet — embedding model choice deferred

## Phase 3: Morphological Analysis — Results

### Dimension 1: Storage — DECIDED
Postgres + AGE (graph) + pgvector (embeddings). Single database, single container.

### Dimension 2: Embedding Pipeline — DECIDED
- **2a. Timing:** Async on write. Node created, embedding computed in background. Seconds gap.
- **2b. Content:** Text + lightweight metadata. Configurable per node type. (Details deferred to implementation)
- **2c. Refresh:** Context-aware. Re-embed changed node + check neighbor similarity. Flag for LLM review if threshold crossed.

### Dimension 3: Retrieval API — DECIDED
**Domain-specific methods (Approach A).** Agents call typed methods, never write Cypher/SQL directly.

```python
kg = KnowledgeGraph(project_id="thagid-1")

# Creator queries
frs = kg.search_similar("authentication", node_type="FR", limit=5)
adrs = kg.search_similar("authentication", node_type="ADR", limit=3)
impact = kg.impact_analysis(node_id="FR3", depth=3)

# Executor queries
context = kg.get_story_context(story_id="2-4")

# Writes
kg.create_node(type="ADR", properties={...}, relationships=[...])
kg.update_node(id="FR3", properties={...})
```

~15-20 distinct method types. Deterministic, controlled, no agent exposure to graph complexity.

### Dimension 4: Versioning — DECIDED
Node versioning. Every update creates new version (same id, version+1). Old versions kept. Indexed. Store agent_id + change summary per version.

### Dimension 5: Concurrency — DECIDED
Postgres MVCC. Short-lived agent sessions. Load context fresh per task.

### Dimension 6: BMAD Compatibility — DECIDED
**Separate markdown renderer (Option B).** Skills write to graph only. A renderer service reads graph nodes and produces BMAD-format markdown documents. Decoupled. Skills don't contain rendering logic. Markdown deprecation = turn off the renderer.

### Dimension 7: Data Access Abstraction — DECIDED
Clean Python module between LangGraph agents and database. Domain-specific methods encapsulate Cypher/SQL. Migration to Neo4j (if ever) = rewrite data access layer, not agents.

---

## Complete Data Layer Architecture

```
┌─────────────────────────────────────────────────────┐
│                    Thagid Application                │
│                                                     │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────┐ │
│  │ Creator     │  │ Executor     │  │ Renderer   │ │
│  │ Agents      │  │ Agents       │  │ Service    │ │
│  │ (Arch,PO,UX)│  │ (Dev,Tester) │  │ (BMAD MD)  │ │
│  └──────┬──────┘  └──────┬───────┘  └─────┬──────┘ │
│         │                │                 │        │
│         ▼                ▼                 ▼        │
│  ┌─────────────────────────────────────────────┐   │
│  │         Knowledge Graph API (Python)         │   │
│  │   Domain-specific methods ~15-20 types       │   │
│  │   create_node, update_node, search_similar,  │   │
│  │   impact_analysis, get_story_context, ...    │   │
│  └──────────────────┬──────────────────────────┘   │
│                     │                               │
│         ┌───────────┼───────────┐                   │
│         ▼           ▼           ▼                   │
│  ┌───────────┐ ┌─────────┐ ┌──────────┐           │
│  │   AGE     │ │ pgvector│ │ Postgres │           │
│  │  (graph)  │ │(vectors)│ │(relational│           │
│  │           │ │         │ │  tables)  │           │
│  └───────────┘ └─────────┘ └──────────┘           │
│         │           │           │                   │
│         └───────────┼───────────┘                   │
│                     ▼                               │
│              ┌─────────────┐                        │
│              │  PostgreSQL  │                        │
│              │  (single DB) │                        │
│              └─────────────┘                        │
└─────────────────────────────────────────────────────┘

Supporting Infrastructure:
┌──────────────────┐  ┌──────────────────────┐
│ Role Config Store │  │ Async Embedding      │
│ (documents per   │  │ Pipeline              │
│  agent role)     │  │ (on-write trigger)    │
└──────────────────┘  └──────────────────────┘
```

### Data Flow

```
Skill runs → Creates/updates nodes via KG API
                │
                ├──→ Async: compute embedding, store in node
                ├──→ Async: check neighbor similarity, flag if needed
                ├──→ Async: renderer service generates BMAD markdown
                └──→ Node version history recorded

Agent runs → Queries KG API
                │
                ├──→ Creator: vector search + graph traversal
                └──→ Executor: graph traversal (prescribed path)
```

### Multi-Tenant Scope

```
Organization → Projects → Graph (project_id on every node)
                       → Role Config (per project)
                       → App Data (users, sessions, config)
```

### Migration Strategy

If scale demands Neo4j:
1. Data access layer abstracts database
2. Agents untouched
3. Rewrite data access layer from AGE to Neo4j
4. Standard Cypher patterns used throughout (portable)
5. Markdown renderer untouched (reads from same API)

## Idea Organization and Prioritization

### Thematic Organization

**Theme 1: Data Model — Atomic Entities**
- Dissolve monolithic documents into atomic graph nodes
- Two content types: relational entities (discrete edges) and contextual chunks (similarity-retrieved)
- Role directives stored as documents, not graph nodes
- 13+ node types, 11 typed edge relationships

**Theme 2: Storage — Single Database**
- Postgres + AGE + pgvector in one container
- Multi-tenant: graph per project, project_id on every node
- Node versioning for full audit trail

**Theme 3: Retrieval — Role-Based, Token-Lean**
- Domain-specific API (~15-20 methods), agents never see Cypher/SQL
- Creator agents: vector search primary (discovery)
- Executor agents: graph traversal primary (prescribed path)
- Two-layer retrieval: role config (always) + task dynamic (per query)

**Theme 4: Embedding Pipeline**
- Async on write, background computation
- Context-aware re-embedding on node changes
- Vector similarity as cheap proxy for relationship review

**Theme 5: BMAD Compatibility**
- Separate markdown renderer reads graph, produces BMAD docs
- Skills write to graph only, renderer is decoupled
- Gradual deprecation: turn off renderer when no skill needs markdown

**Theme 6: Migration Safety**
- Clean data access abstraction, agents decoupled from AGE
- Standard Cypher patterns for Neo4j migration path
- Design for migration, not for scale not yet reached

### Prioritized Action Plan

**Priority 1: Knowledge Graph API Abstraction Layer**
Foundation everything else builds on. Must exist before any skill migration.
- Define ~15-20 domain-specific methods
- Implement against a testable interface (start with in-memory mock)
- Success: API spec documented and reviewed

**Priority 2: Infrastructure Setup**
Need the database running before implementing anything.
- Postgres + AGE + pgvector in podman-compose
- Graph schema (node types, edge types, indexes)
- pgvector configuration (dimensions, index type)
- Success: Can create/query/embed nodes via AGE + pgvector

**Priority 3: Embedding Pipeline**
Async on-write pipeline needed before first skill produces data.
- Embedding computation on node creation/update
- Neighbor similarity check on update
- Configurable per node type (details deferred)
- Success: Node created, embedding appears, similarity check runs

**Priority 4: First Skill Migration (Proof of Concept)**
Validates the entire architecture end-to-end.
- Pick one upstream skill (e.g., product brief or PRD subset)
- Implement as LangGraph agent writing to graph via API
- Build BMAD markdown renderer for that document type
- Success: Skill produces both graph data and BMAD markdown, downstream BMAD skill consumes the markdown

**Priority 5: Version History + Concurrency**
Needed once multiple agents interact with the graph.
- Node versioning (every update = new version)
- Short-lived agent session management
- Success: Concurrent agent access with audit trail

## Session Summary and Insights

### Key Achievements

- Designed complete data layer architecture for Thagid's knowledge graph
- Established atomic entity model replacing monolithic documents
- Defined retrieval strategy split by agent role (creators vs executors)
- Resolved database choice with pragmatic decision and migration path
- Mapped all hard constraints and accepted tradeoffs
- Created prioritized implementation roadmap

### Key Session Insights

- The real token savings come from not retrieving what an agent does not need, not from compressing data
- Creator agents create relationships and use vector search; executor agents consume relationships via graph traversal
- Embedding cost is effectively zero; real cost is relationship evaluation
- Postgres + AGE + pgvector is pragmatic for prototype; clean abstraction layer enables future migration
- BMAD markdown output during hybrid period is best handled by a separate renderer service
- Graph schema is bounded (SDLC artifacts) — ~11 edge types should stabilize quickly
- Multi-tenant scope (org, project, graph) is a hard constraint that shapes everything

### Breakthrough Moments

- Dissolving monolithic documents into atomic entities shifts the entire mental model
- Two-layer retrieval (role config + task dynamic) separates always-needed from task-relevant
- Markdown renderer as a separate service enables clean deprecation path
- Context-aware re-embedding with vector similarity as cheap proxy avoids unnecessary LLM calls
