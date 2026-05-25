# init-project — 用户使用指南

本 README 面向**使用者**：如何触发并正确使用 `init-project` skill。
执行指令与硬性规范在 `SKILL.md`；默认参数在 `config.yaml`。

## 快速开始

### 常规用法（最小可用）

```text
请使用 init-project skill 为本项目进行初始化
输入：当前项目目录（自动分析）
输出：AGENTS.md、CLAUDE.md、README.md、CHANGELOG.md、.gitignore、docs/、docs/plans/
```

你也可以用更自然的方式：

```
初始化项目
创建项目指令文件
生成 AGENTS.md
```

### 进阶用法（带参数约束）

```text
初始化项目
另外，还有下列参数约束：
- --overwrite：完全覆盖现有文件
- --skip-readme：跳过 README 生成
- --only-readme：仅生成 README
```

## 设计理念

✨ **核心价值**：一键为新项目或现有项目补齐标准化的 AI 协作文档体系。自动检测项目类型，生成符合 AGENTS.md 社区标准的跨平台指令文件。

**工作原理**（简化版）：
1. 扫描项目目录，识别标志文件（`pyproject.toml` / `package.json` / `Cargo.toml` 等）
2. 自动检测项目类型、语言、目录结构
3. 从模板生成文档，替换占位符
4. 已存在的文件启用智能合并（保留你的自定义内容）

**设计哲学**：
- 📄 **AGENTS.md 唯一真相源** — 你只需维护这一个文件
- 🔗 **CLAUDE.md 自动引用** — 通过 `@./AGENTS.md` 自动同步，零维护
- 🧠 **智能合并** — 再次运行不会覆盖你的自定义内容
- 🌐 **跨平台兼容** — 支持 20+ AI 编码工具

## 使用示例

### 示例 1：全新项目初始化（最常用）

```
初始化项目
```

> AI 自动运行：检测项目类型 → 生成全部文档 → 补齐 docs/ 目录。

### 示例 2：现有项目补全文档

```
为当前项目补齐 AGENTS.md 和 CLAUDE.md
```

> 智能合并：保留你已自定义的项目目标和工作流，更新标准化部分。

### 示例 3：完全覆盖重新生成

```
初始化项目，使用 --overwrite 覆盖现有文件
```

## 输出文件

| 文件 | 用途 | 强制性 |
|------|------|--------|
| `AGENTS.md` | 跨平台通用项目指令（Single Source of Truth） | 必须 |
| `CLAUDE.md` | Claude Code 特定适配（`@./AGENTS.md` 引用） | 必须 |
| `README.md` | 项目介绍与使用方法 | 可选 |
| `CHANGELOG.md` | 项目变更记录（Keep a Changelog 格式） | 必须 |
| `.gitignore` | Git 忽略规则（安全优先） | 推荐 |
| `docs/` `docs/plans/` | 文档和计划目录 | 推荐 |

## 支持的项目类型

| 类型 | 检测依据 |
|------|----------|
| Python | `pyproject.toml`、`requirements.txt`、`setup.py` |
| Web | `package.json`、`yarn.lock`、`webpack.config.js` |
| Rust | `Cargo.toml`、`Cargo.lock` |
| Go | `go.mod`、`go.sum` |
| Java | `pom.xml`、`build.gradle` |
| 数据科学 | `*.ipynb`、`*.R`、`environment.yml` |
| 文档 | `docs/`、`mkdocs.yml`、`docusaurus.config.js` |
| 通用 | 未识别时回退 |

## ✨ 特性一览

- ✅ 完全自动化，无需手动输入信息
- ✅ 智能项目类型检测（7 种常见类型）
- ✅ 自动语言检测（zh-CN / en-US / ja-JP / ko-KR）
- ✅ 智能合并：保留自定义内容，更新标准化部分
- ✅ 零维护成本：修改 AGENTS.md 后 CLAUDE.md 自动生效
- ✅ 跨平台兼容：符合 AGENTS.md 标准，支持 20+ AI 工具
- ✅ 安全优先的 .gitignore（自动忽略 .env、密钥、证书）

## 备选用法（脚本/命令行）

### 完全自动化

```bash
python3 init-project/scripts/generate.py --auto
```

### 覆盖现有文件

```bash
python3 init-project/scripts/generate.py --auto --overwrite
```

### 仅生成特定文件

```bash
# 跳过 README
python3 init-project/scripts/generate.py --auto --skip-readme

# 仅生成 README
python3 init-project/scripts/generate.py --auto --only-readme
```

### 手动指定信息

```bash
python3 init-project/scripts/generate.py \
  --project-name "my-project" \
  --project-description "数据科学项目" \
  --workflow "数据获取 → 分析 → 可视化"
```

## 常见问题

### Q：AGENTS.md 和 CLAUDE.md 有什么区别？

A：AGENTS.md 是跨平台通用指令（支持 20+ AI 工具），你手动维护这一个文件即可。CLAUDE.md 通过 `@./AGENTS.md` 自动引用 AGENTS.md，加上少量 Claude Code 专属说明，无需单独维护。

### Q：再次运行会覆盖我之前的修改吗？

A：不会。技能默认启用智能合并模式——保留你自定义的项目目标、工作流、自定义章节；只更新工程原则、语言设置等标准化内容。除非你用了 `--overwrite`。

### Q：为什么 CHANGELOG.md 是强制性的？

A：项目管理的硬性要求。每次修改项目指令文件或项目结构时，都应记录变更，方便追溯和协作。

### Q：支持哪些项目类型？

A：Python、Web（Node.js）、Rust、Go、Java、数据科学、文档项目，以及通用模板（未识别时回退）。

### Q：脚本需要什么依赖？

A：Python 3.x + PyYAML（`pip install pyyaml`）。其余均为标准库。

### Q：生成的文件可以手动修改吗？

A：可以。AGENTS.md 就是设计来让你手动维护的。智能合并机制会保护你的自定义内容。
