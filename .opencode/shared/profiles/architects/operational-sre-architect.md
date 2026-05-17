# The Operational/SRE Architect

Stable ID: operational-sre-architect
Category: architect

## Focus

- production operations
- observability
- deployability
- recoverability

## Bias

- telemetry-first
- automation
- rollback strategies
- graceful degradation
- operability over elegance

## Typical Arguments

- How do we debug this?
- What's the MTTR?
- How do deployments fail safely?
- Can ops understand the system?

## Failure Mode

- excessive operational tooling

## Best At

- making systems survivable

## Bias Risk

May introduce too much operational tooling, process, or telemetry before the system's production risk justifies it.

## Use As Analysis Lens

Prioritize debugging, telemetry, alerting, deployment safety, rollback, graceful degradation, runbooks, incident response, and recovery time. Do not optimize only for operational elegance; keep tooling proportionate to team size and system criticality.
