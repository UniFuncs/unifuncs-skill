#!/bin/bash

# UniFuncs Skills 安装脚本
# 用法: curl -fsSL https://raw.githubusercontent.com/UniFuncs/unifuncs-skill/main/install.sh | bash

set -e

REPO_URL="https://github.com/UniFuncs/unifuncs-skill"
SKILLS_DIR="$HOME/.claude/skills"
TEMP_DIR=$(mktemp -d)

echo "=================================="
echo "  UniFuncs Skills 安装程序"
echo "=================================="
echo ""

# 检查 git
if ! command -v git &> /dev/null; then
    echo "错误: 需要安装 git"
    exit 1
fi

# 创建 skills 目录
echo "1. 创建 skills 目录..."
mkdir -p "$SKILLS_DIR"

# 克隆仓库
echo "2. 下载 Skills..."
git clone --depth 1 "$REPO_URL" "$TEMP_DIR" 2>/dev/null || {
    echo "错误: 无法克隆仓库，请检查网络连接"
    rm -rf "$TEMP_DIR"
    exit 1
}

# 复制 Skills
echo "3. 安装 Skills..."
for skill in unifunc-search unifunc-reader unifunc-deep-search unifunc-deep-research; do
    if [ -d "$TEMP_DIR/$skill" ]; then
        cp -r "$TEMP_DIR/$skill" "$SKILLS_DIR/"
        echo "   ✓ $skill"
    fi
done

# 清理
rm -rf "$TEMP_DIR"

echo ""
echo "=================================="
echo "  安装完成!"
echo "=================================="
echo ""
echo "下一步:"
echo "1. 获取 API Key: https://unifuncs.com/account"
echo "2. 设置环境变量:"
echo "   export UNIFUNCS_API_KEY=\"sk-your-api-key\""
echo ""
echo "添加到 shell 配置文件 (~/.bashrc 或 ~/.zshrc):"
echo "   echo 'export UNIFUNCS_API_KEY=\"sk-your-api-key\"' >> ~/.zshrc"
echo ""
