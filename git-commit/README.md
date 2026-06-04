# git-commit — Git 提交自动化

本 README 面向使用者：如何触发并正确使用 `git-commit` skill。执行细节和默认策略在 `SKILL.md` 与 `config.yaml`。

`git-commit` 用来自动完成 Git 提交流程：分析改动、暂存文件、生成 Conventional Commit 信息、提交，并在默认模式下推送当前分支。

## 快速开始

在 Git 仓库中直接说：

```text
提交改动
```

AI 会按顺序处理：

```text
检查仓库 -> 分析改动 -> 判断是否拆分 -> git add -A -> git commit -> git push
```

如果你想在关键步骤确认：

```text
提交改动 --review
```

## 触发方式

| 你的需求 | 推荐说法 |
| --- | --- |
| 自动提交所有改动 | `提交改动` |
| 提交前先确认 | `提交改动 --review` |
| 提交并推送 | `提交代码并推送` |
| 只处理文档提交 | `提交改动 --type docs` |
| 指定 scope | `提交改动 --scope pptx` |
| 提交信息带 emoji | `提交改动，使用 emoji` |
| 只推送 | `推送` |

## 工作模式

| 模式 | 触发方式 | 适合场景 |
| --- | --- | --- |
| Auto | 默认 | 日常快速提交 |
| Review | `--review`、`审核模式` | 改动较大或你想确认文件范围 |

Auto 模式默认会暂存所有改动，包括未跟踪文件。Review 模式会在暂存、拆分、提交信息和推送等关键节点让你确认。

## 提交信息格式

默认使用 Conventional Commits：

```text
<type>[scope]: <subject>

<body>
```

示例：

```text
docs(readme): 优化 skill 使用说明
```

常见类型：

| 类型 | 适合改动 |
| --- | --- |
| `feat` | 新功能、新 skill、新脚本 |
| `fix` | Bug 修复 |
| `docs` | README、说明文档 |
| `refactor` | 不改变行为的重构 |
| `test` | 测试相关 |
| `chore` | 配置、维护、安装脚本 |
| `ci` | CI/CD 配置 |

## 自动拆分

改动较大时，AI 会考虑拆成多个语义清晰的提交：

| 条件 | 默认阈值 |
| --- | --- |
| 总改动行数 | 超过 300 行 |
| 涉及文件数 | 超过 20 个 |
| 顶层目录数 | 超过 5 个 |
| 改动类型 | 同时包含多种类型 |

如果你不想自动处理拆分，请使用：

```text
提交改动 --review
```

## 参数

| 参数 | 作用 |
| --- | --- |
| `--review` | 审核模式 |
| `--no-all` | 不自动 `git add -A` |
| `--no-untracked` | 不处理未跟踪文件 |
| `--type <type>` | 指定提交类型 |
| `--scope <name>` | 指定 scope |
| `--emoji` | 提交信息加 emoji |
| `--no-verify` | 跳过 hooks，仅在你明确要求时使用 |

## 安全边界

- 不会执行 `git push --force`。
- 不会执行 `git reset --hard`。
- 不会擅自修改 Git 配置。
- 不会在 `user.name` / `user.email` 缺失时强行提交。
- 在 `main` / `master` 上提交时会提醒你。

## 常见问题

### 会不会提交不该提交的文件？

默认会执行 `git add -A`，所以未跟踪文件也会被包含。想更谨慎就用：

```text
提交改动 --review
```

### 可以只提交部分文件吗？

可以，在请求里写清范围：

```text
只提交 pptx 和 README 相关改动
```

### 提交失败怎么办？

AI 会读取错误信息。如果是 hooks 或测试失败，会先说明失败原因，再根据情况修复或提示你处理。
