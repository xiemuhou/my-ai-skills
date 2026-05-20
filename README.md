# My AI Skills

个人 Claude Code Skills 集合，覆盖 Git 提交自动化、GitHub Release 发布、网页文章保存、技能文档生成等常见任务。

## 前置条件

- **Python 3.x**（[python.org](https://python.org) 下载安装）
- **Git**（[git-scm.com](https://git-scm.com) 下载安装）

> Windows 用户注意：务必从 [python.org](https://python.org) 安装 Python，不要使用 Microsoft Store 版本。安装时勾选 "Add Python to PATH"。安装后可使用系统自带的 `py` 启动器代替 `python` 命令，避免与 Windows 自带的商店跳转器冲突。

## 快速开始

### 安装（推荐：远程安装，无需克隆仓库）

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/xiemuhou/my-ai-skills/main/install/install.py | python3

# Windows PowerShell（使用 py 启动器）
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/xiemuhou/my-ai-skills/main/install/install.py" -OutFile "$env:TEMP\xmh-install.py"; py "$env:TEMP\xmh-install.py"
```

### 安装（本地安装）

```powershell
# 克隆仓库
git clone https://github.com/xiemuhou/my-ai-skills.git
cd my-ai-skills

# 安装所有 skills 到系统级目录（Windows 使用 py，macOS/Linux 使用 python3）
py install-xmh-skills/scripts/install.py
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

### article-to-markdown — 网页文章保存

将网页文章保存为本地 Markdown 文件，AI 根据内容自动生成 YAML Front Matter 元数据。

**触发方式：**

| 你说的话 | 效果 |
|----------|------|
| `保存文章 <url>` `article to markdown` | 获取网页，保存为 .md 文件 |
| `保存网页 <url> --category 技术 --tag python` | 手动指定分类和标签 |
| `保存文章 <url> --path D:\笔记` | 指定保存目录 |

**主要特性：**

- AI 自动推断 category 和 tag（各不超过 2 个词语）
- 原样保存正文，图片使用原始链接
- 自动移除文章来源、更新时间、页脚推广
- 标题用于文件名，不出现在正文中

详细文档见 [article-to-markdown/README.md](article-to-markdown/README.md)

### write-skill-readme — 技能文档生成

自动分析 Skill 结构，为 Agent Skills 生成小白友好的 README.md 使用指南。

**触发方式：**

| 你说的话 | 效果 |
|----------|------|
| `生成技能 README` `编写用户指南` | 分析 SKILL.md 并生成文档 |
| `更新技能文档` | 更新已有 README |

**主要特性：**

- 自动解析 SKILL.md 提取触发词、参数、流程
- 按模板生成结构化用户文档
- 支持 config.yaml 参数说明

详细文档见 [write-skill-readme/README.md](write-skill-readme/README.md)

### git-publish-release — GitHub Release 发布

智能分析 tag 间历史变化，自动生成 Release Notes 并创建 GitHub Release。

**触发方式：**

| 你说的话 | 效果 |
|----------|------|
| `发布项目到 GitHub` `创建 GitHub Release` | 自动分析变更并发布 |
| `生成 Release Notes` | 仅生成 Release Notes |
| `发布 v1.0.0` | 指定版本号发布 |

**主要特性：**

- 自动分析 tag 间 commit 差异
- 按 Conventional Commits 分类生成 Release Notes
- 支持首次发布、常规版本、预发布版本（alpha/beta/rc）
- 自动识别 prerelease 标记

详细文档见 [git-publish-release/README.md](git-publish-release/README.md)

## 项目结构

```
my-ai-skills/
├── README.md                  ← 本文件
├── CLAUDE.md                  ← 项目级 AI 指令
├── git-commit/                ← Git 提交 skill
│   ├── SKILL.md               ← AI 执行规范
│   ├── README.md              ← 用户使用文档
│   └── config.yaml            ← 默认参数
├── install-xmh-skills/        ← Skills 安装器
│   ├── SKILL.md               ← AI 执行规范
│   ├── README.md              ← 用户使用文档
│   └── scripts/
│       └── install.py         ← 安装脚本
├── article-to-markdown/       ← 网页文章保存 skill
│   ├── SKILL.md               ← AI 执行规范
│   └── README.md              ← 用户使用文档
├── write-skill-readme/        ← 技能文档生成 skill
│   ├── SKILL.md               ← AI 执行规范
│   └── references/            ← 参考模板
└── git-publish-release/       ← GitHub Release 发布 skill
    ├── SKILL.md               ← AI 执行规范
    ├── README.md              ← 用户使用文档
    ├── scripts/               ← 辅助脚本
    └── references/            ← 参考模板
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
