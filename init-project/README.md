# init-project — 项目初始化文档生成

本 README 面向使用者：如何触发并正确使用 `init-project` skill。执行细节、模板和参数在 `SKILL.md`、`config.yaml` 与 `templates/`。

`init-project` 用来为项目生成 AI 协作基础文档。它会分析当前目录，推断项目类型，并生成或更新 `AGENTS.md`、`CLAUDE.md`、`README.md`、`CHANGELOG.md`、`.gitignore` 和基础 `docs/` 目录。

## 快速开始

在项目根目录说：

```text
请使用 init-project skill 初始化当前项目
输入：当前项目目录
输出：AGENTS.md、CLAUDE.md、README.md、CHANGELOG.md、.gitignore、docs/
```

最短触发：

```text
初始化项目
```

## 触发方式

| 你的需求 | 推荐说法 |
| --- | --- |
| 初始化新项目 | `初始化项目` |
| 补齐 AI 协作文档 | `生成 AGENTS.md 和 CLAUDE.md` |
| 覆盖旧文档 | `初始化项目 --overwrite` |
| 只生成 README | `只生成 README.md` |
| 只生成 CHANGELOG | `只生成 CHANGELOG.md` |
| 指定项目描述 | `初始化项目，项目描述是：个人技能仓库` |

## 会生成什么

| 文件或目录 | 作用 | 默认行为 |
| --- | --- | --- |
| `AGENTS.md` | 跨平台通用 AI 项目指令 | 生成或智能合并 |
| `CLAUDE.md` | Claude Code 适配文件，引用 `AGENTS.md` | 生成或智能合并 |
| `README.md` | 项目介绍和使用说明 | 不存在时生成 |
| `CHANGELOG.md` | 项目变更记录 | 不存在时生成，必要时追加 |
| `.gitignore` | 安全优先的忽略规则 | 不存在时生成或智能合并 |
| `docs/` | 文档根目录 | 完整初始化时补齐 |
| `docs/plans/` | 计划文档目录 | 完整初始化时补齐 |

## 核心概念

`AGENTS.md` 是项目 AI 指令的唯一事实来源。`CLAUDE.md` 只做 Claude Code 适配，并通过下面的方式引用 `AGENTS.md`：

```markdown
@./AGENTS.md
```

这样你主要维护 `AGENTS.md`，Codex、Claude Code 和其他支持 AGENTS.md 的工具都能共享同一套项目规则。

## 默认流程

```text
扫描目录 -> 判断项目类型 -> 提取项目名称和描述 -> 生成文档 -> 智能合并已有内容 -> 初始化 docs 目录
```

支持识别的常见项目类型包括 Python、Web、Rust、Go、Java、数据科学和文档项目。

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
| `--skip-readme` | 跳过 README |
| `--skip-changelog` | 跳过 CHANGELOG |
| `--skip-gitignore` | 跳过 `.gitignore` |
| `--only-readme` | 只生成 README |
| `--only-changelog` | 只生成 CHANGELOG |

## 示例

初始化当前项目：

```text
初始化项目
```

保留已有 README：

```text
请生成 AGENTS.md 和 CLAUDE.md，保留我已有的 README.md
```

指定背景：

```text
初始化项目。项目名称是 my-ai-skills，项目用途是管理个人 Codex 和 Claude Code skills。
```

覆盖生成：

```text
初始化项目 --overwrite
```

## 安全边界

- 只在当前项目目录内创建或修改文件。
- 默认不会覆盖已有 `README.md`。
- 已有 `AGENTS.md` / `CLAUDE.md` 时优先智能合并。
- 使用 `--overwrite` 才会覆盖已有文件。
- `.gitignore` 默认包含敏感文件、缓存和环境文件忽略规则。

## 常见问题

### 为什么一定要 CHANGELOG.md？

它用于记录项目结构、AI 指令和工作流变化，方便后续维护时知道“为什么这么改”。

### 已经有 AGENTS.md 会怎样？

默认智能合并，尽量保留你的项目目标、核心工作流和自定义章节，只更新标准化内容。

### 可以只生成 AGENTS.md 吗？

可以在自然语言里明确要求。但完整初始化默认同时处理 `AGENTS.md` 和 `CLAUDE.md`，保证跨平台一致。
