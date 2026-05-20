#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
XMH Skills 远程安装器 — 无需克隆仓库，一行命令安装所有 skills。

用法:
  # 一键安装到 Codex 和 Claude Code（默认）
  curl -fsSL https://raw.githubusercontent.com/xiemuhou/my-ai-skills/main/install/install.py | python3

  # 或者下载后运行
  python3 install.py              # 默认：同时安装到两个平台
  python3 install.py --codex      # 仅安装到 ~/.codex/skills/
  python3 install.py --claude     # 仅安装到 ~/.claude/skills/
  python3 install.py --force      # 强制重装
  python3 install.py --dry-run    # 预览模式不写入

安装目录:
  ~/.codex/skills/   — Codex
  ~/.claude/skills/  — Claude Code

仓库: https://github.com/xiemuhou/my-ai-skills
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

# ── 编码设置 ──────────────────────────────────────────────
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, "strict")

# ── 常量 ──────────────────────────────────────────────────
REPO_URL = "https://github.com/xiemuhou/my-ai-skills.git"
REPO_BRANCH = "main"

_IGNORE_DIR_NAMES = {"__pycache__", ".pytest_cache", ".mypy_cache", "test", "tests", "plans"}
_IGNORE_FILE_NAMES = {".DS_Store"}
_IGNORE_ROOT_FILE_NAMES = {"readme.md", "changelog.md", "claude.md", ".gitignore"}

# ── 工具函数 ──────────────────────────────────────────────


def _now_stamp() -> str:
    return time.strftime("%Y%m%d-%H%M%S", time.localtime())


def _should_ignore(rel_path: Path) -> bool:
    if len(rel_path.parts) == 1:
        if rel_path.name.lower() in _IGNORE_ROOT_FILE_NAMES:
            return True
        if rel_path.name.lower().startswith("readme"):
            return True
    if any(part.startswith(".") for part in rel_path.parts):
        return True
    if any(part in _IGNORE_DIR_NAMES for part in rel_path.parts):
        return True
    if rel_path.name in _IGNORE_FILE_NAMES:
        return True
    if rel_path.suffix in (".pyc", ".pyo"):
        return True
    return False


def _copytree_ignore(src_root: Path):
    def _ignore(current_dir: str, names: list[str]) -> list[str]:
        current_path = Path(current_dir)
        ignored = []
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
    hasher = hashlib.md5()
    for f in sorted(skill_dir.rglob("*")):
        if not f.is_file():
            continue
        rel = f.relative_to(skill_dir)
        if _should_ignore(rel):
            continue
        hasher.update(str(rel).encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(f.read_bytes())
    return hasher.hexdigest()


def _get_installed_md5(dest_dir: Path, target_label: str) -> str | None:
    manifest = dest_dir / f".skill-manifest.{target_label}.json"
    if manifest.exists():
        try:
            return json.loads(manifest.read_text(encoding="utf-8")).get("md5")
        except (json.JSONDecodeError, KeyError):
            pass
    if dest_dir.exists():
        try:
            return _calculate_skill_md5(dest_dir)
        except Exception:
            pass
    return None


def _save_manifest(dest_dir: Path, md5: str, target_label: str) -> None:
    data = {
        "md5": md5,
        "source": REPO_URL,
        "installed_at": _now_stamp(),
        "target": target_label,
    }
    mf = dest_dir / f".skill-manifest.{target_label}.json"
    mf.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _find_skills(repo_root: Path) -> list[Path]:
    """在克隆的仓库根目录中扫描所有 skill 目录（含 SKILL.md 的直接子目录）。"""
    result = []
    if not repo_root.exists() or not repo_root.is_dir():
        return result
    for child in sorted(repo_root.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith("."):
            continue
        if child.name == "install":
            continue
        if (child / "SKILL.md").exists():
            result.append(child)
    return result


def _clone_repo(temp_dir: Path, branch: str = REPO_BRANCH) -> Path:
    """浅克隆仓库到临时目录，返回仓库根目录路径。"""
    clone_dir = temp_dir / "repo"
    print(f"📦 正在从 GitHub 下载 skills 仓库...")
    print(f"   {REPO_URL}")
    subprocess.run(
        ["git", "clone", "--depth", "1", "--branch", branch, "--single-branch", REPO_URL, str(clone_dir)],
        capture_output=True,
        check=True,
        text=True,
        timeout=300,
    )
    print(f"   ✅ 下载完成")
    return clone_dir


# ── 表格输出 ──────────────────────────────────────────────


def _display_width(s: str) -> int:
    w = 0
    for ch in s:
        w += 2 if ord(ch) > 127 else 1
    return w


def _pad(s: str, width: int) -> str:
    return s + " " * max(width - _display_width(s), 0)


def _print_table(installed, skipped):
    all_skills = installed + skipped
    if not all_skills:
        return
    h_name, h_status, h_reason = "Skill", "状态", "原因"
    nw = max(max((_display_width(s["name"]) for s in all_skills), default=10), _display_width(h_name)) + 2
    sw = max(_display_width(h_status), 12) + 2
    rw = max(max((_display_width(s.get("reason", "")) for s in all_skills), default=20), _display_width(h_reason)) + 2
    sep = "─" * nw + "┬" + "─" * sw + "┬" + "─" * rw
    print()
    print("┌" + sep + "┐")
    print(f"│ {_pad(h_name, nw)} │ {_pad(h_status, sw)} │ {_pad(h_reason, rw)} │")
    print("├" + sep.replace("┬", "┼") + "┤")
    for s in sorted(all_skills, key=lambda x: not x["installed"]):
        status = "✅ 已安装" if s["installed"] else "⏭️  跳过"
        reason = s.get("reason", "版本未变化")
        print(f"│ {_pad(s['name'], nw)} │ {_pad(status, sw)} │ {_pad(reason, rw)} │")
    print("└" + sep.replace("┬", "┴") + "┘")


# ── 安装逻辑 ──────────────────────────────────────────────


def install(target_label: str, target_root: Path, skill_dirs: list[Path], dry_run: bool, force: bool) -> dict:
    installed, skipped, messages = [], [], []

    if not dry_run:
        target_root.mkdir(parents=True, exist_ok=True)

    for src in skill_dirs:
        dest = target_root / src.name
        src_md5 = _calculate_skill_md5(src)
        cur_md5 = None if force else _get_installed_md5(dest, target_label)

        if cur_md5 == src_md5:
            skipped.append({"name": src.name, "installed": False, "reason": "版本未变化"})
            continue

        if dest.exists():
            msg = f"  [dry-run] 删除旧版本: {dest.name}" if dry_run else f"  🗑️  删除旧版本: {dest.name}"
            messages.append(msg)
            if not dry_run:
                if dest.is_symlink() or dest.is_file():
                    dest.unlink()
                else:
                    shutil.rmtree(dest)

        if dry_run:
            messages.append(f"  [dry-run] 安装: {src.name} -> {dest}")
        else:
            shutil.copytree(src, dest, symlinks=False, dirs_exist_ok=False, ignore=_copytree_ignore(src))
            _save_manifest(dest, src_md5, target_label)
            messages.append(f"  ✅ 安装完成: {src.name}")

        installed.append({"name": src.name, "installed": True, "reason": f"MD5: {src_md5[:12]}..."})

    return {"label": target_label, "root": target_root, "installed": installed, "skipped": skipped, "messages": messages}


def _print_report(report: dict) -> None:
    print()
    print("─" * 60)
    print(f"📦 {report['label'].upper()} -> {report['root']}")
    print("─" * 60)
    for m in report["messages"]:
        print(m)
    _print_table(report["installed"], report["skipped"])
    print(f"\n📊 {report['label']}: {len(report['installed'])} 个已安装, {len(report['skipped'])} 个跳过")


# ── 主入口 ────────────────────────────────────────────────


def main(argv: list[str] | None = None):
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser(description="XMH Skills 远程安装器 — 无需克隆仓库，一键安装")
    parser.add_argument("--dry-run", action="store_true", help="预览模式")
    parser.add_argument("--codex", action="store_true", help="仅安装到 ~/.codex/skills/")
    parser.add_argument("--claude", action="store_true", help="仅安装到 ~/.claude/skills/")
    parser.add_argument("--force", action="store_true", help="强制重新安装所有 skill")
    parser.add_argument("--branch", type=str, default=REPO_BRANCH, help=f"Git 分支 (默认: {REPO_BRANCH})")
    args = parser.parse_args(argv)

    # 默认安装两个平台
    install_codex = args.codex or (not args.codex and not args.claude)
    install_claude = args.claude or (not args.codex and not args.claude)

    print()
    print("╔══════════════════════════════════════════════╗")
    print("║       XMH Skills 远程安装器                  ║")
    print("║  https://github.com/xiemuhou/my-ai-skills    ║")
    print("╚══════════════════════════════════════════════╝")

    # 克隆仓库
    temp_dir = Path(tempfile.mkdtemp(prefix="xmh-skills-"))
    try:
        repo_root = _clone_repo(temp_dir, branch=args.branch)
        skill_dirs = _find_skills(repo_root)

        if not skill_dirs:
            print("❌ 未找到任何 skill。")
            return 1

        print(f"📋 发现 {len(skill_dirs)} 个 skill: {', '.join(d.name for d in skill_dirs)}")

        home = Path.home()
        targets = []
        if install_codex:
            targets.append(("codex", home / ".codex" / "skills"))
        if install_claude:
            targets.append(("claude", home / ".claude" / "skills"))

        reports = []
        for label, root in targets:
            report = install(label, root, skill_dirs, args.dry_run, args.force)
            reports.append(report)
            _print_report(report)

        # 摘要
        print()
        print("=" * 60)
        print("📊 安装摘要")
        print("=" * 60)
        inames = {s["name"] for r in reports for s in r["installed"]}
        snames = {s["name"] for r in reports for s in r["skipped"]}
        print(f"  ✅ 已安装: {len(inames)} 个 ({', '.join(sorted(inames)) or '无'})")
        print(f"  ⏭️  跳过: {len(snames)} 个 ({', '.join(sorted(snames)) or '无'})")
        for label, root in targets:
            print(f"  📁 {label}: {root}")
        print("=" * 60)

        if args.dry_run:
            print("\n💡 预览模式，未实际修改。去掉 --dry-run 执行安装。")
        else:
            print("\n🎉 安装完成！现在可以在任意项目中使用这些 skills 了。")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
