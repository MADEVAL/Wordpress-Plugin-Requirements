#!/usr/bin/env python3
"""Structural validator for wordpress-plugin-requirements.

Stdlib only. Run from the repository root or from any directory:

    python tests/validate_skill.py
    python tests/validate_skill.py --root tests/fixtures/bad-skill

Exits 1 if any hard check fails.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

DEFAULT_ROOT = Path(__file__).resolve().parent.parent
SKILL_NAME = "wordpress-plugin-requirements"
REQUIRED_SECTIONS = [
    "When Not to Use",
    "Modes",
    "Workflow",
    "Findings",
    "Output Contract",
    "Hard Stops",
    "Constraints",
    "Reference Files",
    "Disclosure",
]
REQUIRED_ROOT_FILES = [
    "LICENSE",
    "install.py",
    "README.md",
    "README.ru.md",
    "CHANGELOG.md",
    ".gitattributes",
    ".editorconfig",
    ".markdownlint.json",
    ".github/workflows/ci.yml",
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".cursor-plugin/plugin.json",
    "skills/{}/agents/openai.yaml".format(SKILL_NAME),
    "evals/cases.md",
    "tests/validate_skill.py",
]
TEXT_SUFFIXES = {
    ".md",
    ".py",
    ".json",
    ".yaml",
    ".yml",
    ".txt",
}
SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".venv", "venv", "node_modules"}

errors: list[str] = []
root: Path
skill_dir: Path


def fail(message: str) -> None:
    errors.append(message)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        fail(f"{path.relative_to(root)} is not valid UTF-8")
        return ""
    except FileNotFoundError:
        fail(f"missing file: {path.relative_to(root)}")
        return ""


def parse_frontmatter(text: str) -> tuple[dict[str, str], dict[str, str]]:
    match = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not match:
        return {}, {}
    raw = match.group(1)
    top: dict[str, str] = {}
    meta: dict[str, str] = {}
    in_metadata = False
    for line in raw.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if line.startswith("  ") and in_metadata:
            key, _, value = line.strip().partition(":")
            meta[key.strip()] = value.strip().strip('"').strip("'")
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key == "metadata":
            in_metadata = True
            continue
        in_metadata = False
        top[key] = value
    return top, meta


def semver(value: str) -> bool:
    return bool(re.fullmatch(r"\d+\.\d+\.\d+", value))


def check_encoding(path: Path) -> None:
    data = path.read_bytes()
    rel = path.relative_to(root)
    if data.startswith(b"\xef\xbb\xbf"):
        fail(f"{rel}: UTF-8 BOM is not allowed")
    if b"\r\n" in data:
        fail(f"{rel}: CRLF found, use LF")
    if data and not data.endswith(b"\n"):
        fail(f"{rel}: missing final newline")


def check_dashes(path: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    if "\u2014" in text:
        fail(f"{path.relative_to(root)}: em dash found")
    if "\u2013" in text:
        fail(f"{path.relative_to(root)}: en dash found")


def iter_project_text_files() -> list[Path]:
    paths: list[Path] = []
    bases = [
        skill_dir,
        root / "tests",
        root / "evals",
        root / ".claude-plugin",
        root / ".cursor-plugin",
        root / ".github",
    ]
    for base in bases:
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            rel_parts = path.relative_to(root).parts
            if any(part in SKIP_DIRS for part in rel_parts):
                continue
            if (root / "tests" / "fixtures") in path.parents:
                continue
            if path.suffix.lower() in TEXT_SUFFIXES:
                paths.append(path)
    for name in ["README.md", "README.ru.md", "CHANGELOG.md", "LICENSE", "install.py"]:
        path = root / name
        if path.is_file():
            paths.append(path)
    return sorted(set(paths))


def check_links(path: Path) -> None:
    text = read_text(path)
    for target in re.findall(r"\]\(([^)]+)\)", text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        clean = target.split("#", 1)[0].strip()
        if not clean:
            continue
        if clean.startswith("<"):
            clean = clean.strip("<>")
        resolved = (path.parent / clean).resolve()
        if not resolved.exists():
            fail(f"{path.relative_to(root)}: broken link: {target}")


def check_skill() -> None:
    skill = skill_dir / "SKILL.md"
    text = read_text(skill)
    if not text:
        return
    top, meta = parse_frontmatter(text)

    if top.get("name") != SKILL_NAME:
        fail(f"frontmatter name must be {SKILL_NAME!r}, got {top.get('name')!r}")
    name = top.get("name", "")
    if not re.fullmatch(r"[a-z0-9-]{1,64}", name):
        fail(f"frontmatter name is invalid: {name!r}")

    description = top.get("description", "")
    if not 80 <= len(description) <= 1024:
        fail(f"description length must be 80..1024, got {len(description)}")
    if "do not use" not in description.lower():
        fail("description must include negative triggers ('Do NOT use')")
    if top.get("license") != "MIT":
        fail("frontmatter license must be MIT")
    if not top.get("compatibility"):
        fail("frontmatter compatibility is required")
    if not meta.get("author"):
        fail("metadata.author is required")
    if not meta.get("repository"):
        fail("metadata.repository is required")
    if not re.fullmatch(r"\[[a-z]{2}(, *[a-z]{2})*\]", meta.get("languages", "")):
        fail(
            "metadata.languages must be a YAML list such as [en, ru], got "
            f"{meta.get('languages')!r}"
        )

    version = meta.get("version", "")
    if not semver(version):
        fail(f"metadata.version must be semver, got {version!r}")
    modes = meta.get("modes", "")
    if not modes.isdigit():
        fail(f"metadata.modes must be a number, got {modes!r}")
    guidelines = meta.get("guidelines", "")
    if not guidelines.isdigit():
        fail(f"metadata.guidelines must be a number, got {guidelines!r}")

    for section in REQUIRED_SECTIONS:
        if f"## {section}" not in text:
            fail(f"missing section: ## {section}")

    if len(text.splitlines()) > 500:
        fail(f"SKILL.md must stay at or under 500 lines, got {len(text.splitlines())}")

    mode_block = (
        text.split("## Modes", 1)[1].split("\n## ", 1)[0]
        if "## Modes" in text
        else ""
    )
    mode_rows = re.findall(r"^\| `([a-z-]+)` \|", mode_block, re.M)
    if len(mode_rows) < 2:
        fail(f"Modes table must list at least 2 modes, got {len(mode_rows)}")
    if modes.isdigit() and int(modes) != len(mode_rows):
        fail(f"metadata.modes={modes} does not match {len(mode_rows)} rows")

    for needle in ("TODO", "FIXME"):
        if needle in text:
            fail(f"SKILL.md contains forbidden string: {needle}")

    if "]()" in text:
        fail("SKILL.md contains an empty badge or link")

    check_links(skill)

    listed: set[str] = set()
    for match in re.findall(r"`((?:references|agents)/[^`]+)`", text):
        if "[" in match or match.endswith("/"):
            continue
        listed.add(match)
    for rel in sorted(listed):
        if not (skill_dir / rel).exists():
            fail(f"SKILL.md references missing path: {rel}")

    for rel in sorted(listed):
        if rel.endswith(".md"):
            check_links(skill_dir / rel)

    if (skill_dir / "references").is_dir():
        for reference in sorted((skill_dir / "references").glob("*.md")):
            check_links(reference)


def check_guidelines() -> None:
    path = skill_dir / "references" / "guidelines.md"
    text = read_text(path)
    ids = re.findall(r"^## (G\d+)\. ", text, re.M)
    numbers = [int(item[1:]) for item in ids]
    if numbers != list(range(1, len(numbers) + 1)):
        fail(f"references/guidelines.md guidelines must be sequential from G1, got {ids}")
    _, meta = parse_frontmatter(read_text(skill_dir / "SKILL.md"))
    declared = meta.get("guidelines", "")
    if declared.isdigit() and int(declared) != len(ids):
        fail(f"metadata.guidelines={declared} does not match {len(ids)} guidelines")
    if not ids:
        fail("references/guidelines.md defines no guidelines")


def check_version_files(version: str) -> None:
    if not version:
        return
    changelog = read_text(root / "CHANGELOG.md")
    if f"[{version}]" not in changelog:
        fail(f"CHANGELOG.md has no entry for {version}")
    for name in ("README.md", "README.ru.md"):
        text = read_text(root / name)
        if version not in text:
            fail(f"{name} does not mention version {version}")

    plugin = root / ".claude-plugin" / "plugin.json"
    marketplace = root / ".claude-plugin" / "marketplace.json"
    cursor = root / ".cursor-plugin" / "plugin.json"
    for path, required in (
        (plugin, ("name", "displayName", "description", "version", "author", "homepage", "repository", "license", "keywords")),
        (cursor, ("name", "displayName", "description", "version", "author", "homepage", "repository", "license")),
    ):
        if not path.exists():
            fail(f"missing manifest: {path.relative_to(root)}")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f"{path.relative_to(root)}: invalid JSON: {exc}")
            continue
        for field in required:
            if not data.get(field):
                fail(f"{path.relative_to(root)} missing field: {field}")
        if str(data.get("version", "")) != version:
            fail(
                f"{path.relative_to(root)} version {data.get('version')!r} "
                f"does not match {version!r}"
            )
        skills_path = data.get("skills", "")
        if skills_path and not (root / skills_path.lstrip("./")).exists():
            fail(f"{path.relative_to(root)} skills path does not exist: {skills_path}")

    if marketplace.exists():
        try:
            data = json.loads(marketplace.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            fail(f".claude-plugin/marketplace.json: invalid JSON: {exc}")
            return
        owner = data.get("owner") or {}
        if not owner.get("name") or not owner.get("url"):
            fail(".claude-plugin/marketplace.json missing owner.name or owner.url")
        entry = (data.get("plugins") or [{}])[0]
        for field in ("name", "source", "description", "version", "homepage", "repository"):
            if not entry.get(field):
                fail(f".claude-plugin/marketplace.json missing plugins[0].{field}")
        if str(entry.get("version", "")) != version:
            fail("marketplace.json version does not match SKILL.md")


def check_openai_yaml() -> None:
    path = skill_dir / "agents" / "openai.yaml"
    text = read_text(path)
    for needle in (
        "interface:",
        "display_name:",
        "short_description:",
        "default_prompt:",
        "policy:",
        "allow_implicit_invocation:",
    ):
        if needle not in text:
            fail(f"agents/openai.yaml missing {needle!r}")


def check_installer() -> None:
    text = read_text(root / "install.py")
    for needle in (
        '"claude"',
        '"opencode"',
        '"agents"',
        '"codex"',
        '"project"',
        "all",
        "--check",
        "--dry-run",
        "--list",
        "--with-deps",
        'default="all"',
    ):
        if needle not in text:
            fail(f"install.py does not contain {needle!r}")
    for forbidden in ("evals", "docs", "tests/fixtures", "SPEC.md", "ARCHITECTURE.md"):
        if f'"{forbidden}"' in text or f"'{forbidden}'" in text:
            fail(f"install.py payload must not include {forbidden}")


def check_root_files() -> None:
    for rel in REQUIRED_ROOT_FILES:
        if not (root / rel).exists():
            fail(f"missing required file: {rel}")


def check_evals() -> None:
    path = root / "evals" / "cases.md"
    if not path.exists():
        return
    text = read_text(path)
    cases = re.findall(r"^\| E-\d+ \|", text, re.M)
    if len(cases) < 3:
        fail(f"evals/cases.md must contain at least 3 cases, got {len(cases)}")


def main() -> int:
    global root, skill_dir
    parser = argparse.ArgumentParser(
        description="Validate the wordpress-plugin-requirements skill."
    )
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    args = parser.parse_args()
    root = args.root.resolve()
    skill_dir = root / "skills" / SKILL_NAME

    if not skill_dir.exists():
        fail(f"missing skill directory: skills/{SKILL_NAME}")

    check_root_files()

    for path in iter_project_text_files():
        check_encoding(path)
        check_dashes(path)

    for name in ("README.md", "README.ru.md"):
        readme = root / name
        if readme.is_file():
            check_links(readme)

    if skill_dir.exists():
        check_skill()
        check_guidelines()
        check_openai_yaml()

    version = ""
    if (skill_dir / "SKILL.md").exists():
        _, meta = parse_frontmatter(read_text(skill_dir / "SKILL.md"))
        version = meta.get("version", "")
    check_version_files(version)
    check_installer()
    check_evals()

    if errors:
        print("wordpress-plugin-requirements validator")
        print("\nErrors:")
        for message in errors:
            print(f"  - {message}")
        print(f"\nFAILED: {len(errors)} error(s)")
        return 1
    print("wordpress-plugin-requirements validator")
    print("OK: all structural checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
