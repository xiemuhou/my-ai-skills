# pptx — 教程类 PPTX 制作

本 README 面向使用者：如何触发并正确使用 `pptx` skill。执行细节、默认样式和品牌规则在 `SKILL.md`、`config.yaml` 与 `references/tutorial-template-style.md`。

`pptx` 用来把主题、资料、笔记或大纲制作成可演示的教程类 PowerPoint。默认风格是简洁现代、明亮浅色、技术课程网页感，适合课程、培训、操作指南和技术分享。

## 快速开始

```text
请使用 pptx skill 制作一个 10 页教程类 PPT
输入：主题是如何使用 Codex Skills，受众是刚开始使用 Codex 的开发者
输出：桌面上的 .pptx 文件
```

更具体一点：

```text
请使用 pptx skill 制作教程类 PPT
主题：SNMP 协议配置入门
页数：10
受众：网络工程师
输出：D:\slides\snmp-tutorial.pptx
```

## 触发方式

| 你的需求 | 推荐说法 |
| --- | --- |
| 制作教程 PPT | `做一个教程类 PPT，主题是...` |
| 生成课件 | `生成一份课件，面向初学者` |
| 制作培训材料 | `把这些内容整理成培训 PPT` |
| 做操作指南 | `生成操作指南 PPT，每页一个步骤` |
| 技术分享 | `生成一份技术分享 PPT，包含代码和实践建议` |
| 指定输出文件 | `--output D:\slides\demo.pptx` |

## 默认风格

| 项目 | 规范 |
| --- | --- |
| 主题 | 明亮浅色主题 |
| 背景 | 浅灰蓝到白色柔和渐变 |
| 主色 | 深绿色或科技蓝 |
| 强调色 | 青绿色、浅蓝色 |
| 气质 | 简洁、现代、清爽、技术感、教学感 |
| 结构 | 学习目标、路线图、概念、步骤、示例、误区、复盘 |
| 画幅 | 16:9 宽屏 |

整体效果应像高级技术课程网页，而不是传统商务 PPT 或营销海报。

## 品牌 Logo

默认 Logo：

```text
pptx/assets/xiemuhou-wordmark-logo.svg
```

Logo 内容包含 `xiemuhou` 和 `blog.xmhweb.cn`，默认放在左下角。生成 PPT 时必须保持：

- 所有页面 Logo 尺寸一致。
- Logo 作为背景品牌层或母版层处理。
- 不与正文、页码、表格、代码块或图表重叠。
- 默认不添加背景色、边框、底板或光晕。
- 如果用户提供 `--logo <path/url>`，优先使用用户指定 Logo。

## 默认页面结构

如果你只给主题，skill 会自动补齐教学路径：

```text
1. 封面
2. 为什么要学
3. 学习地图
4. 核心概念
5. 操作步骤
6. 代码或示例演示
7. 方案对比
8. 常见误区
9. 检查清单
10. 总结与下一步
```

## 代码页规则

当 PPT 里包含代码：

- 使用等宽字体，例如 `Consolas`、`Cascadia Code`、`JetBrains Mono`。
- 每页代码不超过 12 行。
- 只展示关键片段，不把完整文件塞进一页。
- 做基础语法高亮。
- 用标注解释关键行。

## 参数

| 参数 | 作用 |
| --- | --- |
| `--pages <n>` | 指定页数 |
| `--audience <text>` | 指定受众 |
| `--level beginner|intermediate|advanced` | 指定难度 |
| `--style tutorial|workshop|course|guide|tech-share` | 指定教程子风格 |
| `--theme light|dark` | 指定主题，默认 `light` |
| `--logo <path/url>` | 指定 Logo |
| `--brand xmh|xiemuhou|谢幕后` | 指定品牌文字 |
| `--output <path>` | 指定输出路径 |
| `--language zh|en` | 指定语言 |

## 示例

基础教程：

```text
请使用 pptx skill 制作 10 页教程类 PPT
主题：Python 虚拟环境入门
受众：没有工程经验的初学者
风格：简洁现代，明亮主题，技术感
```

技术分享：

```text
请使用 pptx skill 生成 12 页技术分享 PPT
主题：如何设计高质量 Agent Skill
难度：intermediate
要求：包含代码示例、反例、最佳实践和课后练习
```

指定输出路径：

```text
请使用 pptx skill 制作教程类 PPT
主题：AI 热门词语讲解
--pages 15
--output C:\Users\<你的用户名>\Desktop\AI术语讲解.pptx
```

## 交付检查

生成后应尽量检查：

- 页数符合要求。
- 每页标题可读。
- 文本没有明显溢出。
- 元素没有重叠。
- Logo 尺寸和位置一致。
- 代码块清晰可读。
- 输出路径明确。

## 常见问题

### 只给主题可以吗？

可以。AI 会自动补齐大纲和教学路径。

### 这个 skill 适合做营销 PPT 吗？

不优先适合。它偏教程、培训、技术分享和知识讲解，不做夸张营销风格。

### Logo 可以换吗？

可以，用 `--logo <path/url>` 指定你自己的 Logo。
