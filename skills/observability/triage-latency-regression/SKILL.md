---
id: triage-latency-regression
name: Triage Latency Regression
description: Identify what changed and where latency increased, using logs/metrics/traces.
tags: [observability, performance, triage, oncall]
maturity: draft
inputs:
  service: string
  environment: string?
  time_window: string? # e.g. PT1H
outputs:
  - suspected_contributors
  - proposed_tests
  - mitigation_options
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

Use when p95/p99 latency increases and you need a fast root-cause hypothesis.

## Preconditions

- You have access to metrics, logs, and (ideally) traces.

## Procedure

1. Confirm scope: which endpoints/operations, which regions, which customers.
2. Compare before/after: deployment markers, config changes, dependency status.
3. Decompose: queueing vs compute vs dependency latency.
4. Validate saturation: CPU, memory, GC, thread pools, connection pools.
5. Correlate errors/timeouts with latency.

## Decision points

- Strong correlation with a deploy: consider rollback.
- Dependency latency increase: mitigate with timeouts, caching, failover.
- Saturation increase: scale, shed load, or reduce work.

## Verification

- Latency returns to baseline and stays stable across multiple windows.
- Error rate does not regress.

## Rollback / undo

- Roll back the most recent change correlated with the regression.
- Revert performance tuning if it degrades correctness.

## Escalation

- Escalate to dependency owners if external system is the bottleneck.
- Escalate to service owners if code changes are required.

## Examples

Example queries to adapt:

```text
Compare p95 latency now vs 1h ago; split by route, status code, and upstream.
```
