#!/bin/bash
# UniFuncs Web Search API 调用脚本
# 用法: ./search.sh "搜索关键词" [area] [count]

QUERY="$1"
AREA="${2:-global}"
COUNT="${3:-10}"

if [ -z "$UNIFUNCS_API_KEY" ]; then
    echo "错误: 请设置 UNIFUNCS_API_KEY 环境变量"
    echo "export UNIFUNCS_API_KEY=\"sk-your-api-key\""
    exit 1
fi

if [ -z "$QUERY" ]; then
    echo "用法: ./search.sh \"搜索关键词\" [area:global|cn] [count:1-50]"
    exit 1
fi

curl -s -X POST "https://api.unifuncs.com/api/web-search/search" \
    -H "Authorization: Bearer $UNIFUNCS_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"query\": \"$QUERY\", \"area\": \"$AREA\", \"count\": $COUNT}"
