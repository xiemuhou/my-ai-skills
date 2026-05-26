# git-publish-release — GitHub Release 发布助手

`git-publish-release` 用来根据 Git 历史生成 Release Notes，并创建 GitHub Release。它适合项目准备发版时使用，尤其是已经使用 tag 或 Conventional Commits 管理变更的仓库。

## 快速开始

```text
发布项目到 GitHub
```

AI 会按顺序处理：

```text
检查仓库状态 -> 分析 tag 和 commit -> 生成 Release Notes -> 判断是否预发布 -> 创建 GitHub Release
```

如果你只想生成文案，不创建 Release：

```text
生成 Release Notes
```

## 适合场景

| 你的需求 | 推荐说法 |
| --- | --- |
| 发布最新版本 | `发布项目到 GitHub` |
| 指定版本号发布 | `发布 v1.2.0` |
| 生成但不发布 | `生成 Release Notes` |
| 发布预发布版本 | `发布 v1.3.0-beta.1` |
| 首次发布 | `创建第一个 GitHub Release` |

## 发布前准备

建议在使用前确认：

```text
1. 当前仓库已经推送到 GitHub
2. GitHub 远端地址正确
3. 本地有 GitHub 认证，例如 gh auth login
4. 工作区没有未提交的重要改动
5. 版本号或 tag 策略已经明确
```

## Release Notes 生成逻辑

skill 会根据 commit 和 tag 历史归纳变更：

| Commit 类型 | Release Notes 分类 |
| --- | --- |
| `feat` | 新功能 |
| `fix` | 修复 |
| `docs` | 文档 |
| `perf` | 性能优化 |
| `refactor` | 重构 |
| `test` | 测试 |
| `chore` | 维护 |
| 其他 | 其他变更 |

如果没有足够规范的 commit message，AI 会根据 diff 和提交内容进行归纳。

## 版本和预发布

| 版本示例 | 处理方式 |
| --- | --- |
| `v1.0.0` | 正式版本 |
| `v1.1.0-alpha.1` | 预发布 |
| `v1.1.0-beta.1` | 预发布 |
| `v1.1.0-rc.1` | 预发布 |

带有 `alpha`、`beta`、`rc` 等标记的版本会自动识别为 prerelease。

## Prompt 示例

发布正式版：

```text
发布 v1.2.0 到 GitHub
```

生成 Release Notes 供人工检查：

```text
生成从上一个 tag 到现在的 Release Notes，但先不要发布
```

发布 beta 版本：

```text
发布 v1.3.0-beta.1 到 GitHub
```

首次发布：

```text
这是项目第一次发布，请生成首个 GitHub Release
```

## 辅助资源

| 路径 | 用途 |
| --- | --- |
| `references/release-notes-strategy.md` | Release Notes 组织策略 |
| `references/release-templates.md` | 常用发布文案模板 |
| `scripts/get-github-token.sh` | 获取 GitHub token 的辅助脚本 |

## 安全边界

- 不会 force push。
- 不会擅自改写 tag 历史。
- 发布前会尽量检查仓库状态和远端信息。
- 如果缺少 GitHub 权限或认证，会提示你先完成认证。

## 常见问题

### 需要先手动创建 tag 吗？

不一定。你可以让 AI 根据版本号创建发布流程，也可以先手动打 tag。更稳妥的方式是明确告诉 AI 版本号。

### 可以只生成 Release Notes 吗？

可以：

```text
只生成 Release Notes，不创建 GitHub Release
```

### GitHub 认证失败怎么办？

先在终端运行：

```bash
gh auth login
```

然后重新发起发布请求。
