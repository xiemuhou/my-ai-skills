# init-project — 项目初始化文档生成

`init-project` 用来为一个项目生成 AI 协作所需的基础文档。它会分析当前目录，推断项目类型，并生成或更新 `AGENTS.md`、`CLAUDE.md`、`README.md`、`CHANGELOG.md`、`.gitignore` 和基础 `docs/` 目录。

## 快速开始

在项目根目录对 AI 说：

```text
初始化项目
```

或者更明确一些：

```text
请使用 init-project skill 初始化当前项目
```

默认会自动检测项目语言、目录结构和用途，并生成适合当前项目的文档。

## 会生成什么

| 文件或目录 | 作用 | 默认行为 |
| --- | --- | --- |
| `AGENTS.md` | 跨平台通用 AI 项目指令 | 生成或智能合并 |
| `CLAUDE.md` | Claude Code 适配文件，引用 `AGENTS.md` | 生成或智能合并 |
| `README.md` | 项目介绍和使用说明 | 不存在时生成 |
| `CHANGELOG.md` | 项目变更记录 | 不存在时生成，必要时追加 |
| `.gitignore` | 安全优先的忽略规则 | 不存在时生成 |
| `docs/` | 文档目录 | 完整初始化时补齐 |
| `docs/plans/` | 计划文档目录 | 完整初始化时补齐 |

## AGENTS.md 和 CLAUDE.md 的关系

核心原则：

```text
AGENTS.md 是 Single Source of Truth。
CLAUDE.md 只做 Claude Code 适配，并通过 @./AGENTS.md 引用 AGENTS.md。
```

这样你主要维护 `AGENTS.md`，Claude Code 也能自动获得同一套项目指令。

## 适合场景

| 你的需求 | 推荐说法 |
| --- | --- |
| 给新项目补齐 AI 协作文档 | `初始化项目` |
| 只生成项目指令 | `生成 AGENTS.md 和 CLAUDE.md` |
| 覆盖旧文档 | `初始化项目 --overwrite` |
| 只更新 README | `只生成 README.md` |
| 只更新 CHANGELOG | `只生成 CHANGELOG.md` |
| 指定项目描述 | `初始化项目，项目描述是：个人技能仓库` |

## 脚本用法

自然语言是推荐入口。如果你想直接运行脚本：

```powershell
python init-project/scripts/generate.py --auto
```

常用参数：

| 参数 | 作用 |
| --- | --- |
| `--auto` | 自动检测项目信息 |
| `--project-name <name>` | 指定项目名称 |
| `--project-description <text>` | 指定项目描述 |
| `--workflow <text>` | 指定核心工作流 |
| `--language <lang>` | 指定默认语言 |
| `--output-dir <path>` | 指定输出目录 |
| `--overwrite` | 覆盖已有文件 |
| `--detect-language-only` | 只检测语言 |
| `--skip-readme` | 跳过 README |
| `--skip-changelog` | 跳过 CHANGELOG |
| `--skip-gitignore` | 跳过 `.gitignore` |
| `--only-readme` | 只生成 README |
| `--only-changelog` | 只生成 CHANGELOG |

## Prompt 示例

初始化当前项目：

```text
初始化项目
```

为已有项目补齐指令文件：

```text
请生成 AGENTS.md 和 CLAUDE.md，保留我已有的 README.md
```

覆盖生成：

```text
初始化项目 --overwrite
```

指定项目背景：

```text
初始化项目。项目名称是 my-ai-skills，项目用途是管理个人 Codex 和 Claude Code skills。
```

## 安全边界

- 默认不会覆盖已有 `README.md`。
- 已有 `AGENTS.md` / `CLAUDE.md` 时会优先智能合并。
- 使用 `--overwrite` 才会覆盖已有文件。
- 生成 `.gitignore` 时优先避免把密钥、缓存、环境文件提交进 Git。

## 常见问题

### 为什么 CHANGELOG.md 是强制性的？

它帮助项目持续记录重要变更，尤其是 AI 指令文件、项目结构和工作流变化。这样后续维护时能知道“为什么变成这样”。

### 已经有 README.md 了会怎样？

默认跳过，不覆盖。你可以明确要求 `--overwrite` 或 `--only-readme`。

### 可以只生成 AGENTS.md 吗？

可以在自然语言里明确要求，但完整初始化默认会同时处理 `AGENTS.md` 和 `CLAUDE.md`，保证跨平台一致。
