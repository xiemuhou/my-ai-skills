---
name: install-xmh-skills
description: 将当前仓库的 skills 复制安装到 ~/.codex/skills/ 和 ~/.claude/skills/，使 skills 全局可用
metadata:
  type: skill
  trigger:
    - "安装skills" "安装技能" "install skills"
    - "更新skills" "更新技能" "update skills"
    - "/install-xmh-skills"
  os: [windows, linux, macos]
  shell: [powershell, bash]
---

# Install XMH Skills — 执行规范

## 核心原则

1. **复制安装**: 将 skill 目录复制到系统级目录，不使用软链接（兼容性更好）
2. **MD5 版本追踪**: 通过 `.skill-manifest.{codex,claude}.json` 追踪已安装版本，仅更新有变化的 skill
3. **双平台支持**: 默认同时安装到 Codex (`~/.codex/skills/`) 和 Claude Code (`~/.claude/skills/`)

---

## 触发方式

用户通过以下方式触发安装：

| 触发词 | 效果 |
|--------|------|
| `安装skills` / `安装技能` | 默认：同时安装到 Codex 和 Claude Code |
| `安装skills到codex` | 仅安装到 `~/.codex/skills/` |
| `安装skills到claude` | 仅安装到 `~/.claude/skills/` |
| `更新skills` / `更新技能` | 强制重新安装所有 skill（`--force`） |

---

## 执行流程

### 阶段 1: 定位安装脚本

找到当前仓库中的安装脚本。优先使用远程安装器（无需克隆仓库），本地安装器作为备选：

| 场景 | 脚本路径 |
|------|----------|
| 远程安装（推荐） | `https://raw.githubusercontent.com/xiemuhou/my-ai-skills/main/install/install.py` |
| 本地安装 | `<repo-root>/install-xmh-skills/scripts/install.py` |

**如果用户还未克隆仓库**，指导用户使用远程安装：

```bash
# macOS / Linux
curl -fsSL https://raw.githubusercontent.com/xiemuhou/my-ai-skills/main/install/install.py | python3

# Windows PowerShell
Invoke-WebRequest -Uri "https://raw.githubusercontent.com/xiemuhou/my-ai-skills/main/install/install.py" -OutFile "$env:TEMP\xmh-install.py"; python "$env:TEMP\xmh-install.py"
```

### 阶段 2: 解析用户意图

| 用户表述 | 对应参数 |
|----------|----------|
| 默认（无特殊说明） | 无额外参数 → 同时安装到两个平台 |
| "codex" / "仅codex" | `--codex` |
| "claude" / "仅claude" | `--claude` |
| "强制" / "更新" / "重装" | `--force` |
| "预览" / "看看" / "dry-run" | `--dry-run` |

### 阶段 3: 执行安装

根据解析的参数，运行安装命令：

```bash
python3 "<repo-root>/install-xmh-skills/scripts/install.py" [参数...]
```

**Windows (PowerShell)**:
```powershell
python "$env:USERPROFILE\my-ai-skills\install-xmh-skills\scripts\install.py" --codex --claude
```

### 阶段 4: 展示结果

安装完成后，向用户展示：
- 安装了哪些 skill
- 跳过了哪些 skill（版本未变化）
- 安装目标路径

---

## 参数速查

| 参数 | 效果 |
|------|------|
| `--codex` | 仅安装到 `~/.codex/skills/` |
| `--claude` | 仅安装到 `~/.claude/skills/` |
| `--force` | 强制重新安装（忽略 MD5 比较） |
| `--dry-run` | 预览模式，只显示将要执行的操作 |
| `--source <path>` | 指定 skills 源目录（默认自动检测） |

---

## 重要约束

1. **安装脚本在 `install-xmh-skills/scripts/install.py`**，不要移动
2. 安装过程不删除用户自定义文件，只替换同名 skill 目录
3. 默认跳过 `README.md`、`tests/`、`plans/`、隐藏文件（`.` 开头）等非核心文件
4. 不在 `main`/`master` 分支上不会阻止安装，但提醒用户
