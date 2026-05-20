# My AI Skills

个人 Claude Code Skills 集合，让 AI 助手自动完成 Git 提交等常见开发任务。

## 快速开始

### 安装

将仓库克隆到本地，然后把 skills 目录链接到 Claude Code 的 skills 路径：

```powershell
# 克隆仓库
git clone https://github.com/xiemuhou/my-ai-skills.git

# 创建符号链接（Windows PowerShell，需管理员权限）
New-Item -ItemType SymbolicLink -Path "$env:USERPROFILE\.claude\skills" -Target "D:\my-ai-skills\.claude\skills"
```

或者直接复制 skills 目录：

```powershell
# 复制整个 skills 目录
Copy-Item -Recurse "D:\my-ai-skills\.claude\skills" "$env:USERPROFILE\.claude\skills"
```

### 使用

安装后，在 Claude Code 中直接用自然语言触发：

```
提交 Git 改动
```

AI 会自动：分析改动 → 暂存文件 → 生成 conventional commit 信息 → 提交 → 推送。

## 已有 Skills

### git-commit — 自动化 Git 提交

自动分析工作区改动，生成符合 [Conventional Commits](https://www.conventionalcommits.org/) 规范的提交信息，智能拆分为多个语义清晰的提交，并推送到 GitHub。

**触发方式：**

| 你说的话 | 效果 |
|----------|------|
| `提交改动` `commit` `git commit` | 自动模式，全流程自动完成 |
| `提交改动，审核模式` `commit --review` | 审核模式，关键节点暂停确认 |
| `提交代码，使用 emoji` | 提交信息带 emoji 前缀 |
| `推送` `push` | 推送到远程仓库 |

**主要特性：**

- 自动识别改动类型（feat / fix / docs / refactor / ...）
- 大改动智能拆分为多个提交（行数 > 300 / 文件 > 20 / 跨模块）
- 支持自动模式和审核模式
- 提交信息中文/英文自适应
- 默认推送到远程仓库

详细文档见 [git-commit/README.md](git-commit/README.md)

## 项目结构

```
my-ai-skills/
├── README.md               ← 本文件
├── CLAUDE.md               ← 项目级 AI 指令
├── .claude/
│   └── skills/             ← Claude Code 自动发现 skills
│       ├── git-commit/     ← Git 提交 skill
│       │   ├── SKILL.md    ← AI 执行规范
│       │   ├── README.md   ← 用户使用文档
│       │   └── config.yaml ← 默认参数
│       └── <future-skills>/
└── git-commit/             ← 源文件（同上）
    ├── SKILL.md
    ├── README.md
    └── config.yaml
```

## 开发新 Skill

### 最小结构

每个 skill 是一个目录，必须包含 `SKILL.md`：

```
my-skill/
├── SKILL.md     ← 必须：AI 执行规范（含 YAML frontmatter）
├── README.md    ← 可选：用户使用文档
└── config.yaml  ← 可选：默认参数
```

### SKILL.md 模板

```markdown
---
name: my-skill
description: 一句话描述这个 skill 做什么
metadata:
  type: skill
  trigger:
    - "触发词1"
    - "触发词2"
---

# My Skill — 执行规范

## 核心原则
...

## 执行流程
...
```

### Skill 规范

1. **frontmatter 必填**：`name`、`description`、`trigger` 列表
2. **执行规范完整**：AI 需要足够的信息来自动完成全部步骤
3. **安全约束明确**：列出所有禁止操作
4. **错误处理**：覆盖常见异常场景的处理方式

## 技术栈

- 平台：Windows + VSCode + Claude Code 扩展
- Skills 标准：Claude Code Skills 格式（基于 Agent Skills 开放标准）
- 托管：GitHub

## License

MIT
