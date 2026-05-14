---
project_name: 'Thagid'
user_name: 'Fmorais'
date: '2026-05-12'
sections_completed:
  ['technology_stack', 'language_rules', 'framework_rules', 'testing_rules', 'quality_rules', 'workflow_rules', 'agent_rules', 'kg_rules', 'anti_patterns']
status: 'complete'
rule_count: 106
optimized_for_llm: true
architecture_sources:
  - path: '_bmad-output/planning-artifacts/architecture.md'
    date: '2026-05-12'
---

# Project Context for AI Agents

_This file contains critical rules and patterns that AI agents must follow when implementing code in this project. Focus on unobvious details that agents might otherwise miss._

---

## Technology Stack & Versions

**Backend:**
- Python 3.12+ (fastapi>=0.115, uvicorn>=0.34, sqlalchemy>=2.0, asyncpg, alembic, pydantic>=2.0, python-jose[cryptography], httpx>=0.28)
- Brainstorm agent: LangGraph 1.1.x, langgraph-checkpoint-postgres, PydanticAI, FastAPI agent service
- Tests: pytest>=8.0, httpx (via TestClient)
- Container: Podman + Podman Compose

**Frontend:**
- SvelteKit 2, Svelte 5 (runes), TypeScript (strict), Vite
- shadcn-svelte (CLI-managed), TailwindCSS v4, lucide-svelte
- Tests: Vitest (unit, co-located), Playwright (e2e in `web/e2e/`)

**Database:** PostgreSQL 16 container, SQLAlchemy 2.0 async (asyncpg driver), Apache AGE, pgvector (`vector(1536)`)

**Infrastructure:** nginx (SPA serving + reverse proxy), Cloudflare tunnel (dev only)

## Critical Implementation Rules

### Architecture Pattern

- **Backend:** Router → Service → Model. Routers handle HTTP only. Services contain business logic. Models define schema. No shortcuts.
- **Frontend:** Pages call API client functions. API client functions update stores. Components read stores. Never skip a layer.
- **Agent:** `thagid-agent` is a separate FastAPI container/package under `agent/`; it never imports from `thagid` and communicates with FastAPI over internal HTTP.
- **Agent ownership:** LangGraph owns conversation/workflow state. PydanticAI owns individual agent execution. The DB owns business records/audit records.
- **Agent flow:** FastAPI chat API → LangGraph thread/session → LangGraph orchestration + checkpointing → PydanticAI agent nodes → tools / MCP / git / shell / project APIs.
- **Knowledge Graph:** `KnowledgeGraphService` owns all AGE + pgvector operations; other code uses its domain API, not raw graph access.

### Naming Conventions

- **Python:** snake_case functions/variables, PascalCase classes
- **TypeScript:** camelCase functions/variables, PascalCase types/components
- **Database:** plural snake_case tables (`organisations`, `projects`), snake_case columns, FKs as `{table_singular}_id`
- **API JSON:** snake_case fields (`created_at`, `org_id`)
- **Svelte files:** PascalCase components (`ChatBubble.svelte`)
- **IDs:** UUID v4 strings everywhere — never expose integers
- **AGE graph:** graph names are `project_{normalized_uuid}` with lowercase UUID hyphens replaced by underscores; use one helper to normalize/validate.
- **AGE schema:** node labels PascalCase (`Session`), relationship types UPPER_SNAKE_CASE (`HAS_THEME`), properties snake_case.
- **Agent package:** `agent.brainstorm`, `agent.tools`, `agent.state`; one LangGraph node function per file in `agent/brainstorm/nodes/`; PydanticAI `Agent` instances execute inside nodes.

### API Format

- Single resource: `{ "id": "uuid", ... }`
- List: `{ "items": [...], "total": N }`
- Error: `{ "detail": "message" }`
- Dates: ISO 8601 (`"2026-05-06T14:30:00Z"`)
- Status codes: 200/201/204/400/401/403/404/422
- User-facing brainstorm routes live under `/api/packages/{package_id}/brainstorm/...` and use JWT auth.
- Internal KG routes live under `/internal/kg/projects/{project_id}/...` and require `X-Agent-Key`; browser traffic must never call them.
- Agent internal routes live under `/internal/agent/...`; browser traffic must never call the agent directly.

### Frontend State

- Svelte writable stores in `$lib/stores/` for global state (auth, scope)
- Local `$state` for UI-only concerns (form inputs, dropdowns)
- URL params drive scope resolution — page loads populate stores
- Components never directly mutate stores — call API functions

### Frontend API Client

- All API calls go through `$lib/api/client.ts` wrapper — no raw `fetch()` in components
- Global error handling: 500-level errors show toast, 401 redirects to sign-in
- Auth via HTTP-only cookie — no manual token management

### Backend Layer Rules

- One model per file in `thagid/models/`
- One Pydantic schema set per file in `thagid/schemas/` (Create, Update, Response)
- One router per resource in `thagid/routers/`
- One service per domain in `thagid/services/`
- Services receive `AsyncSession` — never create their own
- Services raise domain exceptions — routers map to HTTP status
- No service imports another service
- KG node types are `Session`, `Theme`, `Idea`, `ContextChunk`; relationships are `HAS_THEME`, `CONTAINS_IDEA`, `USES_CONTEXT`, `VERSION_OF`.
- KG updates create a new node version linked by `VERSION_OF`; previous versions are preserved for audit history.
- AGE Cypher must be parameterized through `cypher()` with parameter payloads; never interpolate IDs, graph values, or properties into Cypher strings.
- Embedding columns live in dedicated relational tables, not AGE node properties; column name `embedding`, type `vector(1536)`, HNSW index using `vector_cosine_ops`, nullable while async computation is pending.

### Auth Flow

- Backend verifies Google ID token, creates/finds user, returns JWT in HTTP-only cookie
- `get_current_user` dependency on all `/api/*` routes
- All data scoped by `user.org_id` — enforced in service layer
- Frontend root layout: no session → `/sign-in`, no org → `/org/create`
- Agent → FastAPI calls authenticate with `X-Agent-Key`; this shared secret is for internal service calls only, not user auth.

### Design System

- All UI must follow `design-system/thagid/MASTER.md` and page-specific overrides
- Use shadcn-svelte components — do not create custom versions of existing shadcn components
- Custom components go in `$lib/components/custom/`
- Colors: navy primary `#0A3B85`, green CTA `#22C55E`
- Font: Plus Jakarta Sans
- Icons: lucide-svelte only

### Testing

- Backend tests in `thagid/tests/` using pytest + httpx TestClient
- Frontend unit tests co-located: `Component.test.ts` next to `Component.svelte`
- E2E tests in `web/e2e/` using Playwright
- Agent tests live under `agent/tests/` and run with pytest
- KG/brainstorm backend changes need pytest coverage for service/router behavior; frontend brainstorm UI changes need Vitest and Playwright where applicable
- No comments in code unless explicitly requested

### Brainstorm Agent & KG Rules

- FastAPI proxies frontend brainstorm messages to `thagid-agent`; browser-to-agent traffic is forbidden.
- FastAPI chat routes user messages into a LangGraph thread/session; LangGraph then routes workflow execution and resumes from checkpoints.
- Agent responses follow the agreed shape: `reply`, `session_id`, `state_change`, `ideas`, `themes`, `markdown`.
- LangGraph state persists messages, ideas, themes, active documents, summary, technique, package_id, and session_id via PostgreSQL checkpointing.
- Use LangGraph for conversation thread state, approval pauses, resume after user input, retry loops between nodes, long-running workflow state, and checkpoint history.
- Use PydanticAI for LLM calls, tool registration, typed outputs, tool argument validation, agent-level retry, and structured result parsing.
- Business records and audit records belong in the DB/KG, not in LangGraph checkpoints or PydanticAI runtime state.
- Application code may use PydanticAI `Agent`, Pydantic models, and LangGraph `StateGraph`/checkpointing/orchestration primitives.
- Application code must not use LangChain agents, chains, tools, memory, prompts, message classes, or Runnable/RunnableConfig.
- Brainstorm validation auto-corrects structural issues: orphan ideas → `General`, empty themes removed, missing summaries generated.
- If validation finds no meaningful ideas/themes, route back to facilitation with a user-facing explanation; cap extract/validate/facilitate retry loops at 2.
- Embedding writes are async/fire-and-forget after KG node writes; failed embeddings leave graph nodes intact and are logged.
- PydanticAI handles agent-level LLM retry with exponential backoff, max 3 attempts; LangGraph handles retry loops between nodes; KG write failures during extraction surface as errors through FastAPI.

### Container Topology

```
podman-compose: thagid (FastAPI :8000) | thagid-web (nginx :3000) | thagid-agent (FastAPI :8001 internal) | postgres (PostgreSQL 16 + AGE + pgvector :5432 internal) | pgadmin/age-viewer (dev only) | cloudflared (host network)
```

- Dev: Vite (`:5173`) proxies `/api/` to FastAPI (`:6969`). Run `podman-compose up thagid thagid-agent postgres` + `npm run dev` in `web/`
- Prod: nginx serves SPA static, proxies `/api/`, `/auth/`, `/webhook` to FastAPI; agent remains internal only
- Cloudflare tunnel routes to `:3000` (nginx)
- FastAPI reaches agent at `http://thagid-agent:8001`; agent reaches FastAPI at `http://thagid:8000`; agent may connect to PostgreSQL only for LangGraph checkpointing.

### Anti-Patterns (NEVER DO)

- Business logic in routers or components
- Raw `fetch()` in Svelte components — always use `$lib/api/` wrapper
- SQLAlchemy models leaked directly in API responses — always use Pydantic schemas
- Hardcoded colors/spacing — use design system tokens
- Editing `ui/` components directly — they are CLI-managed by shadcn-svelte
- Mixing camelCase and snake_case within a single layer
- Adding comments unless explicitly requested
- Using integer auto-increment IDs — always UUID
- Agent importing `thagid` modules or calling KG service directly — use internal HTTP instead
- Using LangChain agents, chains, tools, memory, prompts, message classes, or Runnable/RunnableConfig in application code
- Storing conversation/workflow state in PydanticAI instead of LangGraph checkpoints
- Storing business records or audit records only in LangGraph checkpoints instead of the DB/KG
- String interpolation or f-strings inside AGE Cypher calls
- Storing embeddings inside AGE graph properties instead of relational embedding tables
- Exposing `/internal/kg/*` or `thagid-agent` directly to the browser/nginx public routes

---

## Usage Guidelines

**For AI Agents:**
- Read this file before implementing any code
- Follow ALL rules exactly as documented
- When in doubt, prefer the more restrictive option
- Update this file if new patterns emerge

**For Humans:**
- Keep this file lean and focused on agent needs
- Update when technology stack changes
- Review quarterly for outdated rules
- Remove rules that become obvious over time

Last Updated: 2026-05-12
