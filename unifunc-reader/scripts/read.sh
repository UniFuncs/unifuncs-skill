#!/bin/bash
# UniFuncs Web Reader API 调用脚本
# 用法: ./read.sh "URL" [format]

URL="$1"
FORMAT="${2:-md}"

if [ -z "$UNIFUNCS_API_KEY" ]; then
    echo "错误: 请设置 UNIFUNCS_API_KEY 环境变量"
    exit 1
fi

if [ -z "$URL" ]; then
    echo "用法: ./read.sh \"URL\" [format:md|txt]"
    exit 1
fi

curl -s -X POST "https://api.unifuncs.com/api/web-reader/read" \
    -H "Authorization: Bearer $UNIFUNCS_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{\"url\": \"$URL\", \"format\": \"$FORMAT\"}"
