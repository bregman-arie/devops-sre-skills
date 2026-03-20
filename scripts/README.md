# Scripts

## validate_skills.py

Validates that each `skills/<category>/<skill-id>/SKILL.md` file:
- has valid YAML front matter
- includes required keys
- includes required Markdown headings
- uses a unique `id` that matches its folder name

Run locally:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r scripts/requirements.txt
python scripts/validate_skills.py
```
