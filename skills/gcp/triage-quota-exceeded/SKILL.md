---
id: triage-quota-exceeded
name: Triage GCP Quota Exceeded
description: Diagnose GCP quota errors and identify the quota, scope, and fastest safe mitigation.
tags: [gcp, quota, triage, oncall]
maturity: draft
inputs:
  service: string
  error_message: string
  region: string?
outputs:
  - quota_name
  - quota_scope
  - mitigation_options
tools_allowed:
  - gcp.logging_read
  - gcp.quotas_read
safety:
  default_mode: read_only
  forbidden: [gcp.quotas_write]
  requires_confirmation_for: [gcp.quotas_write]
---

## When to use

Use when services fail with `quota exceeded`, `RESOURCE_EXHAUSTED`, or similar quota limit errors.

## Preconditions

- You can access the project and identify the failing service and region.

## Procedure

1. Extract the quota name/metric from the error message.
2. Determine the scope: project, region, zone, or per-user.
3. Confirm whether this is a spike (traffic/deploy) or a steady-state growth.
4. Identify the top consumers (which resources or calls drive the quota).
5. Choose mitigation: reduce usage, shift traffic, or request quota increase.

## Decision points

- Spike caused by deploy/loop: rollback or hotfix to reduce calls.
- Legit growth: request quota increase and add alerting before hitting limits.
- Regional quota: spread across regions or rebalance.

## Verification

- Error rate drops and quota errors stop.
- Resource creation/API calls succeed.

## Rollback / undo

- Revert changes that increased consumption (deploy/config).
- If throttling is introduced, remove it after quota is safe.

## Escalation

- Escalate to service owners if usage is driven by application behavior.
- Escalate to cloud owners for quota increase approvals.

## Examples

```text
Look for the quota metric name in the error, then map it to the service and region.
```
