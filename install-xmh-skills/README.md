# install-xmh-skills — Skills 安装器

`install-xmh-skills` 用来把当前仓库里的 skills 安装到全局目录，让 Codex 和 Claude Code 都能直接触发使用。

它会扫描仓库根目录下所有包含 `SKILL.md` 的子目录，并用 MD5 判断哪些 skill 发生了变化，只安装需要更新的部分。

## 快速开始

在仓库根目录运行：

```powershell
python install-xmh-skills/scripts/install.py
```

或者在 Codex / Claude Code 里直接说：

```text
安装 skills
```

默认会安装到两个目录：

| 平台 | 安装目录 |
| --- | --- |
| Codex | `~/.codex/skills/` |
| Claude Code | `~/.claude/skills/` |

## 常用命令

| 需求 | 命令 |
| --- | --- |
| 安装到两个平台 | `python install-xmh-skills/scripts/install.py` |
| 只安装到 Codex | `python install-xmh-skills/scripts/install.py --codex` |
| 只安装到 Claude Code | `python install-xmh-skills/scripts/install.py --claude` |
| 强制重装全部 skills | `python install-xmh-skills/scripts/install.py --force` |
| 只预览安装结果 | `python install-xmh-skills/scripts/install.py --dry-run` |
| 指定源目录 | `python install-xmh-skills/scripts/install.py --source D:\my-ai-skills` |

## 自然语言用法

| 你说 | AI 会做什么 |
| --- | --- |
| `安装 skills` | 安装或更新所有 skills |
| `更新 skills` | 通常会使用 `--force` 强制重装 |
| `预览安装 skills` | 使用 `--dry-run` 查看会安装什么 |
| `只安装到 Codex` | 使用 `--codex` |
| `只安装到 Claude` | 使用 `--claude` |

## 安装规则

安装器会复制 skill 的核心文件，但跳过不需要进入运行环境的内容：

| 会安装 | 会跳过 |
| --- | --- |
| `SKILL.md` | 根级 `README.md` |
| `config.yaml` | 根级 `CHANGELOG.md` |
| `scripts/` | `tests/`、`test/` |
| `references/` | `plans/` |
| `assets/` | 隐藏文件、缓存文件、`*.pyc` |

安装器还会跳过根级 `SKILL.yaml` / `SKILL.yml`，避免同一个 skill 出现重复入口。

## 版本判断

每个安装后的 skill 都会写入 manifest：

```text
.skill-manifest.codex.json
.skill-manifest.claude.json
```

如果源目录内容的 MD5 没变，安装器会跳过该 skill。这样重复运行安装命令也很快。

## 推荐工作流

更新 GitHub 最新版本并安装：

```powershell
cd D:\my-ai-skills
git pull --ff-only origin main
python install-xmh-skills/scripts/install.py
```

修改 skill 后本地验证：

```powershell
python install-xmh-skills/scripts/install.py --dry-run
python install-xmh-skills/scripts/install.py
```

## 常见问题

### 为什么 README.md 没有安装到全局 skill 目录？

README 面向人阅读，运行时 AI 主要读取 `SKILL.md`。安装器会跳过 README，避免全局 skill 包过大。

### 为什么某些 skill 显示“跳过”？

表示这个 skill 和上次安装的内容一致，不需要重复复制。

### 可以只给 Codex 安装吗？

可以：

```powershell
python install-xmh-skills/scripts/install.py --codex
```
