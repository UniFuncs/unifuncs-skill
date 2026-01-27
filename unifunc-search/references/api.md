# Web Search API 参考文档

## 端点

| 方法 | URL |
|------|-----|
| GET | `https://api.unifuncs.com/api/web-search/search?query={关键词}&apiKey={API_KEY}` |
| POST | `https://api.unifuncs.com/api/web-search/search` |

## 请求参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| query | string | 是 | 搜索关键词 |
| apiKey | string | 是 | API密钥（也可通过Authorization头传送） |
| area | string | 否 | 搜索地区：`global`（全球，默认）、`cn`（中国） |
| freshness | string | 否 | 结果时效性：`Day`、`Week`、`Month`、`Year` |
| includeImages | boolean | 否 | 是否同时搜索图像，默认 `false` |
| page | number | 否 | 页码，默认 `1` |
| count | number | 否 | 每页结果数量（1-50），默认 `10` |
| format | string | 否 | 返回格式：`json`（默认）、`markdown`、`md`、`text`、`txt` |

## 状态码

| 状态码 | 消息 | 说明 |
|--------|------|------|
| 0 | 请求成功 | 返回正常的响应内容 |
| -20001 | 服务器错误 | 联系客服或稍后再试 |
| -20021 | API Key无效或已过期 | 检查API Key |
| -20025 | 账户余额不足 | 检查账户余额 |
| -20033 | 请求超出速率限制 | 降低请求频率 |
| -30001 | 搜索关键词无效 | 检查搜索关键词 |
