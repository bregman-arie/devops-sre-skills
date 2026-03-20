---
id: triage-node-pressure
name: Triage Kubernetes Node Pressure
description: Diagnose node-level memory/disk/pid pressure and determine safe mitigations.
tags: [kubernetes, triage, oncall, nodes]
maturity: draft
inputs:
  node: string?
  namespace: string?
  time_window: string? # e.g. PT30M
outputs:
  - pressure_type
  - suspected_causes
  - safe_mitigations
tools_allowed:
  - k8s.get
  - k8s.describe
  - k8s.logs
safety:
  default_mode: read_only
  forbidden: [k8s.delete, k8s.apply, k8s.patch, k8s.drain]
  requires_confirmation_for: [k8s.drain]
---

## When to use

Use when nodes show `MemoryPressure`, `DiskPressure`, or pods are evicted due to node conditions.

## Preconditions

- You have read access to node and pod data.
- You can identify the affected node(s) or the evicted pods.

## Procedure

1. Confirm the node condition and the time it started.
2. Identify impacted workloads (evictions, pending pods, restarts).
3. Determine whether the issue is a single node or widespread.
4. Identify top contributors (largest pods, runaway logs, tmpfs, imagefs).
5. Choose the lowest-risk mitigation that restores capacity.

## Decision points

- Single node only: consider cordon/drain after identifying a safe target.
- Many nodes: treat as capacity or systemic issue (autoscaling, noisy neighbor policy).
- Disk pressure: check image garbage, log growth, emptyDir usage.
- Memory pressure: check memory limits, leaks, and node size.

## Verification

- Node condition clears and stays stable.
- Evictions stop and pending pods schedule.
- Workload SLO signals return to baseline.

## Rollback / undo

- If you drained a node and it increases impact, stop draining and rebalance workloads.
- If you changed resource requests/limits, revert to previous values.

## Escalation

- Platform team for cluster-wide pressure or autoscaler issues.
- Service owners for runaway resource usage.

## Examples

```bash
kubectl describe node <node>
kubectl get pods -A -o wide | grep <node>
kubectl get events -A --sort-by=.lastTimestamp | tail -n 50
```
