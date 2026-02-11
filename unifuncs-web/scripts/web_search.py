#!/usr/bin/env python3
"""
UniFuncs 网页搜索 CLI
=====================
实时网页搜索，获取搜索结果列表。

环境变量:
    UNIFUNCS_API_KEY: UniFuncs API Key (必需)

使用示例:
    python3 web_search.py "Python 教程"
    python3 web_search.py "Claude MCP" --count 20 --format json
    python3 web_search.py "AI 新闻" --freshness Week
"""

import os
import sys
import json
import argparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# API 配置
API_ENDPOINT = "https://api.unifuncs.com/api/web-search/search"
FORMATS = ["json", "markdown", "md", "text", "txt"]
FRESHNESS_OPTIONS = ["Day", "Week", "Month", "Year"]
AREA_OPTIONS = ["global", "cn"]


def get_api_key() -> str:
    """获取 API Key"""
    return os.getenv("UNIFUNCS_API_KEY", "")


def web_search(
    query: str,
    count: int = 10,
    page: int = 1,
    format: str = "markdown",
    freshness: str = None,
    area: str = None,
    include_images: bool = False
) -> str:
    """执行网页搜索"""
    api_key = get_api_key()
    if not api_key:
        return "错误: 未设置 UNIFUNCS_API_KEY 环境变量\n请运行: export UNIFUNCS_API_KEY=\"sk-your-api-key\""

    # 构建请求体
    request_body = {
        "query": query.strip(),
        "apiKey": api_key,
        "count": count,
        "page": page,
        "format": format,
        "includeImages": include_images
    }

    if freshness:
        request_body["freshness"] = freshness
    if area:
        request_body["area"] = area

    # 发送请求
    try:
        data = json.dumps(request_body).encode("utf-8")
        req = Request(
            API_ENDPOINT,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urlopen(req, timeout=60) as response:
            if format == "json":
                result = json.loads(response.read().decode("utf-8"))
                return json.dumps(result, ensure_ascii=False, indent=2)
            else:
                return response.read().decode("utf-8")

    except HTTPError as e:
        error_msg = f"API 请求失败 (HTTP {e.code})"
        try:
            error_detail = json.loads(e.read().decode("utf-8"))
            error_msg += f": {json.dumps(error_detail, ensure_ascii=False)}"
        except Exception:
            error_msg += f": {e.reason}"
        return error_msg

    except URLError as e:
        return f"网络错误: {e.reason}"

    except Exception as e:
        return f"请求失败: {str(e)}"


def main():
    parser = argparse.ArgumentParser(
        description="UniFuncs 网页搜索 - 实时搜索结果列表",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "Python 教程"
  %(prog)s "Claude MCP" --count 20 --format json
  %(prog)s "AI 新闻" --freshness Week
  %(prog)s "site:github.com FastAPI" --page 2

环境变量:
  UNIFUNCS_API_KEY    UniFuncs API Key (必需)
                      获取地址: https://unifuncs.com/account
        """
    )

    parser.add_argument("query", help="搜索关键词")
    parser.add_argument(
        "--count", "-c",
        type=int,
        default=10,
        choices=range(1, 51),
        metavar="1-50",
        help="每页结果数量 (默认: 10)"
    )
    parser.add_argument(
        "--page", "-p",
        type=int,
        default=1,
        help="页码 (默认: 1)"
    )
    parser.add_argument(
        "--format", "-f",
        choices=FORMATS,
        default="markdown",
        help="输出格式 (默认: markdown)"
    )
    parser.add_argument(
        "--freshness",
        choices=FRESHNESS_OPTIONS,
        help="时效性过滤: Day, Week, Month, Year"
    )
    parser.add_argument(
        "--area", "-a",
        choices=AREA_OPTIONS,
        help="搜索区域: global, cn"
    )
    parser.add_argument(
        "--images", "-i",
        action="store_true",
        help="包含图片搜索结果"
    )

    args = parser.parse_args()

    # 执行搜索
    result = web_search(
        query=args.query,
        count=args.count,
        page=args.page,
        format=args.format,
        freshness=args.freshness,
        area=args.area,
        include_images=args.images
    )

    print(result)


if __name__ == "__main__":
    main()
