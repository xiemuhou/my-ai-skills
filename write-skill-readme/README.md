# write-skill-readme — Skill README 写作助手

本 README 面向使用者：如何触发并正确使用 `write-skill-readme` skill。执行细节和写作规范在 `SKILL.md`。

`write-skill-readme` 用来为 Agent Skills 编写面向用户的 README。它会读取目标 skill 的 `SKILL.md`、`config.yaml`、`scripts/` 和 `references/`，把执行规范整理成清晰、可复制、容易上手的使用文档。

## 快速开始

```text
请使用 write-skill-readme skill 为 git-commit 生成 README.md
输入：git-commit skill 目录
输出：git-commit/README.md
```

优化已有文档：

```text
请优化 git-publish-release 的 README.md
目标：让读者 1 分钟内理解它能做什么、怎么触发、发布前要准备什么。
```

## 触发方式

| 你的需求 | 推荐说法 |
| --- | --- |
| 给新 skill 写 README | `为 <skill> 生成 README.md` |
| 优化已有 README | `优化 <skill> 的 README，让用户更容易理解` |
| 批量优化 | `优化所有 skill 的 README 文档` |
| 面向小白用户 | `把这个 README 写得更适合第一次使用的人` |
| 只改 README | `只更新 README，不修改 SKILL.md` |

## 它会读取什么

| 文件或目录 | 用途 |
| --- | --- |
| `SKILL.md` | 理解触发条件、执行流程、安全边界 |
| `config.yaml` | 提取默认参数和可配置项 |
| `scripts/` | 提取脚本入口和命令行参数 |
| `references/` | 提取模板、策略或领域说明 |
| 现有 `README.md` | 保留有价值内容，重写不清晰部分 |

## 推荐 README 结构

通常会生成下面的结构：

```text
标题
一句话定位
快速开始
触发方式
输入输出
Prompt 示例
参数或配置说明
注意事项
常见问题
```

如果目标 skill 有脚本，会把命令行用法放在后面，作为备选用法；自然语言 Prompt 仍然优先。

## 示例

为单个 skill 生成：

```text
请使用 write-skill-readme skill 为 init-project 生成 README.md
要求：面向第一次使用的人，先给最常用 Prompt，再说明参数。
```

批量优化：

```text
请优化当前仓库所有 skill 的 README.md
要求：统一结构，突出自然语言用法，避免堆砌内部执行细节。
```

保留部分内容：

```text
优化 pptx 的 README.md，但保留“品牌 Logo”和“代码页规则”这两个章节。
```

## 写作原则

- 先讲怎么用，再讲工作原理。
- Prompt 示例要能直接复制。
- 技术细节只保留对使用者有帮助的部分。
- 不把 README 写成 `SKILL.md` 的重复版本。
- 对危险操作、安全边界和输出文件说清楚。
- 有脚本时，说明脚本是备选入口。

## 安全边界

默认只修改目标 skill 的 `README.md`。除非你明确要求，不修改：

- `SKILL.md`
- `config.yaml`
- `scripts/`
- `references/`
- 模板和资源文件

## 常见问题

### README 是否需要覆盖全部参数？

不需要。README 覆盖高频用法和关键风险即可，完整执行细节留给 `SKILL.md`。

### 可以保留我手写的内容吗？

可以。你可以明确说：

```text
优化 README，但保留“设计理念”和“FAQ”里的原有内容
```

### README 要不要写得很长？

不建议。好的 README 应该让读者快速开始，然后在需要时查到参数、输出和注意事项。
