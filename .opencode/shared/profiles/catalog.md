# SSD Analysis Profile Catalog

Profiles are stable IDs. Calling skills select a profile from this catalog, then invoke `ssd_profile_analyzer` with `profile_id` and input. Profiles are analysis lenses, not personas.

## architects

### conservative-enterprise-architect

Name: The Conservative Enterprise Architect
Category: architect
Path: `.opencode/shared/profiles/architects/conservative-enterprise-architect.md`
Fit: stability, operational maturity, vendor support, auditability, boring tech
Best at: avoiding catastrophic platform mistakes
Avoid when: the goal is intentionally exploratory, disruptive, or innovation-first

### pragmatic-delivery-architect

Name: The Pragmatic Delivery Architect
Category: architect
Path: `.opencode/shared/profiles/architects/pragmatic-delivery-architect.md`
Fit: shipping, developer productivity, reducing accidental complexity, team capability
Best at: grounding architecture discussions in delivery reality
Avoid when: the main risk is future hyperscale, deep regulatory exposure, or adversarial threat modeling

### scalability-distributed-systems-architect

Name: The Scalability/Distributed Systems Architect
Category: architect
Path: `.opencode/shared/profiles/architects/scalability-distributed-systems-architect.md`
Fit: scale, resilience, throughput, distributed correctness, blast radius analysis
Best at: identifying future bottlenecks early
Avoid when: the system is intentionally small, short-lived, or not expected to need distributed complexity

### security-compliance-architect

Name: The Security & Compliance Architect
Category: architect
Path: `.opencode/shared/profiles/architects/security-compliance-architect.md`
Fit: threat models, identity, audit, legal exposure, regulatory exposure
Best at: preventing invisible existential risks
Avoid when: the decision is low-risk and speed matters more than formal control design

### cost-efficiency-architect

Name: The Cost Efficiency Architect
Category: architect
Path: `.opencode/shared/profiles/architects/cost-efficiency-architect.md`
Fit: infrastructure spend, operational efficiency, total cost of ownership, cloud bill exposure
Best at: exposing hidden operational cost
Avoid when: managed-service leverage or strategic speed is more important than near-term cost control

### ai-automation-native-architect

Name: The AI/Automation-Native Architect
Category: architect
Path: `.opencode/shared/profiles/architects/ai-automation-native-architect.md`
Fit: AI-assisted development, agentic systems, automation leverage, semantic workflows
Best at: future-proofing for AI-native operations
Avoid when: current reliability, compliance, or team maturity cannot support AI-assisted workflows

### product-oriented-architect

Name: The Product-Oriented Architect
Category: architect
Path: `.opencode/shared/profiles/architects/product-oriented-architect.md`
Fit: user outcomes, iteration speed, business adaptability, experimentation, roadmap uncertainty
Best at: preventing architecture from becoming detached from product reality
Avoid when: technical rigor, compliance, or operational resilience is the dominant near-term risk

### operational-sre-architect

Name: The Operational/SRE Architect
Category: architect
Path: `.opencode/shared/profiles/architects/operational-sre-architect.md`
Fit: production operations, observability, deployability, recoverability, MTTR
Best at: making systems survivable
Avoid when: the system is not production-bound or operational tooling would dominate actual delivery needs

## product-owners

### revenue-pmf-product-owner

Name: The Revenue/Product-Market-Fit Product Owner
Category: product-owner
Path: `.opencode/shared/profiles/product-owners/revenue-pmf-product-owner.md`
Fit: monetization, market traction, customer acquisition, competitive differentiation, growth loops
Best at: preventing technically impressive irrelevance
Avoid when: the decision is foundational, non-commercial, or primarily about technical risk reduction

### user-experience-product-owner

Name: The User Experience Product Owner
Category: product-owner
Path: `.opencode/shared/profiles/product-owners/user-experience-product-owner.md`
Fit: usability, friction reduction, onboarding, accessibility, emotional experience
Best at: preventing engineer-designed UX disasters
Avoid when: implementation feasibility, compliance, or delivery risk is the dominant constraint

### enterprise-governance-product-owner

Name: The Enterprise/Governance Product Owner
Category: product-owner
Path: `.opencode/shared/profiles/product-owners/enterprise-governance-product-owner.md`
Fit: compliance, procurement readiness, enterprise adoption, governance features, admin controls
Best at: identifying enterprise blockers early
Avoid when: the target market is small teams, consumers, or early exploration where governance would distort learning

### delivery-focused-product-owner

Name: The Delivery-Focused Product Owner
Category: product-owner
Path: `.opencode/shared/profiles/product-owners/delivery-focused-product-owner.md`
Fit: roadmap execution, milestone predictability, delivery risk reduction, dependency control, phase boundaries
Best at: preventing roadmap fantasy
Avoid when: aggressive product discovery or strategic differentiation matters more than near-term predictability

### data-analytics-product-owner

Name: The Data/Analytics Product Owner
Category: product-owner
Path: `.opencode/shared/profiles/product-owners/data-analytics-product-owner.md`
Fit: measurable outcomes, instrumentation, experimentation, KPIs, hypothesis validation
Best at: turning opinions into measurable hypotheses
Avoid when: metrics are unavailable, misleading, or slower than necessary qualitative learning

### platform-ecosystem-product-owner

Name: The Platform/Ecosystem Product Owner
Category: product-owner
Path: `.opencode/shared/profiles/product-owners/platform-ecosystem-product-owner.md`
Fit: extensibility, integrations, APIs, partner ecosystem, interoperability
Best at: long-term ecosystem strategy
Avoid when: core product demand is unproven or platform abstractions would precede real use cases

### ai-native-workflow-product-owner

Name: The AI-Native Workflow Product Owner
Category: product-owner
Path: `.opencode/shared/profiles/product-owners/ai-native-workflow-product-owner.md`
Fit: automation, AI-assisted workflows, reducing human operational burden, knowledge augmentation, semantic systems
Best at: future-facing workflow design
Avoid when: AI reliability, trust, evaluation, or fallback paths are not mature enough for the workflow

### customer-support-operations-product-owner

Name: The Customer Support/Operations Product Owner
Category: product-owner
Path: `.opencode/shared/profiles/product-owners/customer-support-operations-product-owner.md`
Fit: operational pain, support burden, onboarding/support tickets, recoverability, self-service
Best at: preventing support nightmares
Avoid when: support concerns would overfit edge cases or expose internals that users should not see

### financial-business-constraints-product-owner

Name: The Financial/Business Constraints Product Owner
Category: product-owner
Path: `.opencode/shared/profiles/product-owners/financial-business-constraints-product-owner.md`
Fit: ROI, burn rate, margins, implementation cost vs value, opportunity cost
Best at: killing expensive low-value ideas
Avoid when: the work is a strategic bet, platform foundation, or risk-reduction investment with indirect value
