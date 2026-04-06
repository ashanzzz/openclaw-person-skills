#!/usr/bin/env python3
"""
Skill Packager - 将 Skill 目录打包成分发文件

Usage:
    python3 package_skill.py <skill-path> [output-directory]

Example:
    python3 package_skill.py ../skills/my-new-skill
    python3 package_skill.py ../skills/my-new-skill ./dist
"""

import sys
import zipfile
from pathlib import Path
from typing import Optional, Tuple

from quick_validate import validate_skill

EXCLUDED_DIRS = {".git", ".svn", ".hg", "__pycache__", "node_modules", ".DS_Store"}


def _is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def package_skill(skill_path: str, output_dir: str = None) -> Optional[Path]:
    """打包 Skill 目录为 .skill 文件（zip 格式）"""
    skill_path = Path(skill_path).resolve()

    if not skill_path.exists():
        print(f"[ERROR] 目录不存在: {skill_path}")
        return None
    if not skill_path.is_dir():
        print(f"[ERROR] 不是目录: {skill_path}")
        return None

    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        print(f"[ERROR] SKILL.md 不存在: {skill_md}")
        return None

    # 验证
    print("验证 Skill...")
    valid, msg = validate_skill(skill_path)
    if not valid:
        print(f"[ERROR] 验证失败: {msg}")
        print("   请修复后再打包。")
        return None
    print(f"[OK] {msg}\n")

    # 输出位置
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()

    skill_file = output_path / f"{skill_name}.skill"

    try:
        with zipfile.ZipFile(skill_file, "w", zipfile.ZIP_DEFLATED) as zf:
            for file_path in skill_path.rglob("*"):
                if file_path.is_symlink():
                    print(f"[跳过] 符号链接: {file_path}")
                    continue
                rel_parts = file_path.relative_to(skill_path).parts
                if any(p in EXCLUDED_DIRS for p in rel_parts):
                    continue
                if file_path.is_file():
                    resolved = file_path.resolve()
                    if not _is_within(resolved, skill_path):
                        print(f"[ERROR] 文件超出 Skill 根目录: {file_path}")
                        return None
                    # 避免将输出文件自己打包进去
                    if resolved == skill_file.resolve():
                        print(f"[跳过] 输出文件: {file_path}")
                        continue
                    arcname = Path(skill_name) / file_path.relative_to(skill_path)
                    zf.write(file_path, arcname)
                    print(f"  添加: {arcname}")

        print(f"\n[OK] 打包完成: {skill_file}")
        return skill_file

    except Exception as e:
        print(f"[ERROR] 打包失败: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("用法: python3 package_skill.py <skill-path> [output-directory]")
        print("\n示例:")
        print("  python3 package_skill.py ../skills/my-new-skill")
        print("  python3 package_skill.py ../skills/my-new-skill ./dist")
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"打包 Skill: {skill_path}")
    if output_dir:
        print(f"   输出目录: {output_dir}")
    print()

    result = package_skill(skill_path, output_dir)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
