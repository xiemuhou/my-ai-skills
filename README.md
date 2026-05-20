# My AI Skills

个人 Claude Code Skills 集合，让 AI 助手自动完成 Git 提交等常见开发任务。

## 快速开始

### 安装（推荐：远程安装，无需克隆仓库）

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/xiemuhou/my-ai-skills/main/install/install.py | python3

# Windows PowerShell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/xiemuhou/my-ai-skills/main/install/install.py" -OutFile "$env:TEMP\xmh-install.py"; python "$env:TEMP\xmh-install.py"
```

### 安装（本地安装）

```powershell
# 克隆仓库
git clone https://github.com/xiemuhou/my-ai-skills.git
cd my-ai-skills

# 安装所有 skills 到系统级目录
python install-xmh-skills/scripts/install.py
```

也可以让 AI 帮你安装 — 在 Claude Code 中直接说：

```
安装 skills
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

### install-xmh-skills — Skills 安装器

将仓库中的 skills 复制安装到 `~/.codex/skills/` 和 `~/.claude/skills/`，使 skills 全局可用。

**触发方式：**

| 你说的话 | 效果 |
|----------|------|
| `安装skills` `安装技能` | 安装所有 skills 到两个平台 |
| `安装skills到claude` | 仅安装到 Claude Code |
| `更新skills` `强制安装skills` | 强制重新安装（忽略版本检测） |

**主要特性：**

- MD5 版本追踪，仅更新有变化的 skill
- 支持 Codex 和 Claude Code 双平台
- 支持预览模式 (`--dry-run`)
- 自动排除文档、测试、缓存等非核心文件

详细文档见 [install-xmh-skills/README.md](install-xmh-skills/README.md)

## 项目结构

```
my-ai-skills/
├── README.md                  ← 本文件
├── CLAUDE.md                  ← 项目级 AI 指令
├── git-commit/                ← Git 提交 skill
│   ├── SKILL.md               ← AI 执行规范
│   ├── README.md              ← 用户使用文档
│   └── config.yaml            ← 默认参数
└── install-xmh-skills/        ← Skills 安装器
    ├── SKILL.md               ← AI 执行规范
    ├── README.md              ← 用户使用文档
    └── scripts/
        └── install.py         ← 安装脚本
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
