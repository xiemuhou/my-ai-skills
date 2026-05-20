---
name: git-commit
description: 自动化 Git 提交流程 — 分析改动、生成 conventional commit 信息、提交并可选推送
metadata:
  type: skill
  trigger:
    - 用户说"提交"、"commit"、"git commit"、"提交改动"、"提交代码"
    - 用户说"推送"、"push"
    - 用户执行 /git-commit
  os: [windows, linux, macos]
  shell: [powershell, bash]
---

# Git Commit Skill — 执行规范

## 核心原则

1. **安全第一**: 绝不执行破坏性操作（force push、hard reset 等），除非用户明确要求
2. **默认自动**: 自动分析、暂存、拆分、提交，减少用户交互
3. **conventional commits**: 严格遵循 Conventional Commits 规范生成提交信息
4. **智能拆分**: 大改动自动拆分为多个语义清晰的提交

---

## 工作模式

### Auto 模式（默认）

用户触发后，AI 自主完成全流程，无需确认。设计理念：提交的顺畅度高于内容完美度，不满意可 `git reset` 回滚。

### Review 模式

用户触发时加入 `--review`、`审核模式`、`review` 等关键词。在关键决策点暂停，等待用户确认：
- 暂存方式选择
- 大改动拆分方案
- 提交信息确认
- 是否推送

---

## 执行流程

### 阶段 1: 环境检查

1. 确认当前在 Git 仓库中
2. 检查当前分支，若在 `main`/`master` 上直接提交则警告
3. 检查工作区状态，若无改动则退出

### 阶段 2: 改动分析

执行 `git status`, `git diff --stat`, `git diff` 获取：
- 修改、新增、删除的文件列表及行数统计
- 未跟踪文件列表
- 具体改动内容

分析要点：
- 改动涉及的功能模块
- 改动类型（feat/fix/docs/style/refactor/perf/test/chore/ci/revert）
- 改动规模（文件数、行数）

### 阶段 3: 拆分判断

触发拆分的条件（满足任一即拆分）：

| 条件 | 阈值 |
|------|------|
| 总改动行数 | > 300 行 |
| 涉及文件数 | > 20 个 |
| 跨模块 | 涉及 > 5 个顶层目录 |
| 混合类型 | 包含 2+ 种不同提交类型 |
| 独立功能 | 涉及 2+ 个不相关的功能模块 |

拆分策略：
- 按功能模块分组
- 每组的提交类型独立判断
- 每组生成独立的提交信息
- 按逻辑依赖顺序执行提交

### 阶段 4: 暂存文件

Auto 模式：
- `git add -A` 暂存所有改动（包括未跟踪文件）
- 用户可通过 `--no-all` 跳过自动暂存
- 用户可通过 `--no-untracked` 跳过未跟踪文件

Review 模式：
- 展示改动清单，让用户选择暂存方式
- 支持手动指定文件范围

### 阶段 5: 生成提交信息

格式遵循 Conventional Commits：

```
<type>[<scope>]: <subject>

<body>
```

**类型判断规则**：

| 类型 | 判断依据 |
|------|----------|
| `feat` | 新增文件/函数/功能、新页面/组件 |
| `fix` | 修复 bug、修正逻辑错误 |
| `docs` | 仅修改 .md/.txt 等文档文件 |
| `style` | 仅格式调整（空格、缩进、分号等） |
| `refactor` | 代码重构，无功能变化 |
| `perf` | 性能优化相关改动 |
| `test` | 仅测试文件改动 |
| `chore` | 配置文件、依赖更新、构建脚本 |
| `ci` | CI/CD 相关文件 |
| `revert` | 回滚之前的提交 |

**scope 推断**：
- 从修改文件的最上层目录名推断
- 多个目录时取最相关的那个
- 不确定时可省略 scope

**subject 规则**：
- 中文提交信息：< 72 字符
- 英文提交信息：< 72 字符
- 使用祈使句（"添加"而非"添加了"）
- 不加句号结尾

**body 规则**（可选，大改动时推荐）：
- 每行说明一个关键改动
- 最多 10 行，每项最多 3 条
- 说明改动的 WHAT 和 WHY

**语言选择**：
- 检查最近 5 条提交的语言，保持一致
- 用户可指定语言偏好

**Emoji**：
- 用户要求 emoji 时，在 subject 前加对应 emoji
- 类型-emoji 映射见 config.yaml

### 阶段 6: 执行提交

```bash
git commit -m "<生成的提交信息>"
```

- 不跳过 git hooks（除非用户要求 `--no-verify`）
- 不支持 `--amend`（除非用户明确要求且分支未推送）
- 若提交失败，分析错误原因并修复

### 阶段 7: 推送

Auto 模式：
- 默认推送到远程
- `git push origin <current-branch>`

Review 模式：
- 询问用户是否推送

推送安全规则：
- 绝不 force push
- 若远程有新提交，先 `git pull --rebase`
- 推送失败时报告具体错误

---

## 参数速查

| 参数 | 效果 |
|------|------|
| `--review` / `审核模式` | 启用审核模式 |
| `--no-all` | 跳过自动暂存 |
| `--no-untracked` | 不处理未跟踪文件 |
| `--no-verify` | 跳过 Git hooks |
| `--amend` | 修改上一次提交 |
| `--signoff` | 添加 Signed-off-by |
| `--emoji` / `使用 emoji` | 提交信息包含 emoji |
| `--scope <name>` | 指定 scope |
| `--type <type>` | 强制指定提交类型 |

---

## 输出格式

提交完成后输出：

```
✅ 提交完成
📦 类型: feat
📍 Scope: skills
📝 信息: feat(skills): 添加 git-commit 技能
📁 文件: 3 files changed, 120 insertions(+)
🌿 分支: main
⬆️  已推送到 origin/main
```

多个提交时按执行顺序逐个展示。

---

## 错误处理

| 场景 | 处理方式 |
|------|----------|
| 工作区干净，无改动 | 提示"没有需要提交的改动"并退出 |
| 不在 Git 仓库中 | 提示"当前目录不是 Git 仓库"并退出 |
| 提交失败（hooks） | 展示错误信息，建议修复或使用 --no-verify |
| 推送冲突 | 执行 git pull --rebase 后重试推送 |
| 有未合并的冲突 | 提示用户手动解决冲突 |
| 在 main 分支上提交 | 警告用户确认 |

---

## 重要约束

1. **绝不** 执行 `git push --force` 或 `git push -f`
2. **绝不** 执行 `git reset --hard` 除非用户明确要求
3. **绝不** 跳过 hooks 除非用户要求 `--no-verify`
4. **绝不** 在 user.email/user.name 未配置时提交（先检查）
5. **绝不** 修改 git config
