# git-commit — Git 提交自动化

`git-commit` 帮你把“检查改动、暂存文件、生成提交信息、提交、推送”这一整套 Git 流程交给 AI 处理。它适合日常开发中快速、规范地提交代码。

## 快速开始

在 Git 仓库里直接说：

```text
提交改动
```

AI 会自动完成：

```text
分析工作区 -> 判断是否需要拆分提交 -> git add -A -> 生成 Conventional Commit -> git commit -> git push
```

如果你想在关键步骤确认：

```text
提交改动 --review
```

## 适合场景

| 你的需求 | 推荐说法 |
| --- | --- |
| 自动提交当前所有改动 | `提交改动` |
| 只想提交但先审核 | `提交改动 --review` |
| 提交并推送 | `提交代码并推送` |
| 只推送当前分支 | `推送` |
| 提交信息带 emoji | `提交改动，使用 emoji` |
| 指定提交类型 | `提交改动 --type docs` |
| 指定 scope | `提交改动 --scope init-project` |

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
| `docs` | README、说明文档、注释文档 |
| `refactor` | 不改变行为的代码重构 |
| `test` | 测试相关 |
| `chore` | 配置、维护、安装脚本等 |
| `ci` | CI/CD 配置 |

## 自动拆分规则

当改动较大时，AI 会考虑拆成多个语义清晰的提交：

| 条件 | 说明 |
| --- | --- |
| 行数较多 | 总改动超过约 300 行 |
| 文件较多 | 涉及超过约 20 个文件 |
| 跨模块 | 涉及多个顶层目录 |
| 类型混合 | 例如同时有功能、文档、配置改动 |

如果你不想自动拆分，用审核模式：

```text
提交改动 --review
```

## 参数速查

| 参数 | 作用 |
| --- | --- |
| `--review` | 审核模式，关键节点先询问 |
| `--no-all` | 不自动 `git add -A` |
| `--no-untracked` | 不处理未跟踪文件 |
| `--type <type>` | 指定提交类型 |
| `--scope <name>` | 指定 scope |
| `--emoji` | 提交信息加 emoji |
| `--no-verify` | 跳过 hooks，仅在你明确要求时使用 |

## 安全边界

这个 skill 默认不会执行危险操作：

- 不会 `git push --force`
- 不会 `git reset --hard`
- 不会修改 Git 配置
- 不会在没有 `user.name` / `user.email` 时强行提交
- 在 `main` / `master` 上提交时会提醒你

## 常见问题

### 会不会把不该提交的文件也提交？

默认会执行 `git add -A`，因此会包含未跟踪文件。提交前 AI 会先分析改动。如果你想更谨慎，使用：

```text
提交改动 --review
```

### 提交后不满意怎么办？

如果还没有推送，可以手动调整 Git 历史。如果已经推送，建议新建修正提交，避免改写远程历史。

### 能只提交部分文件吗？

可以在请求里明确文件范围：

```text
只提交 README.md 和 install-xmh-skills 相关改动
```
