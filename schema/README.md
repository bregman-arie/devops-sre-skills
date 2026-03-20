# Schema

Skills use YAML front matter at the top of `SKILL.md`.

- Schema file: `schema/skill-frontmatter.schema.json`
- The schema covers the front matter only; the Markdown body is validated by conventions.

## Required headings

The Markdown body should include the following headings (exact text):

- `## When to use`
- `## Preconditions`
- `## Procedure`
- `## Decision points`
- `## Verification`
- `## Rollback / undo`
- `## Escalation`
- `## Examples`

## Tool naming

`tools_allowed` is an allow-list of *capabilities* (strings) that the agent/runtime maps to concrete tools.

Suggested prefixes:

- `k8s.*` (e.g., `k8s.get`, `k8s.describe`, `k8s.logs`, `k8s.exec`, `k8s.apply`, `k8s.delete`)
- `terraform.*` (e.g., `terraform.plan`, `terraform.apply`)
- `aws.*`, `gcp.*`, `argocd.*`
- `shell.read`, `shell.write` (as a fallback)

Default to `read_only`.
