# article-to-markdown — 网页文章转 Markdown

本 README 面向使用者：如何触发并正确使用 `article-to-markdown` skill。执行细节和硬性规则在 `SKILL.md`。

`article-to-markdown` 用来把网页文章保存成干净的 Markdown 文件，自动生成 YAML Front Matter，并在正文第一行放置可识别到的特色图片。

## 快速开始

```text
请使用 article-to-markdown skill 保存网页文章
输入：https://example.com/article
输出：当前目录下的 Markdown 文件
```

指定保存目录：

```text
保存文章 https://example.com/article --path D:\2.Typora\Blog
```

## 触发方式

| 你的需求 | 推荐说法 |
| --- | --- |
| 保存网页文章 | `保存文章 <url>` |
| 网页转 Markdown | `网页转markdown <url>` |
| 下载文章到指定目录 | `保存网页 <url> --path D:\notes` |
| 指定分类和标签 | `保存文章 <url> --category 技术 --tag AI` |
| 指定文件名 | `保存文章 <url> --filename codex-skills.md` |
| 手动指定特色图片 | `保存文章 <url> --featured-image https://example.com/cover.jpg` |

## 输出文件

生成的 Markdown 文件结构如下：

````markdown
---
category: [技术]
tag: [AI]
status: publish
---

![](https://example.com/cover.jpg)

正文内容...
````

Front Matter 只包含 `category`、`tag`、`status` 三个字段。特色图片必须放在第二个 `---` 之后，属于正文内容，不会写入 YAML Front Matter。

## 处理规则

| 内容 | 处理方式 |
| --- | --- |
| 文章标题 | 用于生成文件名，不写入正文 |
| 特色图片 | 放在正文第一行，保留原始 URL |
| 正文图片 | 保留原链接，不下载、不转存、不改写 |
| 正文内容 | 保留原文结构，不做摘要或润色 |
| 来源、更新时间、页脚推广 | 尽量移除 |
| 标题层级 | 如果正文没有一级标题，会自动整体提升一级 |
| 文件名 | 去除 Windows 不支持的字符 |

## 参数

| 参数 | 作用 |
| --- | --- |
| `--category <名称>` | 指定分类，最多 2 个词语 |
| `--tag <标签>` | 指定标签，最多 2 个词语 |
| `--status <状态>` | 指定发布状态，默认 `publish` |
| `--filename <名称>` | 指定保存文件名 |
| `--path <目录>` | 指定保存目录 |
| `--featured-image <URL>` | 手动指定特色图片链接 |

## 示例

保存到当前目录：

```text
保存文章 https://example.com/article
```

保存到 Typora 博客目录：

```text
保存网页 https://example.com/article --path D:\2.Typora\Blog\AI
```

指定元数据：

```text
保存文章 https://example.com/article --category 网络 --tag SNMP --filename snmp-guide.md
```

## 注意事项

- 目标网页必须能直接访问。
- 付费墙、登录后内容、强反爬页面可能无法完整提取。
- 如果无法可靠识别特色图片，不会编造图片链接，也不会插入占位图。
- 如果目标文件已存在，默认停止并提示，不会直接覆盖。
- 默认不翻译、不总结、不改写原文。

## 常见问题

### 可以把图片下载到本地吗？

默认不下载。这个 skill 的原则是保留图片原始链接，避免改变文章内容和图片来源。

### 特色图片会写入 Front Matter 吗？

不会。Front Matter 只允许 `category`、`tag`、`status`。特色图片会以 Markdown 图片语法放在正文第一行。

### 正文会保留文章标题吗？

不会。标题只用于生成文件名，正文从文章内容开始。
