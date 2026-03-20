---
id: sev1-first-15-minutes
name: Sev1 First 15 Minutes
description: Execute the initial incident workflow to stabilize, communicate, and delegate.
tags: [incident, oncall, sev1, communications]
maturity: draft
inputs:
  service: string
  symptoms: string
  start_time: string?
outputs:
  - incident_roles_assigned
  - initial_status_update
  - stabilization_plan
tools_allowed:
  - incident.comms
  - observability.read
safety:
  default_mode: read_only
  forbidden: []
  requires_confirmation_for: []
---

## When to use

Use for a confirmed high-severity production incident.

## Preconditions

- You have an incident channel and a path to page additional responders.

## Procedure

1. Declare severity and open an incident channel.
2. Assign roles: incident commander, comms lead, operations lead.
3. State the customer impact in one sentence.
4. Stabilize first: stop the bleeding (rollback, disable feature, shed load).
5. Start a timeline and capture key actions/decisions.

## Decision points

- If impact is unknown: prioritize measurement and narrowing scope.
- If rollback is low-risk and likely effective: rollback early.
- If data integrity is at risk: freeze writes and escalate.

## Verification

- Leading indicators improve (error rate, latency, saturation).
- Customer reports decrease.
- Comms cadence is established.

## Rollback / undo

- If mitigation worsens impact, revert and try the next lowest-risk action.

## Escalation

- Escalate to security if incident involves auth, data exposure, or suspicious activity.
- Escalate to leadership if SLA/SLO breach is likely.

## Examples

Initial update template:

```text
Impact: <who/what is affected>
Start: <time>
Current status: <what we see>
Mitigation in progress: <what we are doing>
Next update: <time>
```
