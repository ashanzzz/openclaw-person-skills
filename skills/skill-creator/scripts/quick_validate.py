#!/usr/bin/env python3
"""
快速验证 OpenClaw Skill 格式

Usage:
    python3 quick_validate.py <skill-directory>

Exit codes:
    0 = 验证通过
    1 = 验证失败
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
    纯 Python frontmatter 解析（无 PyYAML 依赖时使用）。
    支持简单的 key: value 映射。
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
    """验证 Skill 目录格式"""
    skill_path = Path(skill_path)

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    try:
        content = skill_md.read_text(encoding="utf-8")
    except OSError as e:
        return False, f"无法读取 SKILL.md: {e}"

    fm_text = _extract_frontmatter(content)
    if fm_text is None:
        return False, "Frontmatter 格式无效（需要 --- 分隔符）"

    # 尝试 PyYAML，如果不可用则降级
    try:
        import yaml
        frontmatter = yaml.safe_load(fm_text)
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter 必须是 YAML 字典"
    except Exception:
        frontmatter = _parse_simple_frontmatter(fm_text)
        if frontmatter is None:
            return False, "Frontmatter YAML 解析失败（请安装 PyYAML 以获得最佳支持）"

    # 检查意外字段
    unexpected = set(frontmatter.keys()) - ALLOWED_PROPERTIES
    if unexpected:
        allowed = ", ".join(sorted(ALLOWED_PROPERTIES))
        return False, f"意外字段: {', '.join(sorted(unexpected))}。允许: {allowed}"

    # name 检查
    if "name" not in frontmatter:
        return False, "缺少 'name' 字段"
    name = frontmatter.get("name", "").strip()
    if not isinstance(name, str):
        return False, f"name 必须是字符串，得到 {type(name).__name__}"
    if not re.match(r"^[a-z0-9][a-z0-9-]*$", name):
        return False, f"name '{name}' 必须为小写字母/数字/连字符，且以字母或数字开头"
    if len(name) > MAX_SKILL_NAME_LENGTH:
        return False, f"name 过长（{len(name)}字符），上限 {MAX_SKILL_NAME_LENGTH}"

    # description 检查
    if "description" not in frontmatter:
        return False, "缺少 'description' 字段"
    desc = frontmatter.get("description", "").strip()
    if not isinstance(desc, str):
        return False, f"description 必须是字符串"
    if "<" in desc or ">" in desc:
        return False, "description 不能包含 < 或 > 符号"
    if len(desc) > 1024:
        return False, f"description 过长（{len(desc)}字符），上限 1024"

    # 禁止的文件检查
    forbidden = ["README.md", "CHANGELOG.md", "INSTALLATION_GUIDE.md", "QUICK_REFERENCE.md"]
    for f in forbidden:
        if (skill_path / f).exists():
            return False, f"禁止文件存在: {f}（Skill 目录不应包含用户文档）"

    return True, "验证通过！"


def main():
    if len(sys.argv) != 2:
        print("用法: python3 quick_validate.py <skill-directory>")
        sys.exit(1)

    valid, msg = validate_skill(sys.argv[1])
    print(msg)
    sys.exit(0 if valid else 1)


if __name__ == "__main__":
    main()
