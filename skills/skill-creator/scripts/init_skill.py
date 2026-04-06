#!/usr/bin/env python3
"""
Skill Initializer - 创建新的 OpenClaw Skill 目录

Usage:
    python3 init_skill.py <skill-name> --path <output-dir> [--resources scripts,references,assets] [--examples]

Examples:
    python3 init_skill.py erpnext-helper --path ~/workspace/skills
    python3 init_skill.py finance-reconcile --path . --resources scripts,references
    python3 init_skill.py my-skill --path . --resources scripts --examples
"""

import argparse
import re
import sys
from pathlib import Path

MAX_SKILL_NAME_LENGTH = 64
ALLOWED_RESOURCES = {"scripts", "references", "assets"}

SKILL_TEMPLATE = '''---
name: {skill_name}
description: [TODO: 完整描述这个 Skill 做什么，以及何时触发。
格式：描述 + 具体触发条件。
触发条件放这里（不在正文），正文只在触发后才加载。
例如："导出 ERPNext 发票。触发：(1) 用户说"导出某月发票"；(2) 用户提供公司+月份组合"。
]
---

# {skill_title}

## When to Use This Skill

[TODO: 具体触发场景，用户会怎么说，哪些文件/任务类型会触发这个 Skill]

## Context / 背景

[TODO: Agent 需要知道的专业领域知识，具体到你的场景。
不要写通用知识，只写 Agent 不知道的、你这个 Skill 特有的信息。]

## Instructions / 执行步骤

[TODO: 分步流程，每步有明确的质量标准和输出预期。
优先用编号列表，每步说明：
1. 做什么
2. 怎么做（命令/代码片段）
3. 怎么验证]

## Constraints / 约束

[TODO: 禁止事项，来自真实失败经验。
格式：- 绝对不能 X（因为 Y）
- 必须先做 X 才能做 Y
- 避免 X，推荐 Y]

## Examples（推荐）

[TODO: 好/坏输出对比示例。
每个示例包含：
- 场景描述
- 好的输出（符合标准）
- 差的输出（踩坑案例）]

---

## Resources 说明

### scripts/
[TODO: 如果创建了 scripts/，说明里面有什么、可执行什么]

### references/
[TODO: 如果创建了 references/，说明里面有什么、什么时候加载]
'''

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
{skill_name} - 辅助脚本

描述：这个脚本做什么。
用法：python3 scripts/example.py [参数]

依赖：
  - Python 3.8+
  - requests（pip install requests）

Example:
    python3 scripts/example.py --input data.csv
"""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="{skill_name} 辅助工具")
    parser.add_argument("--input", required=True, help="输入文件路径")
    args = parser.parse_args()

    print(f"处理输入: {{args.input}}")
    # TODO: 实现逻辑


if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = '''# {skill_title} - 参考文档

本文件包含 {skill_title} 的详细参考资料，按需加载到 context。

## 目录

- [概述](#概述)
- [API 参考](#api-参考)
- [常见问题](#常见问题)

## 概述

[TODO: 详细描述]

## API 参考

[TODO: API 端点、参数、返回值]

## 常见问题

[TODO: FAQ，来自真实用户问题]

---

**何时加载此文件：**
- 当 Agent 需要执行复杂查询时
- 当 SKILL.md 正文提到"详见 references/xxx"时
- 当用户问题涉及本文件覆盖的细节时
'''

EXAMPLE_ASSET = '''# assets/ 说明

本目录存放不加载到 context、但会在输出中使用的文件。

**常见用途：**
- 模板文件（.xlsx, .docx, .pptx）
- Logo / 图片资源
- 字体文件
- 样例数据（.csv, .json）

**原则：** 这些文件**不被读取进 context**，只被**复制或修改**后用于最终输出。

**添加资源：**
将模板/资源文件直接放入本目录，并在 SKILL.md 的 Resources 说明中描述其用途。
'''


def normalize_skill_name(skill_name: str) -> str:
    """标准化为小写连字符格式"""
    normalized = skill_name.strip().lower()
    normalized = re.sub(r"[^a-z0-9]+", "-", normalized)
    normalized = normalized.strip("-")
    normalized = re.sub(r"-{2,}", "-", normalized)
    return normalized


def title_case(name: str) -> str:
    """连字符转 Title Case"""
    return " ".join(word.capitalize() for word in name.split("-"))


def parse_resources(raw: str) -> list[str]:
    if not raw:
        return []
    resources = [item.strip() for item in raw.split(",") if item.strip()]
    invalid = sorted({r for r in resources if r not in ALLOWED_RESOURCES})
    if invalid:
        print(f"[ERROR] 未知资源类型: {', '.join(invalid)}")
        print(f"   允许: {', '.join(sorted(ALLOWED_RESOURCES))}")
        sys.exit(1)
    deduped, seen = [], set()
    for r in resources:
        if r not in seen:
            deduped.append(r)
            seen.add(r)
    return deduped


def create_skill(skill_name: str, path: str, resources: list[str], include_examples: bool):
    skill_dir = Path(path).resolve() / skill_name
    if skill_dir.exists():
        print(f"[ERROR] 目录已存在: {skill_dir}")
        return None

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"[OK] 创建目录: {skill_dir}")
    except Exception as e:
        print(f"[ERROR] 创建目录失败: {e}")
        return None

    # SKILL.md
    skill_title = title_case(skill_name)
    content = SKILL_TEMPLATE.format(skill_name=skill_name, skill_title=skill_title)
    try:
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")
        print("[OK] 创建 SKILL.md")
    except Exception as e:
        print(f"[ERROR] 写入 SKILL.md 失败: {e}")
        return None

    # 资源目录
    for res in resources:
        res_dir = skill_dir / res
        res_dir.mkdir(exist_ok=True)
        if res == "scripts":
            if include_examples:
                ex = (res_dir / "example.py").write_text(
                    EXAMPLE_SCRIPT.format(skill_name=skill_name), encoding="utf-8"
                )
                (res_dir / "example.py").chmod(0o755)
                print("[OK] 创建 scripts/example.py")
            else:
                print("[OK] 创建 scripts/")
        elif res == "references":
            if include_examples:
                (res_dir / "reference.md").write_text(
                    EXAMPLE_REFERENCE.format(skill_title=skill_title), encoding="utf-8"
                )
                print("[OK] 创建 references/reference.md")
            else:
                print("[OK] 创建 references/")
        elif res == "assets":
            if include_examples:
                (res_dir / "README.txt").write_text(EXAMPLE_ASSET, encoding="utf-8")
                print("[OK] 创建 assets/README.txt")
            else:
                print("[OK] 创建 assets/")

    print(f"\n[OK] Skill '{skill_name}' 初始化完成: {skill_dir}")
    print("\n下一步:")
    print("1. 编辑 SKILL.md，填充 TODO 项")
    print("2. 验证: python3 quick_validate.py <skill-path>")
    return skill_dir


def main():
    parser = argparse.ArgumentParser(description="创建新的 OpenClaw Skill 目录")
    parser.add_argument("skill_name", help="Skill 名称（小写字母/数字/连字符）")
    parser.add_argument("--path", required=True, help="输出目录")
    parser.add_argument("--resources", default="", help="资源目录: scripts,references,assets")
    parser.add_argument("--examples", action="store_true", help="创建示例文件")
    args = parser.parse_args()

    name = normalize_skill_name(args.skill_name)
    if not name:
        print("[ERROR] 名称至少包含一个字母或数字")
        sys.exit(1)
    if len(name) > MAX_SKILL_NAME_LENGTH:
        print(f"[ERROR] 名称过长（{len(name)}字符），上限 {MAX_SKILL_NAME_LENGTH}")
        sys.exit(1)
    if name != args.skill_name:
        print(f"注: 标准化名称: '{args.skill_name}' -> '{name}'")

    resources = parse_resources(args.resources)
    if args.examples and not resources:
        print("[ERROR] --examples 需要配合 --resources")
        sys.exit(1)

    print(f"初始化 Skill: {name}")
    print(f"   位置: {args.path}")
    if resources:
        print(f"   资源: {', '.join(resources)}")
        if args.examples:
            print("   示例: 开启")
    print()

    result = create_skill(name, args.path, resources, args.examples)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
