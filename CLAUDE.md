# 我的 AI Skills 项目

个人 Claude Code Skills 集合，每个 skill 是一个独立的目录，包含 `SKILL.md`（AI 执行规范）和可选的 `config.yaml`、`README.md`。

## 项目结构

```
.claude/skills/          ← Claude Code 自动发现 skills
├── git-commit/          ← 自动化 Git 提交
│   ├── SKILL.md         ← 技能执行规范（AI 读取）
│   ├── README.md        ← 用户使用文档
│   └── config.yaml      ← 默认参数配置
└── <future-skills>/     ← 未来添加的 skills
```

## 技术栈

- 平台: Windows + VSCode + Claude Code 扩展
- Skills 标准: Claude Code Skills 格式（基于 Agent Skills 开放标准）
- 托管: GitHub

## Skill 开发规范

### 最小结构
- `SKILL.md`: 必须，包含 YAML frontmatter（name, description, trigger）和完整执行规范

### 可选文件
- `README.md`: 用户使用文档
- `config.yaml`: 默认参数

### SKILL.md frontmatter 模板
```yaml
---
name: skill-name
description: 一句话描述
metadata:
  type: skill
  trigger:
    - "触发词1"
    - "触发词2"
---
```
