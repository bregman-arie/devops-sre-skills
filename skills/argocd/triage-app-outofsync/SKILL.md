---
id: triage-app-outofsync
name: Triage Argo CD App OutOfSync
description: Identify why an Argo CD application is OutOfSync and resolve safely.
tags: [argocd, kubernetes, gitops, triage]
maturity: draft
inputs:
  app: string
  project: string?
outputs:
  - diff_summary
  - recommended_next_actions
tools_allowed:
  - argocd.get
  - argocd.diff
  - k8s.get
safety:
  default_mode: read_only
  forbidden: [argocd.sync, k8s.apply, k8s.delete]
  requires_confirmation_for: [argocd.sync]
---

## When to use

Use when Argo CD shows an application as `OutOfSync` and you need to understand the drift.

## Preconditions

- You can access Argo CD (CLI or UI) and the target cluster.

## Procedure

1. Confirm what resources are OutOfSync and whether the app is Healthy.
2. Determine whether drift is expected (manual hotfix) or unexpected (controller mutation).
3. Inspect diffs and identify the owning source (Helm/Kustomize/raw manifests).
4. If drift is expected, capture it and move the change back to Git.
5. If drift is unexpected, find the mutating actor (admission, controller, policy).

## Decision points

- Healthy + OutOfSync: often benign drift; decide whether to reconcile.
- Degraded + OutOfSync: treat as incident; fix health first.
- Frequent drift: consider ignoreDifferences / diffing settings.

## Verification

- App becomes `Synced` and remains stable across refreshes.
- Workload health is `Healthy` and key SLO signals stabilize.

## Rollback / undo

- Roll back Git changes or chart version to last known good.
- If reconciliation caused breakage, revert the change and resync.

## Escalation

- Platform team if mutation is due to cluster policy/admission.
- Service owner if the desired state in Git is incorrect.

## Examples

```bash
argocd app get <app>
argocd app diff <app>
```
