---
id: triage-suspected-secret-exposure
name: Triage Suspected Secret Exposure
description: Contain and respond to a suspected credential/secret exposure without increasing blast radius.
tags: [security, incident, secrets, triage]
maturity: draft
inputs:
  secret_type: string # e.g. api_key, oauth_token, ssh_key
  exposure_location: string # e.g. git, logs, support ticket
  first_seen_time: string?
outputs:
  - containment_actions
  - rotation_plan
  - verification_steps
tools_allowed:
  - vcs.read
  - logs.query
  - secrets.read
safety:
  default_mode: read_only
  forbidden: [secrets.write, vcs.rewrite_history]
  requires_confirmation_for: [secrets.write, vcs.rewrite_history]
---

## When to use

Use when a secret may have been exposed (committed to VCS, printed in logs, pasted to a ticket).

## Preconditions

- You have a security contact path and access to rotate the secret.

## Procedure

1. Treat as real until proven otherwise; minimize sharing of the secret.
2. Identify what secret it is, where it was exposed, and potential access scope.
3. Contain: revoke/disable the credential if supported.
4. Rotate: issue a new secret, deploy it, then remove the old one.
5. Remove exposure sources (redact logs, remove from docs, invalidate caches).
6. Audit usage for suspicious activity.

## Decision points

- Public exposure (public repo, public paste): rotate immediately.
- High-privilege secret: prioritize containment and audit.
- Cannot rotate quickly: restrict permissions and add compensating controls.

## Verification

- Old credential is invalid and cannot authenticate.
- New credential works in production.
- No further leak sources remain.

## Rollback / undo

- If rotation breaks service, restore from a secure rollback mechanism while keeping the old credential revoked if possible.

## Escalation

- Escalate to security team for incident handling and external notifications.
- Escalate to compliance/legal if required.

## Examples

```text
Do not paste the secret into issues, PRs, or chat logs.
```
