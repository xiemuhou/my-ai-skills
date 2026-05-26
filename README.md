# My AI Skills

这是一个个人 Agent Skills 仓库，面向 OpenAI Codex 和 Claude Code 使用。它把常见开发工作沉淀成可复用的 skill，例如 Git 提交、项目初始化、网页文章保存、Release 发布和 skill 文档生成。

你可以把它理解为一组“给 AI 助手看的工作说明书”：安装后，在 Codex 或 Claude Code 里直接用自然语言说出需求，AI 会自动选择合适的 skill 执行。

## 快速开始

### 方式一：远程安装

适合只想使用 skills，不想克隆整个仓库的情况。

```powershell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/xiemuhou/my-ai-skills/main/install/install.py" -OutFile "$env:TEMP\xmh-install.py"
py "$env:TEMP\xmh-install.py"
```

macOS / Linux:

```bash
curl -fsSL https://raw.githubusercontent.com/xiemuhou/my-ai-skills/main/install/install.py | python3
```

### 方式二：本地安装

适合你要修改、开发或同步自己的 skills。

```powershell
git clone https://github.com/xiemuhou/my-ai-skills.git
cd my-ai-skills
python install-xmh-skills/scripts/install.py
```

安装目标：

| 平台 | 目录 |
| --- | --- |
| Codex | `~/.codex/skills/` |
| Claude Code | `~/.claude/skills/` |

## 怎么使用

安装后不用记命令，直接对 Codex 或 Claude Code 说自然语言即可：

```text
提交改动
```

```text
初始化项目
```

```text
把这个网页保存成 Markdown：https://example.com/article
```

```text
生成技能 README
```

如果你想指定 skill，也可以这样说：

```text
请使用 init-project skill 初始化当前项目
```

## 已有 Skills

| Skill | 适合做什么 | 常用说法 |
| --- | --- | --- |
| `git-commit` | 分析改动、生成 Conventional Commit、提交并推送 | `提交改动`、`commit`、`推送` |
| `install-xmh-skills` | 安装或更新本仓库 skills | `安装 skills`、`更新 skills` |
| `article-to-markdown` | 把网页文章保存为 Markdown | `保存文章 <url>`、`网页转 markdown` |
| `write-skill-readme` | 为 skill 生成用户友好的 README | `生成技能 README`、`更新技能文档` |
| `git-publish-release` | 生成 Release Notes 并发布 GitHub Release | `发布项目到 GitHub`、`创建 GitHub Release` |
| `init-project` | 生成 AGENTS.md、CLAUDE.md、README、CHANGELOG 等项目指令文件 | `初始化项目`、`生成 AGENTS.md` |

## 推荐工作流

更新本仓库和全局 skills：

```powershell
cd D:\my-ai-skills
git pull --ff-only origin main
python install-xmh-skills/scripts/install.py
```

开发或修改 skill：

```text
1. 修改对应 skill 目录下的 SKILL.md、README.md、config.yaml 或 scripts/
2. 运行 python install-xmh-skills/scripts/install.py --dry-run 预览安装
3. 运行 python install-xmh-skills/scripts/install.py 安装到全局目录
4. 使用 git-commit skill 提交改动
```

## 项目结构

```text
my-ai-skills/
├── README.md
├── AGENTS.md
├── CLAUDE.md
├── install/
│   └── install.py
├── install-xmh-skills/
│   ├── SKILL.md
│   ├── README.md
│   └── scripts/install.py
├── git-commit/
├── article-to-markdown/
├── write-skill-readme/
├── git-publish-release/
└── init-project/
```

每个 skill 至少包含：

```text
skill-name/
├── SKILL.md      # AI 执行规范，必须
├── README.md     # 用户使用文档，推荐
└── config.yaml   # 默认参数，可选
```

## 安装参数

| 参数 | 作用 |
| --- | --- |
| `--codex` | 只安装到 `~/.codex/skills/` |
| `--claude` | 只安装到 `~/.claude/skills/` |
| `--force` | 忽略 MD5，强制重装 |
| `--dry-run` | 只预览，不写入文件 |
| `--source <path>` | 指定 skills 源目录 |

## 常见问题

### 安装后为什么 Codex 里看不到项目子文件？

项目源码在 `D:\my-ai-skills`，安装后的全局 skills 在 `C:\Users\<你>\.codex\skills`。Codex 是否显示源码文件，取决于当前打开的 workspace；skill 是否可用，则取决于全局安装目录。

### 我应该修改源码目录还是全局安装目录？

修改 `D:\my-ai-skills` 里的源码目录。改完后重新运行安装脚本，把最新版本同步到全局 skills 目录。

### README 和 SKILL.md 有什么区别？

`README.md` 面向人，告诉你怎么用。`SKILL.md` 面向 AI，告诉 Codex 或 Claude Code 如何执行任务。

## License

MIT
