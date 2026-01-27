---
name: unifunc-reader
description: 使用 UniFuncs API 读取网页、PDF、Word 等文档内容，支持 AI 内容提取。当用户需要阅读、抓取、提取网页或文档内容时使用。
argument-hint: [URL]
allowed-tools: Bash(curl:*)
---

# UniFuncs 网页阅读 Skill

读取网页、PDF、Word 等文档内容，支持 AI 内容提取。

## 首次使用配置

1. 前往 https://unifuncs.com/account 获取 API Key
2. 设置环境变量：`export UNIFUNCS_API_KEY="sk-your-api-key"`

## 使用方法

读取网页内容：
```bash
curl -X POST "https://api.unifuncs.com/api/web-reader/read" \
  -H "Authorization: Bearer $UNIFUNCS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"url": "$ARGUMENTS", "format": "md"}'
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| url | 目标 URL | 必填 |
| format | `md` 或 `txt` | md |
| topic | AI 提取主题 | 无 |

## 更多信息

- 详细 API 文档见 [api.md](references/api.md)
