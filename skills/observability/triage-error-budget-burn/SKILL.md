---
id: triage-error-budget-burn
name: Triage Error Budget Burn
description: Investigate rapid SLO burn and identify whether the driver is errors, latency, or availability.
tags: [observability, slo, triage, oncall]
maturity: draft
inputs:
  service: string
  slo: string?
  time_window: string? # e.g. PT6H
outputs:
  - burn_driver
  - top_contributors
  - mitigation_plan
tools_allowed:
  - metrics.query
  - logs.query
  - traces.query
safety:
  default_mode: read_only
  forbidden: []
  requires_confirmation_for: []
---

## When to use

Use when burn alerts fire or SLO dashboards show accelerated error budget consumption.

## Preconditions

- The SLO definition and signals are known (good/bad events or latency threshold).

## Procedure

1. Confirm the SLO signal and the burn window.
2. Identify whether burn is driven by errors, latency, or missing telemetry.
3. Break down by endpoint, region, customer segment, and dependency.
4. Correlate with deploys, config changes, and incidents.
5. Choose the fastest mitigation that reduces burn (rollback, disable, scale, failover).

## Decision points

- Telemetry missing: fix instrumentation/pipeline to avoid false burn.
- Dependency-induced burn: mitigate upstream (timeouts, circuit breaker, failover).
- Deploy-correlated burn: rollback or feature flag off.

## Verification

- Burn rate returns to normal and stays stable.
- Alert conditions clear.

## Rollback / undo

- Revert mitigations that cause new errors or correctness regressions.

## Escalation

- Escalate to dependency owners if they are the dominant contributor.
- Escalate to service owners for code fixes.

## Examples

```text
Start by decomposing the SLO into error vs latency vs availability contributions.
```
