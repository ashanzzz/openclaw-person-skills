#!/usr/bin/env python3
"""
Quick validation for OpenClaw Skill format

Usage:
    python3 quick_validate.py <skill-directory>

Exit codes:
    0 = valid
    1 = invalid
"""

import re
import sys
from pathlib import Path
from typing import Optional, Tuple

MAX_SKILL_NAME_LENGTH = 64
ALLOWED_PROPERTIES = {"name", "description", "license", "allowed-tools", "metadata"}


def _extract_frontmatter(content: str) -> Optional[str]:
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            return "\n".join(lines[1:i])
    return None


def _parse_simple_frontmatter(text: str) -> Optional[dict]:
    """
    Pure-Python frontmatter parser (fallback when PyYAML unavailable).
    Supports simple key: value mappings.
    """
    parsed, current_key = {}, None
    for raw in text.splitlines():
        stripped = raw.strip()
        if not stripped or stripped.startswith("#"):
            continue
        is_indented = raw[:1].isspace()
        if is_indented:
            if current_key and parsed.get(current_key):
                parsed[current_key] += "\n" + stripped
            continue
        if ":" not in stripped:
            return None
        key, _, value = stripped.partition(":")
        key, value = key.strip(), value.strip()
        if not key:
            return None
        if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
            value = value[1:-1]
        parsed[key] = value
        current_key = key
    return parsed


def validate_skill(skill_path: str) -> Tuple[bool, str]:
    """Validate a Skill directory's format."""
    skill_path = Path(skill_path)

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    try:
        content = skill_md.read_text(encoding="utf-8")
    except OSError as e:
        return False, f"Cannot read SKILL.md: {e}"

    fm_text = _extract_frontmatter(content)
    if fm_text is None:
        return False, "Invalid frontmatter (missing --- delimiters)"

    # Try PyYAML, fallback to simple parser
    try:
        import yaml
        frontmatter = yaml.safe_load(fm_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a YAML dictionary"
    except Exception:
        frontmatter = _parse_simple_frontmatter(fm_text)
        if frontmatter is None:
            return False, "Frontmatter YAML parse failed (install PyYAML for best support)"

    # Check for unexpected fields
    unexpected = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected:
        allowed = ", ".join(sorted(ALLOWED_PROPERTIES))
        return False, f"Unexpected fields: {', '.join(sorted(unexpected))}. Allowed: {allowed}"

    # name checks
    if "name" not in frontmatter:
        return False, "Missing 'name' field"
    name = frontmatter.get("name", "").strip()
    if not isinstance(name, str):
        return False, f"name must be string, got {type(name).__name__}"
    if not re.match(r"^[a-z0-9][a-z0-9-]*$", name):
        return False, f"name '{name}' must be lowercase letters/digits/hyphens, start with letter or digit"
    if len(name) > MAX_SKILL_NAME_LENGTH:
        return False, f"name too long ({len(name)} chars), max {MAX_SKILL_NAME_LENGTH}"

    # description checks
    if "description" not in frontmatter:
        return False, "Missing 'description' field"
    desc = frontmatter.get("description", "").strip()
    if not isinstance(desc, str):
        return False, f"description must be string"
    if "<" in desc or ">" in desc:
        return False, "description must not contain < or > characters"
    if len(desc) > 1024:
        return False, f"description too long ({len(desc)} chars), max 1024"

    # Forbidden files
    forbidden = ["README.md", "CHANGELOG.md", "INSTALLATION_GUIDE.md", "QUICK_REFERENCE.md"]
    for f in forbidden:
        if (skill_path / f).exists():
            return False, f"Forbidden file present: {f} (Skill dirs should not contain user docs)"

    return True, "Validation passed!"


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 quick_validate.py <skill-directory>")
        sys.exit(1)

    valid, msg = validate_skill(sys.argv[1])
    print(msg)
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
