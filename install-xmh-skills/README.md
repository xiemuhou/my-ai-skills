# install-xmh-skills — Skills 安装器

本 README 面向使用者：如何触发并正确使用 `install-xmh-skills` skill。执行细节和安装规则在 `SKILL.md` 与 `scripts/install.py`。

`install-xmh-skills` 用来把当前仓库里的 skills 安装到 Codex 和 Claude Code 的全局目录，让这些 skills 可以在任意项目中触发使用。

## 快速开始

在仓库根目录说：

```text
安装 skills
```

或直接运行：

```powershell
python install-xmh-skills/scripts/install.py
```

默认安装到：

| 平台 | 安装目录 |
| --- | --- |
| Codex | `~/.codex/skills/` |
| Claude Code | `~/.claude/skills/` |

## 触发方式

| 你的需求 | 推荐说法 |
| --- | --- |
| 安装到两个平台 | `安装 skills` |
| 更新已安装 skills | `更新 skills` |
| 强制重装 | `强制安装 skills` |
| 只安装 Codex | `只安装到 Codex` |
| 只安装 Claude | `只安装到 Claude` |
| 先预览 | `预览安装 skills` |

## 命令行用法

| 需求 | 命令 |
| --- | --- |
| 默认安装 | `python install-xmh-skills/scripts/install.py` |
| 只安装到 Codex | `python install-xmh-skills/scripts/install.py --codex` |
| 只安装到 Claude Code | `python install-xmh-skills/scripts/install.py --claude` |
| 强制重装 | `python install-xmh-skills/scripts/install.py --force` |
| 预览模式 | `python install-xmh-skills/scripts/install.py --dry-run` |
| 指定源目录 | `python install-xmh-skills/scripts/install.py --source D:\my-ai-skills` |

## 安装规则

安装器会扫描仓库根目录下所有包含 `SKILL.md` 的子目录。每个 skill 通过 MD5 判断是否变化，未变化的 skill 会跳过。

| 会复制 | 会跳过 |
| --- | --- |
| `SKILL.md` | skill 根目录下的 `README.md` |
| `config.yaml` | skill 根目录下的 `CHANGELOG.md` |
| `scripts/` | `tests/`、`test/` |
| `references/` | `plans/` |
| `assets/` | 隐藏文件、缓存文件、`*.pyc` |

README 是给人阅读的仓库文档，不会安装到全局运行目录。运行时 AI 主要读取 `SKILL.md`。

## 推荐工作流

从 GitHub 拉取最新版本并安装：

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

## 输出怎么看

安装完成后会显示：

| 状态 | 含义 |
| --- | --- |
| `已安装` | 源 skill 有变化，已经复制到目标目录 |
| `跳过` | MD5 未变化，不需要重复复制 |
| `失败` | 安装过程中出现错误，需要查看原因 |

## 常见问题

### 为什么 README.md 没有安装？

README 面向人阅读，运行时 AI 主要读取 `SKILL.md`。安装器会跳过 README，减少全局 skill 包体积和干扰。

### 为什么某些 skill 显示跳过？

表示这个 skill 和上次安装的内容一致，不需要重复复制。

### 可以只给 Codex 安装吗？

可以：

```powershell
python install-xmh-skills/scripts/install.py --codex
```
