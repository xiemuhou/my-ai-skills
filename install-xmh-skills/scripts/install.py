#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
install-xmh-skills — 将当前仓库的 skills 复制安装到系统级目录。

安装目标:
  - ~/.codex/skills/   (Codex)
  - ~/.claude/skills/  (Claude Code)

用法:
  python install.py                  # 默认安装到两个平台
  python install.py --codex          # 仅安装到 Codex
  python install.py --claude         # 仅安装到 Claude Code
  python install.py --force          # 强制重装
  python install.py --dry-run        # 预览模式
  python install.py --source <path>  # 指定源目录
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

# ── 编码设置 ──────────────────────────────────────────────
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")

# ── 常量 ──────────────────────────────────────────────────
_IGNORE_DIR_NAMES = {"__pycache__", ".pytest_cache", ".mypy_cache", "test", "tests", "plans"}
_IGNORE_FILE_NAMES = {".DS_Store"}
_IGNORE_ROOT_FILE_NAMES = {"readme.md", "changelog.md", "skill.yaml", "skill.yml"}
_IGNORE_GLOBS = ("*.pyc", "*.pyo")

# ── 数据类 ────────────────────────────────────────────────


@dataclass
class Target:
    label: str       # "codex" | "claude"
    root: Path       # ~/.codex/skills 或 ~/.claude/skills


@dataclass
class SkillInfo:
    name: str
    src: Path
    dest: Path
    md5: str
    installed: bool = False
    skipped: bool = False
    reason: str = ""


@dataclass
class InstallReport:
    target_label: str
    target_root: Path
    installed_skills: list[SkillInfo] = field(default_factory=list)
    skipped_skills: list[SkillInfo] = field(default_factory=list)
    process_messages: list[str] = field(default_factory=list)


# ── 工具函数 ──────────────────────────────────────────────


def _now_stamp() -> str:
    return time.strftime("%Y%m%d-%H%M%S", time.localtime())


def _should_ignore(rel_path: Path) -> bool:
    """判断相对路径是否应在复制时忽略。"""
    if len(rel_path.parts) == 1 and rel_path.name.lower() in _IGNORE_ROOT_FILE_NAMES:
        return True
    if any(part.startswith(".") for part in rel_path.parts):
        return True
    if any(part in _IGNORE_DIR_NAMES for part in rel_path.parts):
        return True
    if rel_path.name in _IGNORE_FILE_NAMES:
        return True
    if any(rel_path.name.endswith(p.lstrip("*")) for p in _IGNORE_GLOBS if p.startswith("*.")):
        return True
    return False


def _copytree_ignore(src_root: Path):
    """返回 shutil.copytree 的 ignore 回调。"""
    def _ignore(current_dir: str, names: list[str]) -> list[str]:
        current_path = Path(current_dir)
        ignored: list[str] = []
        for name in names:
            try:
                rel = (current_path / name).relative_to(src_root)
            except ValueError:
                continue
            if _should_ignore(rel):
                ignored.append(name)
        return ignored
    return _ignore


def _calculate_skill_md5(skill_dir: Path) -> str:
    """计算 skill 目录的 MD5 哈希值。"""
    hasher = hashlib.md5()
    for file in sorted(skill_dir.rglob("*")):
        if not file.is_file():
            continue
        rel = file.relative_to(skill_dir)
        if _should_ignore(rel):
            continue
        hasher.update(str(rel).encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(file.read_bytes())
    return hasher.hexdigest()


def _get_installed_md5(dest_dir: Path, target_label: str) -> str | None:
    """从 manifest 文件读取已安装 skill 的 MD5。"""
    manifest = dest_dir / f".skill-manifest.{target_label}.json"
    if manifest.exists():
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            return data.get("md5")
        except (json.JSONDecodeError, KeyError):
            pass
    if dest_dir.exists():
        try:
            return _calculate_skill_md5(dest_dir)
        except Exception:
            pass
    return None


def _save_skill_manifest(dest_dir: Path, md5: str, source: str | Path, target_label: str) -> None:
    """保存 skill 版本信息到 manifest 文件。"""
    manifest = dest_dir / f".skill-manifest.{target_label}.json"
    data = {
        "md5": md5,
        "source": str(source),
        "installed_at": _now_stamp(),
        "target": target_label,
    }
    manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _find_skill_dirs(skills_root: Path) -> list[Path]:
    """扫描 skills 根目录，返回所有包含 SKILL.md 的子目录（仅顶级）。"""
    result: list[Path] = []
    if not skills_root.exists() or not skills_root.is_dir():
        return result
    for child in sorted(skills_root.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith("."):
            continue
        if (child / "SKILL.md").exists():
            result.append(child)
    return result


def _detect_source_roots() -> list[Path]:
    """自动检测 skills 源目录。按优先级尝试多个候选路径。"""
    cwd = Path.cwd().resolve()

    # 候选：pipelines/skills, skills, 当前目录
    candidates = [cwd / "pipelines" / "skills", cwd / "skills", cwd]

    # 如果脚本在 install-xmh-skills/scripts/ 下，repo 根在 parents[2]
    script_path = Path(__file__).resolve()
    repo_candidate = script_path.parents[2]

    # 判断 repo_candidate 是否看起来像是源（包含 SKILL.md 子目录）
    if _find_skill_dirs(repo_candidate):
        # 检查不在已安装的目标目录中
        home = Path.home()
        if not any(
            str(repo_candidate.resolve()).startswith(str(r))
            for r in [home / ".codex" / "skills", home / ".claude" / "skills"]
        ):
            candidates.insert(0, repo_candidate)

    # 去重
    seen: set[str] = set()
    result: list[Path] = []
    for p in candidates:
        if not p.exists():
            continue
        rp = str(p.resolve())
        if rp not in seen:
            seen.add(rp)
            result.append(p)
    return result


# ── 表格输出 ──────────────────────────────────────────────


def _display_width(s: str) -> int:
    """计算字符串的显示宽度（CJK/emoji 字符按 2 宽度计算）。"""
    w = 0
    for ch in s:
        if ord(ch) > 127:
            w += 2
        else:
            w += 1
    return w


def _pad_display(s: str, width: int) -> str:
    """按显示宽度填充字符串。"""
    need = width - _display_width(s)
    return s + (" " * max(need, 0))


def _print_skill_table(
    installed: list[SkillInfo],
    skipped: list[SkillInfo],
) -> None:
    """打印技能安装结果表格。"""
    all_skills = installed + skipped
    if not all_skills:
        return

    header_name = "Skill 名称"
    header_status = "状态"
    header_reason = "原因"

    name_width = max(
        max((_display_width(s.name) for s in all_skills), default=15),
        _display_width(header_name),
    ) + 2
    status_width = max(
        _display_width(header_status),
        12,
    ) + 2
    reason_width = max(
        max((_display_width(s.reason) for s in all_skills), default=20),
        _display_width(header_reason),
    ) + 2

    sep = "─" * name_width + "┬" + "─" * status_width + "┬" + "─" * reason_width

    print()
    print("┌" + sep + "┐")
    print(f"│ {_pad_display(header_name, name_width)} │ {_pad_display(header_status, status_width)} │ {_pad_display(header_reason, reason_width)} │")
    print("├" + sep.replace("┬", "┼") + "┤")

    for s in sorted(all_skills, key=lambda x: not x.installed):
        if s.installed:
            status = "✅ 已安装"
            reason = f"MD5: {s.md5[:12]}..."
        else:
            status = "⏭️  跳过"
            reason = s.reason or "版本未变化"
        print(f"│ {_pad_display(s.name, name_width)} │ {_pad_display(status, status_width)} │ {_pad_display(reason, reason_width)} │")

    print("└" + sep.replace("┬", "┴") + "┘")


def _print_report(report: InstallReport) -> None:
    """打印安装报告。"""
    print()
    print("─" * 60)
    print(f"📦 目标: {report.target_label.upper()} ({report.target_root})")
    print("─" * 60)

    for msg in report.process_messages:
        print(msg)

    _print_skill_table(report.installed_skills, report.skipped_skills)

    total_in = len(report.installed_skills)
    total_skip = len(report.skipped_skills)
    print()
    print(f"📊 {report.target_label}: {total_in} 个已安装, {total_skip} 个跳过")


# ── 核心安装逻辑 ──────────────────────────────────────────


def _install_to_target(
    target: Target,
    skill_dirs: list[Path],
    dry_run: bool = False,
    force: bool = False,
) -> InstallReport:
    """安装 skills 到指定目标平台。"""
    report = InstallReport(
        target_label=target.label,
        target_root=target.root,
    )

    if not dry_run:
        target.root.mkdir(parents=True, exist_ok=True)

    for src_dir in skill_dirs:
        dest_dir = target.root / src_dir.name
        src_md5 = _calculate_skill_md5(src_dir)
        installed_md5 = None if force else _get_installed_md5(dest_dir, target.label)

        info = SkillInfo(name=src_dir.name, src=src_dir, dest=dest_dir, md5=src_md5)

        if installed_md5 == src_md5:
            info.skipped = True
            info.reason = "版本未变化"
            report.skipped_skills.append(info)
            continue

        # 删除旧版本
        if dest_dir.exists():
            if dry_run:
                report.process_messages.append(f"  [dry-run] 删除: {dest_dir}")
            else:
                if dest_dir.is_symlink() or dest_dir.is_file():
                    dest_dir.unlink()
                else:
                    shutil.rmtree(dest_dir)
                report.process_messages.append(f"  🗑️  已删除旧版本: {dest_dir.name}")

        # 复制新版本
        if dry_run:
            report.process_messages.append(f"  [dry-run] 安装: {src_dir.name} -> {dest_dir}")
        else:
            shutil.copytree(
                src_dir, dest_dir,
                symlinks=False,
                dirs_exist_ok=False,
                ignore=_copytree_ignore(src_dir),
            )
            _save_skill_manifest(dest_dir, src_md5, str(src_dir), target.label)
            report.process_messages.append(f"  ✅ 已安装: {src_dir.name}")

        info.installed = True
        info.reason = f"MD5: {src_md5[:12]}..."
        report.installed_skills.append(info)

    return report


# ── 主入口 ────────────────────────────────────────────────


def main(argv: list[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(
        description="install-xmh-skills — 将 skills 复制安装到 ~/.codex/skills/ 和 ~/.claude/skills/"
    )
    parser.add_argument("--dry-run", action="store_true", help="预览模式，不实际写入文件")
    parser.add_argument("--codex", action="store_true", help="仅安装到 ~/.codex/skills/")
    parser.add_argument("--claude", action="store_true", help="仅安装到 ~/.claude/skills/")
    parser.add_argument("--force", action="store_true", help="强制重新安装所有 skill（忽略 MD5 比较）")
    parser.add_argument("--source", type=str, default=None, help="指定 skills 源目录路径")

    args = parser.parse_args(argv)

    # 确定目标平台
    install_codex = args.codex or (not args.codex and not args.claude)
    install_claude = args.claude or (not args.codex and not args.claude)

    # 确定源目录
    if args.source:
        source_roots = [Path(args.source).resolve()]
    else:
        source_roots = _detect_source_roots()

    if not source_roots:
        print("❌ 错误: 未找到 skills 源目录。请使用 --source 指定路径。")
        return 1

    # 只使用第一个有效的源目录
    skills_root = source_roots[0]
    print(f"🔍 扫描源目录: {skills_root}")

    skill_dirs = _find_skill_dirs(skills_root)

    if not skill_dirs:
        print(f"❌ 未在 {skills_root} 中找到任何 skill 目录（需要包含 SKILL.md）")
        return 1

    print(f"📋 发现 {len(skill_dirs)} 个 skill: {', '.join(d.name for d in skill_dirs)}")

    # 构建目标列表
    home = Path.home()
    targets: list[Target] = []
    if install_codex:
        targets.append(Target(label="codex", root=home / ".codex" / "skills"))
    if install_claude:
        targets.append(Target(label="claude", root=home / ".claude" / "skills"))

    # 执行安装
    reports: list[InstallReport] = []
    for target in targets:
        report = _install_to_target(
            target=target,
            skill_dirs=skill_dirs,
            dry_run=args.dry_run,
            force=args.force,
        )
        reports.append(report)
        _print_report(report)

    # 总体摘要
    print()
    print("=" * 60)
    print("📊 安装摘要")
    print("=" * 60)

    installed_names: set[str] = set()
    skipped_names: set[str] = set()
    for r in reports:
        for s in r.installed_skills:
            installed_names.add(s.name)
        for s in r.skipped_skills:
            skipped_names.add(s.name)

    print(f"  ✅ 已安装: {len(installed_names)} 个 ({', '.join(sorted(installed_names)) or '无'})")
    print(f"  ⏭️  跳过: {len(skipped_names)} 个 ({', '.join(sorted(skipped_names)) or '无'})")

    for target in targets:
        print(f"  📁 {target.label}: {target.root}")

    print("=" * 60)

    if args.dry_run:
        print()
        print("💡 这是预览模式，没有实际修改文件。去掉 --dry-run 以执行安装。")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
