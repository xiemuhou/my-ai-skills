# Install XMH Skills

将当前仓库的 skills 复制安装到系统级目录，使 skills 在任意项目中全局可用。

## 快速开始

### 远程安装（推荐，无需克隆仓库）

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/xiemuhou/my-ai-skills/main/install/install.py | python3

# Windows PowerShell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/xiemuhou/my-ai-skills/main/install/install.py" -OutFile "$env:TEMP\xmh-install.py"; python "$env:TEMP\xmh-install.py"
```

### 通过 AI 触发

在 Claude Code 中直接说：

```
安装 skills
```

AI 会自动找到并运行安装脚本，将 skills 安装到 `~/.codex/skills/` 和 `~/.claude/skills/`。

### 本地安装（已克隆仓库）

```powershell
python install-xmh-skills/scripts/install.py           # 默认：两个平台
python install-xmh-skills/scripts/install.py --claude  # 仅 Claude Code
python install-xmh-skills/scripts/install.py --codex   # 仅 Codex
python install-xmh-skills/scripts/install.py --force   # 强制重装
python install-xmh-skills/scripts/install.py --dry-run # 预览
```

## 安装目标

| 平台 | 路径 |
|------|------|
| Codex | `~/.codex/skills/` |
| Claude Code | `~/.claude/skills/` |

## 工作原理

1. **扫描** — 在仓库根目录扫描所有包含 `SKILL.md` 的子目录
2. **MD5 比较** — 计算每个 skill 的 MD5，与已安装版本对比
3. **复制** — 仅复制有变化的 skill（排除 `README.md`、`tests/`、隐藏文件等）
4. **记录** — 写入 `.skill-manifest.{codex,claude}.json` 记录版本信息

## 参数

| 参数 | 效果 |
|------|------|
| `--codex` | 仅安装到 `~/.codex/skills/` |
| `--claude` | 仅安装到 `~/.claude/skills/` |
| `--force` | 强制重新安装，忽略 MD5 版本比较 |
| `--dry-run` | 预览模式，显示将要执行的操作但不实际修改 |
| `--source <path>` | 指定 skills 源目录（默认自动检测） |

## 安装时忽略的文件

以下内容不会被复制到目标目录：

- `README.md`、`CHANGELOG.md`（根级文档）
- `tests/`、`plans/` 目录
- 隐藏文件（`.` 开头）
- `__pycache__`、`.pytest_cache` 等缓存目录
- `*.pyc`、`*.pyo` 编译文件

## FAQ

**Q: 安装后如何验证？**
A: 检查目标目录是否存在对应 skill：
```powershell
ls ~/.claude/skills/git-commit/
```

**Q: 安装会覆盖我的自定义修改吗？**
A: 如果目标目录已存在同名 skill 且 MD5 不同，旧版本会被删除后重新复制。如想保留自定义版本，请先备份。

**Q: 如何卸载某个 skill？**
A: 直接删除目标目录即可：
```powershell
rm -r ~/.claude/skills/<skill-name>/
```

**Q: 为什么不用软链接？**
A: 复制安装兼容性更好，不依赖源仓库位置，且各平台行为一致。

## 文件说明

- `SKILL.md` — AI 执行规范
- `README.md` — 本文件，用户使用文档
- `scripts/install.py` — 安装脚本
