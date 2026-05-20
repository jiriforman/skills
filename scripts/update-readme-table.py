#!/usr/bin/env python3
"""Regenerate the skills table in README.md from each skills/*/skill.yaml.

Replaces the content between these markers in README.md:

    <!-- skills-table:start -->
    ...auto-generated table...
    <!-- skills-table:end -->

Run locally with `python scripts/update-readme-table.py`; CI runs it on every
push to main.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
README = REPO_ROOT / "README.md"
START = "<!-- skills-table:start -->"
END = "<!-- skills-table:end -->"
REPO_SLUG = "jiriforman/skills"


def git_last_change(path: Path) -> tuple[str, str]:
    """Return (YYYY-MM-DD, author) for the most recent commit touching `path`."""
    result = subprocess.run(
        ["git", "log", "-1", "--format=%ai|%an", "--", str(path)],
        capture_output=True,
        text=True,
        check=False,
        cwd=REPO_ROOT,
    )
    out = result.stdout.strip()
    if not out:
        return "—", "—"
    date_str, _, author = out.partition("|")
    return date_str.split(" ")[0], author or "—"


def load_skills() -> list[dict]:
    skills = []
    if not SKILLS_DIR.exists():
        return skills
    for skill_yaml in sorted(SKILLS_DIR.glob("*/skill.yaml")):
        folder = skill_yaml.parent
        if folder.name.startswith("_"):
            continue
        with skill_yaml.open(encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        date, author = git_last_change(folder)
        skills.append(
            {
                "folder": folder.name,
                "name": data.get("name", folder.name),
                "display_name": data.get("display_name") or data.get("name", folder.name),
                "description": (data.get("description") or "").strip().replace("\n", " "),
                "version": str(data.get("version", "—")),
                "tags": data.get("tags", []) or [],
                "date": date,
                "author": author,
            }
        )
    return skills


def render_table(skills: list[dict]) -> str:
    if not skills:
        return (
            "_No skills published yet. Check back soon, or browse the catalog at "
            "[ailearning.jforman.cz/skills](https://ailearning.jforman.cz/skills)._"
        )
    header = "| Skill | Description | Tags | Version | Last update | Updated by | Download |"
    sep = "|---|---|---|---|---|---|---|"
    rows = [header, sep]
    for s in skills:
        download = (
            f"[.zip](https://github.com/{REPO_SLUG}/releases/latest/download/{s['name']}.zip)"
        )
        tags = ", ".join(f"`{t}`" for t in s["tags"]) if s["tags"] else "—"
        rows.append(
            f"| [{s['display_name']}](skills/{s['folder']}) "
            f"| {s['description']} "
            f"| {tags} "
            f"| `{s['version']}` "
            f"| {s['date']} "
            f"| {s['author']} "
            f"| {download} |"
        )
    return "\n".join(rows)


def main() -> int:
    if not README.exists():
        print("README.md not found", file=sys.stderr)
        return 1
    text = README.read_text(encoding="utf-8")
    if START not in text or END not in text:
        print(f"Markers {START!r} / {END!r} not found in README.md", file=sys.stderr)
        return 1

    skills = load_skills()
    table = render_table(skills)

    pre, _, rest = text.partition(START)
    _, _, post = rest.partition(END)
    new_text = f"{pre}{START}\n{table}\n{END}{post}"

    if new_text != text:
        README.write_text(new_text, encoding="utf-8")
        print(f"README updated with {len(skills)} skill(s).")
    else:
        print("README already up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
