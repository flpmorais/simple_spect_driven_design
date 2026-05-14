---
docType: business-index
verifiedAt: "{{date}}"
lastUpdatedBy: bmad-business-docs
---

# Business Documentation

This folder contains business/domain documentation organized by business domain.

## Domain Map

{{domain_map}}

## Shared Documents

- [Glossary](./glossary.md)
- [Actors](./actors.md)
- [Cross-Domain Policies](./cross-domain/policies.md)
- [Cross-Domain Invariants](./cross-domain/invariants.md)
- [Discrepancies](./cross-domain/discrepancies.md)

## Maintenance Rules

- Business rules must have a source or be marked `proposed`.
- Code behavior is implementation evidence, not automatic business approval.
- Contradictions between approved rules and observed implementation must be recorded as discrepancies.
- Split documentation by business domain, not technical component.
