# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## 项目概述

个人 Codex Skills 集合仓库。每个 skill 是仓库根目录下的独立文件夹，包含 `SKILL.md`（AI 执行规范）和可选的 `README.md`、`config.yaml`。

Skills 通过 `install-xmh-skills` 安装到 `~/.codex/skills/` 和 `~/.Codex/skills/` 后全局可用。

## 项目结构

```
my-ai-skills/
├── README.md                  ← 项目说明
├── AGENTS.md                  ← 本文件
├── git-commit/                ← Skill: 自动化 Git 提交
│   ├── SKILL.md
│   ├── README.md
│   └── config.yaml
└── install-xmh-skills/        ← Skill: Skills 安装器
    ├── SKILL.md
    ├── README.md
    └── scripts/
        └── install.py
```

Skills 放在仓库根目录（而非 `.Codex/skills/`），由安装脚本复制到系统级目录。

## 安装流程

用户说"安装 skills"时，运行：

```powershell
python install-xmh-skills/scripts/install.py
```

脚本自动扫描根目录下含 `SKILL.md` 的子目录（排除 `install-xmh-skills` 自身），通过 MD5 比较增量安装到 `~/.codex/skills/` 和 `~/.Codex/skills/`。

支持参数：`--codex`、`--Codex`（单平台）、`--force`（强制重装）、`--dry-run`（预览）。

## Skill 开发规范

### 目录结构

```
<skill-name>/
├── SKILL.md     ← 必须：YAML frontmatter + 完整执行规范
├── README.md    ← 可选：用户文档
└── config.yaml  ← 可选：默认参数
```

### SKILL.md frontmatter

```yaml
---
name: skill-name
description: 一句话描述
metadata:
  type: skill
  trigger:
    - "触发词1"
    - "触发词2"
---
```

### 执行规范要点

- 核心原则、完整执行流程、参数速查、错误处理表、重要约束（禁止操作）五项齐全
- 安装时自动排除：`README.md`、`CHANGELOG.md`、`tests/`、`plans/`、隐藏文件、`__pycache__`、`*.pyc`
- git-commit 的 `SKILL.md` 可作为开发新 skill 的执行规范参考模板

## 现有 Skills

### git-commit

触发词：`提交改动`、`commit`、`git commit`、`推送`、`push`

Auto 模式（默认）：AI 自主完成 分析→暂存→拆分→提交信息→提交→推送 全流程。Review 模式（`--review`）：关键节点暂停确认。

Conventional Commits 规范，中文提交信息，智能拆分为多个提交（阈值：>300 行 / >20 文件 / >5 顶层目录 / 混合类型）。默认 `git add -A` 暂存所有文件。

安全约束：绝不 force push、绝不 hard reset、绝不跳过 hooks（除非 `--no-verify`）、绝不修改 git config。

### install-xmh-skills

触发词：`安装skills`、`安装技能`、`更新skills`、`/install-xmh-skills`

定位 `install-xmh-skills/scripts/install.py` 并执行。用户说"强制"/"更新"时传 `--force`，"预览"/"看看"时传 `--dry-run`，"codex"/"Codex"时传对应单平台参数。

## 注意事项

- 平台: Windows + VSCode + Codex 扩展
- Shell: PowerShell 优先（但 Bash 工具也可用）
- git-commit 在 main 分支上提交时需警告用户
- Python 脚本使用 `#!/usr/bin/env python3`，Windows 下用 `python` 命令运行
