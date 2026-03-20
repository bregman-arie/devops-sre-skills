---
id: diagnose-imagepullbackoff
name: Diagnose ImagePullBackOff
description: Determine why a pod cannot pull its container image and resolve safely.
tags: [kubernetes, triage, oncall, registry]
maturity: draft
inputs:
  namespace: string
  pod: string
outputs:
  - root_cause
  - safe_remediation_steps
tools_allowed:
  - k8s.get
  - k8s.describe
safety:
  default_mode: read_only
  forbidden: [k8s.delete, k8s.apply, k8s.patch]
  requires_confirmation_for: []
---

## When to use

Use when a pod is stuck in `ImagePullBackOff` or `ErrImagePull`.

## Preconditions

- You have read access to the namespace.
- You can identify the image reference from pod spec or describe output.

## Procedure

1. Confirm the failing image and container.
2. Read the event message for the exact pull error (404/401/timeout/TLS).
3. Validate the image name/tag/digest exists (out-of-band via registry).
4. Validate image pull secrets and service account configuration.
5. Validate network egress/DNS/TLS to the registry.

## Decision points

- `not found`: wrong tag/digest or repo path.
- `unauthorized`: missing/incorrect credentials or secret reference.
- `i/o timeout`: network path, proxy, firewall, or registry outage.
- `x509`: certificate chain/mitm/proxy issues.

## Verification

- New pods progress to `Running` without pull errors.
- Events stop showing pull failures.

## Rollback / undo

- Revert image reference to the last known-good tag/digest.
- Revert service account/secret references if changed.

## Escalation

- Registry team/vendor if the registry is down or auth is broken broadly.
- Platform/network team for cluster-wide DNS/egress/TLS issues.

## Examples

```bash
kubectl -n <ns> get pod <pod>
kubectl -n <ns> describe pod <pod>
```
