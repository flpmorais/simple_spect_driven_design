# Architecture Blueprint Contract

Apply this contract for Architecture Blueprint creation.

## Interaction Model

The Architecture Blueprint skill is an interactive architecture recommendation sparring partner, not a blind generator.

- Produce source-backed architecture recommendations with confidence labels, not generic concern inventories.
- Ask focused questions by decision cluster. Ask at most 3 questions at a time.
- Create tension before capturing a recommendation: name the viable alternatives, why they compete, and what would make each appropriate.
- Use AI suggestions as proposals for the user to confirm, correct, reject, or mark unknown.
- Store only content grounded in Product Blueprint memory, Product Brief memory when used, direct user input, user-approved synthesis, or explicit assumptions approved through review.
- Do not draft the final artifact until the user has shaped the recommendation set through the interactive flow.
- If evidence is insufficient, record `Unknown` only for that decision area and explain what is missing. Do not invent certainty.
- Keep the flow token-lean: avoid repeated rationale, avoid full-document restatements during discovery, and prefer compact tables and bullets.

Use these confidence labels:

- `Strong recommendation`: enough evidence to treat this as the intended architecture choice unless Phase 1 disproves a specific assumption.
- `Likely right`: best current choice, but one meaningful unknown remains.
- `Weak recommendation`: plausible choice, but Phase 1 must validate early before downstream planning depends on it.
- `Unknown`: insufficient evidence to recommend; use sparingly and explain the missing input.

## Artifact Boundary

The Architecture Blueprint captures high-confidence architecture recommendations before Phase 1 planning. It answers: what architecture choices should we expect to make, why, what compromises are acceptable, what alternatives lost, and what Phase 1 must validate.

Include concrete recommendations for major technical decision areas, confidence labels, rationale, ideal approaches, acceptable compromises, rejected alternatives, important dependencies, open risks, and Phase 1 validation needs.

Exclude generic principles, broad concern inventories, detailed design, data models, API specifications, deployment manifests, implementation tasks, release plans, work packages, and unsupported technology choices.

## Required Sections

The Architecture Blueprint is stored as SQLite-backed `Artifact` memory with kind `architecture-blueprint`. Use these exact section keys and headings:

| Section Key | Heading |
| --- | --- |
| `architecture-recommendations` | Architecture Recommendations |
| `decision-coverage` | Decision Coverage |
| `open-risks` | Open Risks |
| `phase-1-validation` | Phase 1 Validation |

Unsupported sections must state `Unknown` or a clear assumption. Do not invent content.

## Required Decision Coverage

The skill must address these decision areas. Expand relevant areas in `architecture-recommendations`; summarize every area in `decision-coverage`.

| Area | Examples To Consider |
| --- | --- |
| Product surface | Responsive web, PWA, native mobile, desktop app, CLI, browser extension. |
| Deployment model | Serverless, VPS, containers, managed app platform, static plus backend, edge runtime. |
| Data store | No DB, SQLite, Postgres, Supabase/Firebase, graph, vector, object storage. |
| Authentication | None, Google-only, email/password, social auth, enterprise SSO/Okta. |
| Authorization | None, two roles, RBAC, object permissions, tenant permissions, policy engine. |
| User/account management | Admin-created, invite-based, self-registration, organizations/teams, lifecycle management. |
| Multi-tenancy | None, simple organization boundary, strict tenant isolation. |
| Observability | Logs, error tracking, metrics, tracing, audit logs, product analytics. |
| Background work | None, cron, queues, workers, event-driven jobs, long-running jobs. |
| AI/search | None, LLM calls, RAG, vector DB, full-text search. |
| Integrations | None, third-party APIs, webhooks, imports/exports, sync jobs. |
| File/media handling | None, uploads, object storage, CDN, processing. |
| Security/compliance | Secrets, PII, encryption, auditability, retention, regulated workflows. |
| Payments/billing | None, Stripe checkout, subscriptions, invoices, usage billing. |
| DevOps/release | Manual deploy, CI/CD, preview environments, migrations, backups, rollback. |

Use these `decision-coverage` statuses:

- `Recommended`: a recommendation exists or is summarized.
- `Not needed`: the area is intentionally excluded with rationale.
- `Unknown`: evidence is insufficient and the missing input is named.

## Recommendation Format

Use this compact structure for each recommendation:

```md
### <Decision Area>

- Recommendation: <specific architecture choice>
- Confidence: Strong recommendation | Likely right | Weak recommendation | Unknown
- Why: <source/user-backed rationale>
- Ideal approach: <best-fit long-term pattern/technology>
- Acceptable compromise: <v1-safe simplification>
- Rejected alternatives: <alternatives and why they lost>
- Dependencies: <only if this affects another decision>
- Phase 1 validation: <what must be verified>
```

Omit `Dependencies` only when none matter. Do not omit `Phase 1 validation` unless the decision area is `Not needed`.

## Interactive Workflow

Use this sequence:

1. Load Product Blueprint memory and optional Product Brief memory.
2. Extract only the architecture pressures needed for the first decision cluster.
3. Walk these clusters in order: surface/deployment; data/files/search/AI; authentication/authorization/accounts/tenancy; observability/background work/DevOps; integrations/security/compliance/payments.
4. For each cluster, present the real tension and a proposed recommendation for each relevant decision area.
5. Ask the user to confirm, correct, reject, choose another alternative, or mark unknown. Ask at most 3 questions at a time.
6. Capture accepted or user-shaped recommendations in working context.
7. Keep `Not needed` areas short with rationale.
8. After all areas are covered, draft the four required sections for review.
9. Revise until the user approves the full artifact.

## Review And Memory Write

Review the payload before presenting it. Do not write while it has:

- missing required decision coverage;
- a `Recommended` area without a specific recommendation;
- a relevant decision area hidden in `open-risks` instead of recommended or marked unknown;
- confidence labels outside the allowed set;
- generic principles or concern inventories;
- unsupported specificity;
- recommendations presented as facts when they are assumptions;
- repeated rationale across sections;
- open risks that are not capable of overturning recommendations;
- Phase 1 validation that becomes an implementation plan;
- unresolved contradiction with Product Blueprint, Product Brief, or user-approved synthesis.

Present the four sections in human-readable Markdown and ask for explicit approval to create durable memory. Do not write Architecture Blueprint memory until the user approves after reviewing the final sections.

## Memory Write

After interactive discovery, internal review, and final user approval, write Architecture Blueprint memory through `.opencode/scripts/ssd_architecture_blueprint/memory.py`.

Create command:

```text
python .opencode/scripts/ssd_architecture_blueprint/memory.py create
```

Pass the JSON payload on stdin. The payload shape is:

```json
{
  "change_summary": "Initial Architecture Blueprint",
  "product_blueprint_artifact_id": "<uuid>",
  "product_brief_artifact_id": "<uuid or omitted>",
  "sections": {
    "architecture-recommendations": "...",
    "decision-coverage": "...",
    "open-risks": "...",
    "phase-1-validation": "..."
  },
  "source_brainstorms": [],
  "cited_idea_ids": []
}
```

The memory adapter stores the Architecture Blueprint as current `Artifact` and `ArtifactSection` memory, with provenance relationships to the source Product Blueprint, optional source Product Brief, source brainstorms, and cited ideas.

Do not create Architecture Blueprint markdown files or temp markdown drafts.
