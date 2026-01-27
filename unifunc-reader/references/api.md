# Web Reader API 参考文档

## 端点

| 方法 | URL |
|------|-----|
| GET | `https://api.unifuncs.com/api/web-reader/{URL编码的路径}?apiKey={API_KEY}` |
| POST | `https://api.unifuncs.com/api/web-reader/read` |

## 基础参数

| 参数名 | 类型 | 必需 | 描述 |
|--------|------|------|------|
| url/path | string | 是 | 需要阅读的URL |
| format | string | 否 | 返回格式：`markdown`/`md`（默认）、`text`/`txt` |
| liteMode | boolean | 否 | 精简模式，默认 `false` |
| includeImages | boolean | 否 | 是否包含图片，默认 `true` |
| maxWords | number | 否 | 最大字符数（0-5000000） |
