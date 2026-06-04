# git-publish-release — GitHub Release 发布助手

本 README 面向使用者：如何触发并正确使用 `git-publish-release` skill。执行细节和发布安全规则在 `SKILL.md`。

`git-publish-release` 用来根据 Git tag 和 commit 历史生成 Release Notes，并创建 GitHub Release。它适合项目准备发布新版本时使用。

## 快速开始

```text
请使用 git-publish-release skill 发布 v1.2.0
输入：当前 Git 仓库
输出：GitHub Release 页面
```

只生成文案，不发布：

```text
生成 Release Notes，但先不要创建 GitHub Release
```

## 触发方式

| 你的需求 | 推荐说法 |
| --- | --- |
| 发布指定版本 | `发布 v1.2.0` |
| 创建 Release 页面 | `帮我创建 GitHub Release 页面` |
| 生成发布说明 | `生成 Release Notes` |
| 发布预发布版本 | `发布 v1.3.0-beta.1` |
| 首次发布 | `创建第一个 GitHub Release` |
| 只总结变更 | `总结上一个 tag 到现在的变化` |

## 发布前准备

建议先确认：

```text
1. 当前仓库已经关联 GitHub remote
2. 目标 tag 已存在，或你已经明确版本号
3. 本地已经完成 gh auth login
4. 重要改动已经提交
5. 你知道这是正式版还是预发布版
```

检查 GitHub CLI：

```bash
gh auth status
```

## 工作流程

```text
确认仓库 -> 获取上一个 Release -> 分析 commit -> 生成 Release Notes -> 判断 prerelease -> 创建 Release -> 读回校验
```

Release Notes 通常包含：

| 章节 | 内容 |
| --- | --- |
| 核心亮点 | 本次发布最重要的价值 |
| 主要更新 | 新功能、文档、行为变化 |
| 技术改进 | 重构、稳定性、工具链 |
| 完整变更 | 关键 commits 或变更范围 |

## 中文 Release 防乱码

如果 Release 标题或正文包含中文，skill 会强制走 UTF-8 安全路径：

- Release Notes 先写入 UTF-8 文件，再通过 `--notes-file` 或 GitHub API 发布。
- 不把中文正文直接塞进 PowerShell 命令、`echo` 管道或 here-string 管道。
- 发布后必须读回 GitHub 上的标题和正文。
- 如果发现 `????` 或 `�`，必须先修复，再告诉你发布成功。

这条规则是为了避免 Windows / PowerShell 编码导致 GitHub Release 页面中文乱码。

## 版本和预发布

| 版本示例 | 处理方式 |
| --- | --- |
| `v1.0.0` | 正式版本 |
| `v1.1.0-alpha.1` | 预发布 |
| `v1.1.0-beta.1` | 预发布 |
| `v1.1.0-rc.1` | 预发布 |

包含 `alpha`、`beta`、`rc`、`pre` 的 tag 会自动识别为 prerelease。

## 示例

发布正式版：

```text
发布 v2.0.1
```

创建 Release 页面：

```text
帮我创建 GitHub Release 页面，版本是 v2.0.1
```

只生成说明：

```text
生成从上一个 tag 到 v2.0.1 的 Release Notes，但不要发布
```

## 安全边界

- 不会 force push。
- 不会擅自改写 tag 历史。
- Release 已存在时会说明情况，再决定是否编辑。
- 中文发布内容必须读回校验，避免乱码。
- 除非用户明确要求 annotated tag，否则优先使用 lightweight tag。

## 常见问题

### 需要先手动创建 tag 吗？

不一定。你可以明确告诉 AI 版本号，也可以先手动创建 tag。更稳妥的方式是说清目标版本，例如 `发布 v2.0.1`。

### 可以只生成 Release Notes 吗？

可以：

```text
只生成 Release Notes，不创建 GitHub Release
```

### GitHub 认证失败怎么办？

先运行：

```bash
gh auth login
```

完成认证后重新发布。
