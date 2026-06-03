# blog-notes — Markdown 学习笔记 Skill

`blog-notes` 用来生成适合长期查阅的 Markdown 学习笔记。它会把学习内容整理成“前言-主体-总结”的结构，并在文件开头写入 YAML Front Matter。

## 快速开始

```text
请使用 Blog-Notes skill 生成一篇 Markdown 学习笔记
主题：我今天学到的 Prompt Engineering 基础
内容：提示词要明确角色、任务、上下文、输出格式；复杂任务要拆步骤；需要给模型示例。
```

## 输出结构

生成的 `.md` 文件默认是：

```markdown
---
category: [AI]
tag: [prompt]
status: publish
---

# 前言

...

# 主体

...

# 总结

...
```

## 参数说明

| 参数 | 生成方式 | 说明 |
|------|----------|------|
| `category` | AI 根据文章内容推断 | 文章分类，最多 2 个词语 |
| `tag` | AI 根据文章内容提取 | 内容标签，最多 2 个词语 |
| `status` | `publish` | 发布状态 |
| `filename` | AI 自动根据内容生成，或使用用户自定义文件名 | 保存的 Markdown 文件名 |

## 常用说法

| 你的需求 | 推荐说法 |
| --- | --- |
| 记录学习内容 | `写一篇 Blog-Notes，内容是...` |
| 整理课程笔记 | `把这些课程内容整理成 Markdown 笔记` |
| 记录技术知识点 | `生成技术学习笔记，主题是...` |
| 指定分类标签 | `生成笔记 --category AI --tag prompt,codex` |
| 指定文件名 | `生成笔记 --filename prompt-engineering-notes.md` |

## 写作风格

- 前言说明这篇笔记为什么值得记录。
- 主体按知识点分层，避免流水账。
- 总结提炼 takeaway 和后续行动。
- 保留关键术语、命令、代码和示例。
- 不虚构来源、日期、作者或链接。

## 示例

```text
请使用 Blog-Notes skill 生成 Markdown 笔记
主题：Git rebase 的使用场景
内容：
- rebase 可以整理提交历史
- 公共分支不要随便 rebase
- 解决冲突后使用 git rebase --continue
--category Git
--tag rebase,workflow
--filename git-rebase-notes.md
```

## 适合记录什么

| 类型 | 示例 |
| --- | --- |
| 概念学习 | 什么是向量数据库 |
| 工具使用 | 如何配置 Python 虚拟环境 |
| 代码理解 | React hooks 的执行顺序 |
| 读书课程 | 一节课程的核心观点 |
| 问题复盘 | 一次 bug 的原因和解决方案 |

## 注意事项

- 默认 `status` 固定为 `publish`。
- `category` 和 `tag` 都控制在最多 2 个词语。
- 用户没有指定文件名时，AI 会根据内容自动生成。
- 正文不写文章名称；YAML 后直接从 `# 前言` 开始，后续标题层级整体相应提升。
- 如果文件已存在，默认不覆盖。
