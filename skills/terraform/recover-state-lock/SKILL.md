---
id: recover-state-lock
name: Recover Terraform State Lock
description: Safely assess and recover from a stuck Terraform state lock.
tags: [terraform, oncall, triage]
maturity: draft
inputs:
  workspace: string
  backend: string? # e.g. s3, gcs, tfe
outputs:
  - lock_owner
  - safe_unlock_decision
  - verification_steps
tools_allowed:
  - terraform.read
  - terraform.plan
safety:
  default_mode: read_only
  forbidden: [terraform.apply, terraform.force_unlock]
  requires_confirmation_for: [terraform.force_unlock]
---

## When to use

Use when Terraform reports the state is locked and operations cannot proceed.

## Preconditions

- You have access to the workspace and can identify the last run/operator.
- You understand the blast radius of forcing an unlock.

## Procedure

1. Determine whether a Terraform operation is currently running (CI runner, TFC/TFE run, local terminal).
2. Identify lock metadata (who/when/operation).
3. If a run is active, wait or stop it cleanly.
4. If the lock is stale, coordinate and force-unlock only after confirming no active writers.
5. Run a plan to confirm state consistency.

## Decision points

- Active run present: do not force-unlock.
- Stale lock (no active run, old timestamp): force-unlock may be appropriate.
- Repeated lock issues: investigate backend connectivity and CI cancellation behavior.

## Verification

- A new `terraform plan` completes successfully.
- No concurrent runs are writing to state.

## Rollback / undo

- If state becomes inconsistent, restore from backend versioning/snapshots.
- If a partial apply occurred, reconcile with a fresh plan and targeted remediation.

## Escalation

- Escalate to platform/IaC owners if unlock requires backend admin privileges.
- Escalate if state corruption is suspected.

## Examples

```bash
terraform plan
```
