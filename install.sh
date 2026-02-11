#!/bin/bash
# UniFuncs Skills 安装脚本
# 将 UniFuncs Skills 安装到 Claude Code 的 skills 目录

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 配置
REPO_URL="https://github.com/UniFuncs/unifuncs-skill.git"
SKILLS_DIR="$HOME/.claude/skills"
TEMP_DIR=$(mktemp -d)

# 清理函数
cleanup() {
    rm -rf "$TEMP_DIR"
}
trap cleanup EXIT

# 打印带颜色的消息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查 git 是否安装
check_git() {
    if ! command -v git &> /dev/null; then
        print_error "git 未安装，请先安装 git"
        exit 1
    fi
}

# 检查 Python 是否安装
check_python() {
    if ! command -v python3 &> /dev/null; then
        print_warning "python3 未安装，skills 可能无法正常工作"
    else
        print_info "Python 版本: $(python3 --version)"
    fi
}

# 主安装流程
main() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║       UniFuncs Skills for Claude Code 安装程序           ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo ""

    # 检查依赖
    print_info "检查依赖..."
    check_git
    check_python

    # 创建目标目录
    print_info "创建 skills 目录: $SKILLS_DIR"
    mkdir -p "$SKILLS_DIR"

    # 克隆仓库
    print_info "下载 UniFuncs Skills..."
    git clone --depth 1 "$REPO_URL" "$TEMP_DIR" 2>/dev/null || {
        print_error "下载失败，请检查网络连接"
        exit 1
    }

    # 复制 skills
    print_info "安装 skills..."

    # 安装各个 skill
    for skill in unifuncs-web unifuncs-deep-search unifuncs-deep-research; do
        if [ -d "$TEMP_DIR/$skill" ]; then
            cp -r "$TEMP_DIR/$skill" "$SKILLS_DIR/"
            print_success "已安装: $skill"
        fi
    done

    # 设置脚本执行权限
    print_info "设置脚本执行权限..."
    find "$SKILLS_DIR" -name "*.py" -exec chmod +x {} \;

    echo ""
    print_success "安装完成！"
    echo ""
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                      后续配置步骤                        ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo ""
    echo "1. 获取 API Key:"
    echo "   前往 https://unifuncs.com/account 获取您的 API Key"
    echo ""
    echo "2. 设置环境变量:"
    echo "   export UNIFUNCS_API_KEY=\"sk-your-api-key\""
    echo ""
    echo "3. 持久化配置 (可选):"
    echo "   将上述 export 命令添加到 ~/.bashrc 或 ~/.zshrc"
    echo ""
    echo "4. 验证安装:"
    echo "   重启 Claude Code，然后尝试: \"深度搜索 MCP 协议是什么\""
    echo ""
    echo "已安装的 skills:"
    ls -1 "$SKILLS_DIR" | grep unifuncs | while read skill; do
        echo "   - $skill"
    done
    echo ""
}

# 运行主函数
main
