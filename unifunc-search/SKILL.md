---
name: unifunc-search
description: 使用 UniFuncs API 进行实时网络搜索，支持全球和中国地域，获取最新网络内容和新闻。当用户需要搜索、查找、联网获取信息时使用。
argument-hint: [搜索关键词]
allowed-tools: Bash(curl:*)
---

# UniFuncs 实时搜索 Skill

快速的实时搜索服务，支持全球和中国地域搜索。

## 首次使用配置

1. 前往 https://unifuncs.com/account 获取 API Key
2. 设置环境变量：`export UNIFUNCS_API_KEY="sk-your-api-key"`

## 使用方法

执行搜索：
```bash
curl -X POST "https://api.unifuncs.com/api/web-search/search" \
  -H "Authorization: Bearer $UNIFUNCS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "$ARGUMENTS", "count": 10}'
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| query | 搜索关键词 | 必填 |
| area | `global` 或 `cn` | global |
| count | 结果数量 (1-50) | 10 |

## 更多信息

- 详细 API 文档见 [api.md](references/api.md)
