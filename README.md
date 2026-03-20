# devops-sre-skills

Agent-ready `SKILL.md` library for DevOps and SRE work.

This repo is designed to be:
- Good runbooks for humans
- A predictable, machine-readable contract for agents (Claude skills, OpenCode-like agents)

## Principles

- Safe by default: skills should be read-only unless explicitly labeled otherwise
- No secrets, no environment-specific identifiers in examples
- Procedures include verification and rollback/undo guidance

## Repo layout

- `skills/<category>/<skill-id>/SKILL.md` - the skill file (one per skill)
- `skills/_template/SKILL.md` - copyable template
- `schema/` - the front matter schema and conventions
- `scripts/` - validators and tooling

Categories are intentionally shallow (e.g., `kubernetes`, `aws`, `terraform`, `argocd`, `incident`). Prefer tags over deep folder trees.

## Skill format

Each `SKILL.md` starts with YAML front matter (between `---` lines) followed by Markdown sections.

See `skills/_template/SKILL.md` for the canonical structure.

## Using with agents

- Claude skills: load a skill file as an instruction bundle; use the front matter as the contract (inputs/tools/safety)
- OpenCode-like agents: enforce `tools_allowed`/`safety` gates from the front matter; present the Markdown procedure during execution

## Contributing

See `CONTRIBUTING.md`.
