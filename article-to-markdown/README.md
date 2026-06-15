# article-to-markdown — 网页文章转 Markdown

本 README 面向使用者：如何触发并正确使用 `article-to-markdown` skill。执行细节和硬性规则在 `SKILL.md`。

`article-to-markdown` 用来把网页文章保存成干净的 Markdown 文件，自动生成 YAML Front Matter，并在正文第一行放置可识别到的特色图片。

它特别加强了 WordPress、Argon 主题、折叠区块和懒加载图片场景，目标是尽量保存完整正文，而不是只保存前端页面里短暂可见的部分。

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
| WordPress 正文 | 优先核对 REST API 完整正文，避免页面截断 |
| 折叠/隐藏内容 | 去掉折叠外壳但保留内部正文和后续内容 |
| 懒加载图片 | 优先提取真实图片地址，不保存 `data:image` 占位图 |
| 来源、更新时间、页脚推广 | 尽量移除 |
| 标题层级 | 如果正文没有一级标题，会自动整体提升一级 |
| 文件名 | 去除 Windows 不支持的字符 |

## 完整性保护

有些网页前端只展示文章摘要，或把正文放在折叠块、懒加载容器、主题组件里。这个 skill 会额外检查这些情况：

| 场景 | 处理方式 |
| --- | --- |
| WordPress 文章 | 识别文章 ID，并尝试读取 `/wp-json/wp/v2/posts/<id>` 的 `content.rendered` |
| Argon/Bootstrap 折叠块 | 折叠标题转为普通文本，正文继续保留 |
| `details` 展开块 | 保留展开块内部内容 |
| 图片懒加载 | 从 `data-src`、`data-original`、`data-lazy-src`、lightbox `href` 中找真实图片 |
| `data:image` 占位图 | 不写入 Markdown 正文图片，除非它出现在原文代码块中 |
| 内容疑似截断 | 对比正文长度、标题数量、图片数量和文末内容，必要时重新提取 |

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
- WordPress 页面会优先尝试 REST API；如果站点禁用了 API，会回退到页面 HTML。
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

### 折叠内容会不会丢失？

不应该丢失。遇到折叠块时，skill 的规则是“去外壳、保正文”：折叠标题可以转成普通文本，但折叠块内部和后面的正文必须保留。

### 为什么有些图片没有保存？

如果图片只是 `data:image`、透明占位图或 loading SVG，skill 会尝试寻找真实图片地址。找不到真实地址时，不会把占位图写进 Markdown。
