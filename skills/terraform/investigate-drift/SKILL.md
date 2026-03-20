---
id: investigate-drift
name: Investigate Terraform Drift
description: Determine why actual infrastructure differs from Terraform state and choose a safe reconciliation path.
tags: [terraform, drift, triage, oncall]
maturity: draft
inputs:
  workspace: string
  time_window: string? # e.g. P7D
outputs:
  - drift_summary
  - suspected_mutators
  - reconciliation_plan
tools_allowed:
  - terraform.plan
  - terraform.read
  - vcs.read
safety:
  default_mode: read_only
  forbidden: [terraform.apply, terraform.import, terraform.state_write]
  requires_confirmation_for: [terraform.import, terraform.apply]
---

## When to use

Use when a plan shows unexpected changes or monitoring indicates config drift.

## Preconditions

- You can run `terraform plan` against the workspace/backend.
- You can inspect change history (VCS and/or cloud audit logs).

## Procedure

1. Run a plan and classify changes: safe/no-op, risky replacement, access-related.
2. Identify when drift started (compare to deploys and change logs).
3. Determine the mutator: manual console change, controller, autoscaling, policy.
4. Decide the source of truth: Terraform config vs external system.
5. Choose reconciliation: update config, import, ignore changes, or revert manual change.

## Decision points

- Replacement of critical resources: stop and coordinate; avoid apply during incidents.
- Autoscaled fields: consider lifecycle ignore for managed attributes.
- Manual hotfix required: capture it in code and remove out-of-band changes.

## Verification

- A new plan is stable (no unexpected diffs).
- Audit logs align with expected change process.

## Rollback / undo

- Revert config commits that introduced unintended drift.
- Restore from snapshots/backups if drift caused breakage.

## Escalation

- IaC owners for state manipulation or imports.
- Security team if drift indicates unauthorized access.

## Examples

```bash
terraform plan
```
