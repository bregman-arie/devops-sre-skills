---
id: triage-cost-spike
name: Triage Cloud Cost Spike
description: Identify the primary drivers of a sudden cloud cost increase and implement safe mitigations.
tags: [cost, finops, triage, oncall]
maturity: draft
inputs:
  cloud: string? # aws|gcp|azure
  account_or_project: string?
  time_window: string? # e.g. P7D
outputs:
  - top_cost_drivers
  - suspected_root_causes
  - mitigation_options
tools_allowed:
  - billing.read
  - metrics.query
safety:
  default_mode: read_only
  forbidden: [billing.write]
  requires_confirmation_for: [billing.write]
---

## When to use

Use when daily cost increases significantly versus baseline.

## Preconditions

- You can access billing/cost breakdown and recent change/deploy history.

## Procedure

1. Confirm the spike magnitude and when it started.
2. Break down by service, region, and top resources/tags.
3. Identify the change driver: deploy, scaling, traffic, misconfiguration, abuse.
4. Validate whether spend is expected (planned test) or unexpected.
5. Choose the safest mitigation: pause non-critical workloads, cap scaling, fix loops.

## Decision points

- Compute spike: check autoscaling, instance sizes, and runaway jobs.
- Network spike: check egress, NAT, CDN settings, cross-region traffic.
- Storage spike: check log retention, snapshots, object lifecycle policies.

## Verification

- Cost trend returns toward baseline within the next billing window.
- The change driver is addressed (scaling capped, job stopped, retention fixed).

## Rollback / undo

- Revert cost mitigation that impacts critical reliability.
- Restore paused workloads in a controlled manner.

## Escalation

- FinOps/cloud owners for billing anomalies or reserved commitment adjustments.
- Security team if spike may be caused by abuse/compromise.

## Examples

```text
Start with a service-by-service cost breakdown, then drill into the top 1-3 line items.
```
