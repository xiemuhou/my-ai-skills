# blog-notes — Markdown 学习笔记

本 README 面向使用者：如何触发并正确使用 `blog-notes` skill。执行细节和默认参数在 `SKILL.md` 与 `config.yaml`。

`blog-notes` 用来把学习内容、课程记录、技术知识点或读书收获整理成便于长期查阅的 Markdown 笔记。默认结构为“前言、主体、总结”，文件第一行写入 YAML Front Matter。

## 快速开始

```text
请使用 blog-notes skill 生成 Markdown 学习笔记
输入：我今天学习了 SNMP v2 和 v3 的区别，以及华为、华三、思科设备的基础配置命令。
输出：一篇包含前言、主体、总结的 .md 文件
```

指定文件路径：

```text
使用 blog-notes 写一篇笔记
主题：SNMP 协议配置
内容：<你的学习内容>
输出：D:\2.Typora\Blog\network\SNMP协议配置.md
```

## 触发方式

| 你的需求 | 推荐说法 |
| --- | --- |
| 记录学习内容 | `写一篇 Blog-Notes，内容是...` |
| 整理知识点 | `整理这些知识点为 Markdown 笔记` |
| 生成博客笔记 | `生成一篇博客笔记，主题是...` |
| 整理课程内容 | `把这节课内容整理成学习笔记` |
| 指定分类标签 | `生成笔记 --category 网络 --tag SNMP` |
| 指定文件名 | `生成笔记 --filename snmp-notes.md` |

## 输出结构

```markdown
---
category: [网络]
tag: [SNMP]
status: publish
---

# 前言

<说明这篇笔记记录什么、为什么值得记录>

# 主体

<按知识点分层整理正文>

# 总结

<提炼关键结论和后续行动>
```

正文不额外写文章名称，YAML Front Matter 之后直接从 `# 前言` 开始。

## 参数

| 参数 | 生成方式 | 说明 |
| --- | --- | --- |
| `category` | AI 根据内容推断或用户指定 | 分类，最多 2 个词语 |
| `tag` | AI 根据内容提取或用户指定 | 标签，最多 2 个词语 |
| `status` | 固定为 `publish` | 发布状态 |
| `filename` | AI 自动生成或用户指定 | Markdown 文件名 |

## 适合记录什么

| 类型 | 示例 |
| --- | --- |
| 概念学习 | 什么是智能体、什么是 Prompt |
| 工具使用 | 如何配置 Git、如何安装 Skills |
| 代码理解 | 某个 API 的调用流程 |
| 课程笔记 | 一节技术课的核心内容 |
| 问题复盘 | 一个 bug 的原因和解决方式 |

## 示例

```text
请使用 blog-notes skill 生成 Markdown 笔记
主题：Git rebase 的使用场景
内容：
- rebase 可以整理提交历史
- 公共分支不要随便 rebase
- 解决冲突后使用 git rebase --continue
--category Git
--tag rebase
--filename git-rebase-notes.md
```

## 注意事项

- 默认 `status` 固定为 `publish`。
- `category` 和 `tag` 都控制在最多 2 个词语。
- 会保留关键术语、命令、代码片段和示例。
- 不会虚构来源、作者、日期或链接。
- 如果目标文件已存在，默认不覆盖，除非你明确要求覆盖。

## 常见问题

### 可以不保存文件，只输出内容吗？

可以，明确说“只输出 Markdown 内容，不写入文件”。

### 可以覆盖已有文件吗？

可以，但需要明确说“覆盖文件”或“允许覆盖”。

### 标题层级怎么安排？

正文从 `# 前言`、`# 主体`、`# 总结` 开始，主体内部再使用 `##`、`###` 分层。
