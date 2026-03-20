---
id: example-skill-id
name: Example Skill Name
description: One-line description of when this skill is used.
tags: [example, template]
maturity: draft
inputs:
  example_required: string
  example_optional: string?
outputs:
  - expected_artifacts_or_decisions
tools_allowed:
  - shell.read
safety:
  default_mode: read_only
  forbidden:
    - shell.write
  requires_confirmation_for: []
---

## When to use

## Preconditions

## Procedure

## Decision points

## Verification

## Rollback / undo

## Escalation

## Examples
