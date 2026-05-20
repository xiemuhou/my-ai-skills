# article-to-markdown — 用户使用指南

本 README 面向**使用者**：如何触发并正确使用 `article-to-markdown` skill。
执行指令与硬性规范在 `SKILL.md`。

## 快速开始

### 常规用法（最小可用）

```text
请使用 article-to-markdown skill 把网页文章保存为 Markdown 文件
输入：一个网页 URL
输出：当前目录下的 .md 文件，带 YAML Front Matter 元数据
```

你也可以用更自然的方式：

```
保存文章 https://example.com/my-article
```

### 进阶用法（带参数约束）

```text
保存文章 https://example.com/my-article
另外，还有下列参数约束：
- --category 技术工具（文章分类，最多 2 个词语）
- --tag RSS,效率（内容标签，最多 2 个，逗号分隔）
- --path D:\我的笔记（保存目录）
- --filename 自定义文件名（不指定则自动从标题提取）
```

## 设计理念

✨ **核心价值**：一键将网页文章转为本地 Markdown 文件，自动添加 YAML Front Matter，适合博客备份、知识管理、离线阅读。

**工作原理**（简化版）：
1. 你提供一个网页 URL
2. AI 获取网页内容并转为 Markdown
3. AI 自动推断文章分类和标签
4. 清理来源信息、更新时间、页脚推广
5. 生成带 YAML Front Matter 的 `.md` 文件

**设计哲学**：
- 📄 **原样保存** — 不修改正文、不下载图片、不做 AI 摘要
- 🏷️ **自动标签** — AI 根据内容推断 category 和 tag，省去手动标注
- 📐 **标题修正** — 无一级标题时自动提升层级，保证文档结构完整

## 使用示例

### 示例 1：最简单的保存（推荐）

```
保存文章 https://blog.xmhweb.cn/499/
```

> AI 自动完成：获取内容 → 推断标签 → 清理杂项 → 保存文件。

### 示例 2：指定分类和标签

```
保存网页 https://example.com/python-tutorial --category 编程 --tag Python,教程
```

### 示例 3：指定保存目录

```
保存文章 https://example.com/post --path D:\07-博客笔记
```

### 示例 4：自定义文件名

```
下载文章 https://example.com/article --filename 我的学习笔记
```

## 输出文件

| 输出 | 说明 |
|------|------|
| `<标题>.md` | 文章 Markdown 文件，包含 YAML Front Matter |

**文件结构示例**：

```markdown
---
category: [技术工具]
tag: [RSS]
status: publish
---

## 文章章节一
正文内容...
```

## 可配置参数

| 参数 | 默认行为 | 说明 |
|------|----------|------|
| `--category` | AI 自动推断 | 文章分类，最多 2 个词语 |
| `--tag` | AI 自动推断 | 内容标签，最多 2 个，逗号分隔 |
| `--status` | `publish` | 发布状态 |
| `--filename` | 从标题提取 | 自定义保存文件名 |
| `--path` | 当前工作目录 | 指定保存目录 |

## ✨ 特性一览

- ✅ 原样保存，不修改正文
- ✅ 图片使用原始链接，不下载
- ✅ 自动移除文章来源、更新时间、页脚推广
- ✅ AI 根据内容自动推断 category 和 tag
- ✅ 标题仅用于文件名，不出现在正文中
- ✅ 无 H1 时自动提升标题层级
- ✅ 标题自动作为文件名
- ✅ 支持中英文文章

## 常见问题

### Q：文章标题会在文件里吗？

A：不会。标题仅用作文件名和 YAML Front Matter 的参考，不会出现在 Markdown 正文中。

### Q：为什么我的文章所有标题都升了一级？

A：这是自动修正行为。如果原文没有一级标题（`# `），skill 会将所有标题提升一级，确保文档层级从 H1 开始。

### Q：图片会下载到本地吗？

A：不会。所有图片保持原始 URL 链接，节省磁盘空间。

### Q：category 和 tag 可以不指定吗？

A：完全可以。AI 会读取文章内容后自动推断合适的分类和标签，各不超过 2 个词语。

### Q：保存的文件名是什么？

A：默认从文章标题提取，去除 `<>:"/\|?*` 等非法字符。你也可以通过 `--filename` 自定义。
