import os
import re
import sys
from typing import Dict, List, Tuple

import yaml


REQUIRED_HEADINGS = [
    "## When to use",
    "## Preconditions",
    "## Procedure",
    "## Decision points",
    "## Verification",
    "## Rollback / undo",
    "## Escalation",
    "## Examples",
]


def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def split_front_matter(text: str) -> Tuple[Dict, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing front matter start marker '---' on first line")
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
    if end_idx is None:
        raise ValueError("missing front matter end marker '---'")
    fm_text = "\n".join(lines[1:end_idx])
    body = "\n".join(lines[end_idx + 1 :])
    fm = yaml.safe_load(fm_text) or {}
    if not isinstance(fm, dict):
        raise ValueError("front matter must be a YAML mapping")
    return fm, body


def find_skill_files(skills_root: str) -> List[str]:
    out: List[str] = []
    for root, dirs, files in os.walk(skills_root):
        dirs[:] = [d for d in dirs if d not in [".git", "__pycache__"]]
        if "SKILL.md" in files:
            out.append(os.path.join(root, "SKILL.md"))
    out.sort()
    return out


def validate_headings(body: str) -> List[str]:
    errors: List[str] = []
    for h in REQUIRED_HEADINGS:
        if h not in body:
            errors.append(f"missing heading: {h}")
    return errors


def validate_front_matter(fm: Dict) -> List[str]:
    errors: List[str] = []
    required_keys = [
        "id",
        "name",
        "description",
        "tags",
        "maturity",
        "inputs",
        "outputs",
        "tools_allowed",
        "safety",
    ]
    for k in required_keys:
        if k not in fm:
            errors.append(f"missing key: {k}")
    if "id" in fm:
        if not isinstance(fm["id"], str):
            errors.append("id must be a string")
        elif not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", fm["id"]):
            errors.append("id must be kebab-case (lowercase letters/numbers/hyphens)")
    if "tags" in fm and not (
        isinstance(fm["tags"], list) and all(isinstance(x, str) for x in fm["tags"])
    ):
        errors.append("tags must be a list of strings")
    if "maturity" in fm and fm.get("maturity") not in ["draft", "stable", "deprecated"]:
        errors.append("maturity must be one of: draft, stable, deprecated")
    if "inputs" in fm and not isinstance(fm.get("inputs"), dict):
        errors.append("inputs must be a mapping")
    if "outputs" in fm and not (
        isinstance(fm.get("outputs"), list)
        and all(isinstance(x, str) for x in fm["outputs"])
    ):
        errors.append("outputs must be a list of strings")
    if "tools_allowed" in fm and not (
        isinstance(fm.get("tools_allowed"), list)
        and all(isinstance(x, str) for x in fm["tools_allowed"])
    ):
        errors.append("tools_allowed must be a list of strings")
    safety = fm.get("safety")
    if "safety" in fm:
        if not isinstance(safety, dict):
            errors.append("safety must be a mapping")
        else:
            dm = safety.get("default_mode")
            if dm not in ["read_only", "mutating"]:
                errors.append("safety.default_mode must be read_only or mutating")
            forbidden = safety.get("forbidden")
            if not (
                isinstance(forbidden, list)
                and all(isinstance(x, str) for x in forbidden)
            ):
                errors.append("safety.forbidden must be a list of strings")
            else:
                allowed = fm.get("tools_allowed")
                if isinstance(allowed, list):
                    overlap = sorted(set(allowed).intersection(set(forbidden)))
                    if overlap:
                        errors.append(
                            f"tools_allowed overlaps safety.forbidden: {', '.join(overlap)}"
                        )
    return errors


def validate_path(path: str, skills_root: str) -> Tuple[str, str, List[str]]:
    errors: List[str] = []
    rel = os.path.relpath(path, skills_root)
    parts = rel.split(os.sep)
    if parts[0] == "_template":
        return "_template", "_template", []
    if len(parts) != 3 or parts[-1] != "SKILL.md":
        errors.append("skill file must be at skills/<category>/<skill-id>/SKILL.md")
        category = parts[0] if parts else ""
        skill_id = parts[1] if len(parts) > 1 else ""
        return category, skill_id, errors
    category, skill_id, _ = parts
    if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", category):
        errors.append("category folder must be kebab-case")
    if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", skill_id):
        errors.append("skill folder must be kebab-case")
    return category, skill_id, errors


def main() -> int:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    skills_root = os.path.join(repo_root, "skills")
    if not os.path.isdir(skills_root):
        print("ERROR: missing skills/ directory")
        return 2

    files = find_skill_files(skills_root)
    errors: List[str] = []
    ids: Dict[str, str] = {}

    for skill_path in files:
        category, folder_id, path_errors = validate_path(skill_path, skills_root)
        if category == "_template":
            continue
        for e in path_errors:
            errors.append(f"{skill_path}: {e}")
            continue

        try:
            text = read_text(skill_path)
            fm, body = split_front_matter(text)
        except Exception as e:
            errors.append(f"{skill_path}: {e}")
            continue

        for e in validate_front_matter(fm):
            errors.append(f"{skill_path}: {e}")

        skill_id = fm.get("id")
        if isinstance(skill_id, str):
            if skill_id != folder_id:
                errors.append(
                    f"{skill_path}: front matter id '{skill_id}' must match folder '{folder_id}'"
                )
            prev = ids.get(skill_id)
            if prev and prev != skill_path:
                errors.append(f"{skill_path}: duplicate id '{skill_id}' also in {prev}")
            ids[skill_id] = skill_path

        for e in validate_headings(body):
            errors.append(f"{skill_path}: {e}")

    if errors:
        print("Validation failed:\n")
        for e in errors:
            print(f"- {e}")
        return 1

    print(f"OK: validated {len(files) - 1} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
