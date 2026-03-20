---
id: triage-service-dns
name: Triage Kubernetes Service DNS
description: Diagnose in-cluster DNS resolution failures and isolate root causes.
tags: [kubernetes, dns, networking, triage]
maturity: draft
inputs:
  namespace: string
  source_pod: string?
  query_name: string?
outputs:
  - failure_domain
  - suspected_root_cause
  - verification_steps
tools_allowed:
  - k8s.get
  - k8s.describe
  - k8s.exec
  - k8s.logs
safety:
  default_mode: read_only
  forbidden: [k8s.apply, k8s.patch, k8s.delete]
  requires_confirmation_for: []
---

## When to use

Use when pods cannot resolve service names (e.g., `*.svc.cluster.local`) or external DNS intermittently fails.

## Preconditions

- You can run commands in a diagnostic pod or an affected pod.
- You can access CoreDNS/kube-dns logs.

## Procedure

1. Confirm whether the issue is cluster-wide or namespace/workload-specific.
2. Validate resolver configuration inside the pod (`/etc/resolv.conf`) and search domains.
3. Query the same name from multiple pods/nodes to identify locality.
4. Check CoreDNS health, restarts, and error logs.
5. Check network policies and CNI health that might block DNS to the DNS service.

## Decision points

- Only one namespace affected: network policy or custom DNS config.
- Only one node affected: node-level networking issues.
- CoreDNS errors/timeouts: capacity, upstream recursion, or misconfiguration.
- NXDOMAIN for a service: confirm the service/endpoints exist.

## Verification

- Repeated DNS queries succeed from multiple pods.
- CoreDNS error logs stop increasing.

## Rollback / undo

- Revert CoreDNS config changes.
- Revert network policy changes if they widen access unexpectedly.

## Escalation

- Platform/network team for CNI or node-level packet loss.
- Service owner if the service/endpoints are missing due to deploy issues.

## Examples

```bash
kubectl -n <ns> exec <pod> -- cat /etc/resolv.conf
kubectl -n <ns> exec <pod> -- nslookup <service>.<ns>.svc.cluster.local
kubectl -n kube-system logs -l k8s-app=kube-dns --tail=200
```
