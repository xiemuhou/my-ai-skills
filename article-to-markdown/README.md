# article-to-markdown — 网页文章保存为 Markdown

`article-to-markdown` 用来把网页文章保存成干净的 Markdown 文件，自动补齐 YAML Front Matter，并把文章特色图片链接放到正文第一行。它适合收藏技术文章、博客、教程、访谈和参考资料。

## 快速开始

```text
保存文章 https://example.com/article
```

AI 会完成：

```text
获取网页 -> 提取特色图片 -> 提取正文 -> 清理干扰内容 -> 生成 front matter -> 保存 .md 文件
```

默认保存到当前目录。

## 适合场景

| 你的需求 | 推荐说法 |
| --- | --- |
| 保存一篇网页文章 | `保存文章 <url>` |
| 保存到指定目录 | `保存文章 <url> --path D:\notes` |
| 指定分类和标签 | `保存网页 <url> --category 技术 --tag python` |
| 自定义文件名 | `保存文章 <url> --filename async-python.md` |
| 手动指定特色图片 | `保存文章 <url> --featured-image https://example.com/cover.jpg` |
| 英文触发 | `article to markdown <url>` |

## 输出格式

生成的 Markdown 文件通常包含：

```markdown
---
title: 文章标题
source: https://example.com/article
category: 技术
tags:
  - python
  - async
saved_at: 2026-05-26
---

![featured image](https://example.com/cover.jpg)

正文内容...
```

## 保存原则

| 内容 | 处理方式 |
| --- | --- |
| 标题 | 用于文件名和 front matter |
| 特色图片 | 优先从 `og:image`、`twitter:image`、JSON-LD `image` 或文章主图提取，放在正文第一行 |
| 正文 | 尽量保留原文结构 |
| 图片 | 保留原始图片链接 |
| 来源链接 | 写入 front matter |
| 广告、页脚、推荐阅读 | 尽量移除 |
| 更新时间、作者信息 | 如果网页中清晰可见，会尽量保留到元数据 |

## Prompt 示例

最简单的保存：

```text
保存文章 https://example.com/article
```

指定目录：

```text
保存文章 https://example.com/article --path D:\my-notes\articles
```

指定分类和标签：

```text
保存网页 https://example.com/article --category AI --tag prompt --tag codex
```

自定义文件名：

```text
保存文章 https://example.com/article --filename codex-skills-guide.md
```

手动指定特色图片：

```text
保存文章 https://example.com/article --featured-image https://example.com/cover.jpg
```

## 注意事项

- 需要能访问目标网页。
- 付费墙、登录后内容、强反爬页面可能无法完整提取。
- 如果网页结构很复杂，AI 会优先保留正文可读性，而不是逐像素复刻页面。
- 文件名会尽量安全化，避免 Windows 不支持的字符。
- 如果无法可靠识别特色图片，不会编造图片链接，也不会插入占位图片。

## 常见问题

### 可以保存图片到本地吗？

默认只保留图片原始链接，不下载图片。这样生成速度更快，也避免版权和存储问题。

### 特色图片保存在哪里？

如果能识别到特色图片，文件会在 front matter 后的正文第一行写入：

```markdown
![featured image](https://example.com/cover.jpg)
```

特色图片不会写入 YAML Front Matter；front matter 只保留分类、标签、状态等元数据。

### 会翻译文章吗？

默认不会翻译，会保留原文。你可以明确要求：

```text
保存文章 <url>，并额外生成中文摘要
```

### 可以批量保存吗？

可以给出多个 URL，但建议一次不要太多，方便检查每篇文章的提取质量。
