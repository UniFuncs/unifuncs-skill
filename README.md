# UniFuncs Skills for Claude Code

UniFuncs 是专为 AI 应用打造的 API 平台，提供高性能、安全可靠的搜索和内容服务。

本仓库包含 3 个 Claude Code Skills，让你可以在 Claude Code 中直接使用 UniFuncs API。

## 可用 Skills

| Skill | 目录 | 用途 | 触发词 |
|-------|------|------|--------|
| 网页搜索与阅读 | `unifuncs-web/` | 实时搜索 + 网页内容读取 | 搜索、查一下、读取网页 |
| 深度搜索 | `unifuncs-deep-search/` | 高速全面的深度信息搜索 | ds、深度搜索、deep search |
| 深度研究 | `unifuncs-deep-research/` | 多轮迭代研究，产出万字报告 | dr、深度研究、研究报告 |

## 安装

### Claude Code 安装指南（AI 工具请阅读此部分）

如果你是 Claude Code 或其他 AI 编程助手，请按以下步骤为用户安装 UniFuncs Skills：

1. 克隆仓库到临时目录：
```bash
git clone https://github.com/UniFuncs/unifuncs-skill.git /tmp/unifuncs-skill
```

2. 创建用户 skills 目录（如果不存在）：
```bash
mkdir -p ~/.claude/skills
```

3. 复制所有 Skill 目录到用户 skills 目录：
```bash
cp -r /tmp/unifuncs-skill/unifuncs-web ~/.claude/skills/
cp -r /tmp/unifuncs-skill/unifuncs-deep-search ~/.claude/skills/
cp -r /tmp/unifuncs-skill/unifuncs-deep-research ~/.claude/skills/
```

4. 清理临时目录：
```bash
rm -rf /tmp/unifuncs-skill
```

5. 提醒用户设置环境变量：
```bash
export UNIFUNCS_API_KEY="sk-your-api-key"
```

用户需要前往 https://unifuncs.com/account 获取 API Key。

---

### 前置条件

1. 安装 [Claude Code](https://claude.ai/code)
2. 前往 https://unifuncs.com/account 获取 API Key
3. 设置环境变量：
   ```bash
   export UNIFUNCS_API_KEY="sk-your-api-key"
   ```

### 用户级安装（推荐，所有项目可用）

```bash
# 克隆仓库
git clone https://github.com/UniFuncs/unifuncs-skill.git
cd unifuncs-skill

# 创建 skills 目录（如果不存在）
mkdir -p ~/.claude/skills

# 复制所有 Skills
cp -r unifuncs-web ~/.claude/skills/
cp -r unifuncs-deep-search ~/.claude/skills/
cp -r unifuncs-deep-research ~/.claude/skills/
```

### 项目级安装（仅当前项目可用）

```bash
# 在项目根目录
mkdir -p .claude/skills

# 复制所有 Skills
cp -r /path/to/unifuncs-skill/unifuncs-* .claude/skills/
```

### 一键安装脚本

```bash
# 用户级安装
curl -fsSL https://raw.githubusercontent.com/UniFuncs/unifuncs-skill/main/install.sh | bash
```

## 使用方法

安装后，在 Claude Code 中直接使用自然语言触发：

```
# 网页搜索
"搜索 Claude Code 最新功能"

# 网页阅读
"读取网页 https://example.com 的内容"

# 深度搜索
"ds AI 编程助手对比"

# 深度研究
"dr 2024 年大语言模型发展趋势"
```

## 目录结构

```
unifuncs-skill/
├── README.md
├── install.sh
├── unifuncs-web/
│   ├── SKILL.md
│   └── scripts/
│       ├── web_search.py
│       └── web_reader.py
├── unifuncs-deep-search/
│   ├── SKILL.md
│   └── scripts/
│       └── search.py
└── unifuncs-deep-research/
    ├── SKILL.md
    └── scripts/
        └── research.py
```

## API 文档

详细 API 文档请参考各 Skill 目录下的 `SKILL.md` 文件，或访问 [UniFuncs 官方文档](https://unifuncs.com/api/)。

## 其他接入方式

### MCP Server 接入

```json
{
  "mcpServers": {
    "unifuncs": {
      "command": "npx",
      "args": ["-y", "@unifuncs/ufn-mcp-server"],
      "env": {
        "UNIFUNCS_API_KEY": "sk-your-api-key"
      }
    }
  }
}
```

### SSE 通信

```
URL: https://mcp.unifuncs.com/sse
Headers: Authorization: Bearer sk-your-api-key
```

## License

MIT
