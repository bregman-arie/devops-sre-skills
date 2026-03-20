---
id: triage-pending-pods
name: Triage Pending Pods
description: Diagnose pods stuck in Pending and identify scheduling constraints.
tags: [kubernetes, triage, scheduling, oncall]
maturity: draft
inputs:
  namespace: string
  pod: string?
  label_selector: string?
outputs:
  - scheduling_blocker
  - recommended_fixes
tools_allowed:
  - k8s.get
  - k8s.describe
safety:
  default_mode: read_only
  forbidden: [k8s.delete, k8s.apply, k8s.patch]
  requires_confirmation_for: []
---

## When to use

Use when pods remain in `Pending` longer than expected.

## Preconditions

- You can access pod events and node capacity information.

## Procedure

1. Identify which pods are pending and for how long.
2. Inspect pod scheduling events to find the exact constraint.
3. Classify the blocker: insufficient resources, taints/tolerations, affinity, PV binding, quotas, or image pull.
4. Confirm whether the blocker is local (one namespace/workload) or global (cluster capacity).
5. Choose the lowest-risk remediation.

## Decision points

- `Insufficient cpu/memory`: scale cluster, reduce requests, or shed load.
- `taint {node.kubernetes.io/...}`: add toleration only if correct.
- `pod affinity/anti-affinity`: loosen rules if they are too strict.
- `unbound immediate PersistentVolumeClaims`: investigate storage class/provisioner.
- `exceeded quota`: adjust quota or reduce consumption.

## Verification

- Pods transition from `Pending` to `Running`.
- Scheduling events stop reporting the constraint.

## Rollback / undo

- Revert scheduling policy changes (affinity/tolerations) if they increase blast radius.
- Revert quota changes if they cause noisy neighbor impact.

## Escalation

- Platform team for cluster capacity or storage provisioner issues.
- Service owner for incorrect requests/affinity rules.

## Examples

```bash
kubectl -n <ns> get pod <pod>
kubectl -n <ns> describe pod <pod>
kubectl get nodes
```
