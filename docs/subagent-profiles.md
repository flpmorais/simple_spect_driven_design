# SSD Subagent Profiles

This document lists reusable SSD analysis profiles for subagent-driven profile analysis. Profiles are shared Markdown files selected by calling skills and executed by `ssd_profile_analyzer`.

## Purpose

Subagent profiles provide opinionated analysis lenses for reusable review workflows. Profiles are not personas; they define evaluation weights, default concerns, likely blind spots, and practical judgment patterns.

## Source

Profile catalog:

```text
.opencode/shared/profiles/catalog.md
```

Profile files:

```text
.opencode/shared/profiles/
```

## Current Profiles

| Profile | Category | Fit | Best At | Source |
| --- | --- | --- | --- | --- |
| The Conservative Enterprise Architect | architect | stability, operational maturity, vendor support, auditability, boring tech | avoiding catastrophic platform mistakes | `.opencode/shared/profiles/architects/conservative-enterprise-architect.md` |
| The Pragmatic Delivery Architect | architect | shipping, developer productivity, reducing accidental complexity, team capability | grounding architecture discussions in delivery reality | `.opencode/shared/profiles/architects/pragmatic-delivery-architect.md` |
| The Scalability/Distributed Systems Architect | architect | scale, resilience, throughput, distributed correctness, blast radius analysis | identifying future bottlenecks early | `.opencode/shared/profiles/architects/scalability-distributed-systems-architect.md` |
| The Security & Compliance Architect | architect | threat models, identity, audit, legal exposure, regulatory exposure | preventing invisible existential risks | `.opencode/shared/profiles/architects/security-compliance-architect.md` |
| The Cost Efficiency Architect | architect | infrastructure spend, operational efficiency, total cost of ownership, cloud bill exposure | exposing hidden operational cost | `.opencode/shared/profiles/architects/cost-efficiency-architect.md` |
| The AI/Automation-Native Architect | architect | AI-assisted development, agentic systems, automation leverage, semantic workflows | future-proofing for AI-native operations | `.opencode/shared/profiles/architects/ai-automation-native-architect.md` |
| The Product-Oriented Architect | architect | user outcomes, iteration speed, business adaptability, experimentation, roadmap uncertainty | preventing architecture from becoming detached from product reality | `.opencode/shared/profiles/architects/product-oriented-architect.md` |
| The Operational/SRE Architect | architect | production operations, observability, deployability, recoverability, MTTR | making systems survivable | `.opencode/shared/profiles/architects/operational-sre-architect.md` |
| The Revenue/Product-Market-Fit Product Owner | product-owner | monetization, market traction, customer acquisition, competitive differentiation, growth loops | preventing technically impressive irrelevance | `.opencode/shared/profiles/product-owners/revenue-pmf-product-owner.md` |
| The User Experience Product Owner | product-owner | usability, friction reduction, onboarding, accessibility, emotional experience | preventing engineer-designed UX disasters | `.opencode/shared/profiles/product-owners/user-experience-product-owner.md` |
| The Enterprise/Governance Product Owner | product-owner | compliance, procurement readiness, enterprise adoption, governance features, admin controls | identifying enterprise blockers early | `.opencode/shared/profiles/product-owners/enterprise-governance-product-owner.md` |
| The Delivery-Focused Product Owner | product-owner | roadmap execution, milestone predictability, delivery risk reduction, dependency control, phase boundaries | preventing roadmap fantasy | `.opencode/shared/profiles/product-owners/delivery-focused-product-owner.md` |
| The Data/Analytics Product Owner | product-owner | measurable outcomes, instrumentation, experimentation, KPIs, hypothesis validation | turning opinions into measurable hypotheses | `.opencode/shared/profiles/product-owners/data-analytics-product-owner.md` |
| The Platform/Ecosystem Product Owner | product-owner | extensibility, integrations, APIs, partner ecosystem, interoperability | long-term ecosystem strategy | `.opencode/shared/profiles/product-owners/platform-ecosystem-product-owner.md` |
| The AI-Native Workflow Product Owner | product-owner | automation, AI-assisted workflows, reducing human operational burden, knowledge augmentation, semantic systems | future-facing workflow design | `.opencode/shared/profiles/product-owners/ai-native-workflow-product-owner.md` |
| The Customer Support/Operations Product Owner | product-owner | operational pain, support burden, onboarding/support tickets, recoverability, self-service | preventing support nightmares | `.opencode/shared/profiles/product-owners/customer-support-operations-product-owner.md` |
| The Financial/Business Constraints Product Owner | product-owner | ROI, burn rate, margins, implementation cost vs value, opportunity cost | killing expensive low-value ideas | `.opencode/shared/profiles/product-owners/financial-business-constraints-product-owner.md` |

## Rules

- Calling skills select profiles from `.opencode/shared/profiles/catalog.md`.
- `ssd_profile_analyzer` resolves profiles by exact stable ID.
- Profiles are analysis lenses, not roleplay personas.
- Profile files are Markdown source material, not runtime memory.

## Outcome Guidance

Machine-optimized rules for profile-backed analysis:

| Rule | Requirement |
| --- | --- |
| lens_not_persona | Use profile as evaluation weights; do not roleplay, claim identity, or claim experience. |
| bias_applied_required | Always state how profile focus/bias shaped the analysis. |
| bias_risk_required | Always state how profile bias may distort the conclusion. |
| counterarguments_required | Always include conditions, facts, or alternate lenses that weaken the profile view. |
| evidence_vs_interpretation | Separate supplied facts from profile-weighted judgment. |
| missing_facts_required | If input is thin, return provisional opinion plus missing facts. |
| crisp_judgment | Prefer direct opinion over generic balance; expose uncertainty through confidence. |
| constraints_respected | Do not override caller constraints silently; explain tradeoffs. |
| structured_profiles | Keep profile sections stable: Focus, Bias, Typical Arguments, Failure Mode, Best At, Bias Risk, Use As Analysis Lens. |
| caller_selects_profile | Calling skill selects profile in v1; add selector only if selection logic repeats. |
| panel_later | Add multi-profile panel mode only after real workflows need cross-profile tension. |
| validation_later | Add schema validation only if catalog/profile drift becomes a real problem. |
| catalog_selection_only | Catalog supports selection; detailed analysis rules live in profile files. |
