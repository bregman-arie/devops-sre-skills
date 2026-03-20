# Contributing

Thanks for contributing!

## What belongs here

- Skills that help DevOps/SRE workflows (triage, diagnosis, remediation, prevention)
- Skills that are safe-by-default and include verification + rollback/undo guidance

## Add a new skill

1. Pick a category folder under `skills/` (e.g., `kubernetes`, `terraform`, `argocd`, `incident`).
2. Create a new folder named after the skill id: `skills/<category>/<skill-id>/`.
3. Copy `skills/_template/SKILL.md` into the new folder and fill it out.
4. Keep examples parameterized (no account IDs, cluster names, hostnames, tokens).

## Conventions

- **Skill id**: kebab-case, unique across the repo (e.g., `diagnose-crashloop`)
- **Folder name**: must match `id`
- **One skill per folder**: `skills/<category>/<skill-id>/SKILL.md`
- **Safety**: default to `read_only`; list forbidden/mutating operations explicitly

## Validation

CI runs `scripts/validate_skills.py` to ensure:
- required front matter keys exist
- required headings exist
- ids are unique and match folder names
