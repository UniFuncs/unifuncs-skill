#!/usr/bin/env python3
"""
UniFuncs 网页阅读 CLI
=====================
读取并解析网页内容，提取结构化正文。

环境变量:
    UNIFUNCS_API_KEY: UniFuncs API Key (必需)

使用示例:
    python3 web_reader.py "https://docs.python.org/3/tutorial/"
    python3 web_reader.py "https://example.com" --lite --format text
    python3 web_reader.py "https://example.com" --topic "API 使用方法"
"""

import os
import sys
import json
import argparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# API 配置
API_ENDPOINT = "https://api.unifuncs.com/api/web-reader/read"
FORMATS = ["markdown", "md", "text", "txt"]


def get_api_key() -> str:
    """获取 API Key"""
    return os.getenv("UNIFUNCS_API_KEY", "")


def web_reader(
    url: str,
    format: str = "markdown",
    lite_mode: bool = False,
    include_images: bool = True,
    max_words: int = 0,
    read_timeout: int = 120000,
    topic: str = None,
    link_summary: bool = False
) -> str:
    """读取网页内容"""
    api_key = get_api_key()
    if not api_key:
        return "错误: 未设置 UNIFUNCS_API_KEY 环境变量\n请运行: export UNIFUNCS_API_KEY=\"sk-your-api-key\""

    # 构建请求体
    request_body = {
        "url": url.strip(),
        "apiKey": api_key,
        "format": format,
        "liteMode": lite_mode,
        "includeImages": include_images,
        "readTimeout": read_timeout,
        "linkSummary": link_summary
    }

    if max_words > 0:
        request_body["maxWords"] = max_words
    if topic:
        request_body["topic"] = topic

    # 发送请求
    try:
        data = json.dumps(request_body).encode("utf-8")
        req = Request(
            API_ENDPOINT,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        with urlopen(req, timeout=300) as response:
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
        description="UniFuncs 网页阅读 - 提取网页结构化正文",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "https://docs.python.org/3/tutorial/"
  %(prog)s "https://example.com" --lite --format text
  %(prog)s "https://example.com" --topic "API 使用方法"
  %(prog)s "https://example.com" --links --max-words 5000

环境变量:
  UNIFUNCS_API_KEY    UniFuncs API Key (必需)
                      获取地址: https://unifuncs.com/account
        """
    )

    parser.add_argument("url", help="目标网页 URL")
    parser.add_argument(
        "--format", "-f",
        choices=FORMATS,
        default="markdown",
        help="输出格式 (默认: markdown)"
    )
    parser.add_argument(
        "--lite", "-l",
        action="store_true",
        help="可读性过滤模式，只保留正文"
    )
    parser.add_argument(
        "--no-images",
        action="store_true",
        help="不包含图片"
    )
    parser.add_argument(
        "--max-words", "-m",
        type=int,
        default=0,
        help="最大字符数限制 (默认: 不限制)"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=120000,
        help="读取超时时间(毫秒) (默认: 120000)"
    )
    parser.add_argument(
        "--topic",
        help="提取特定主题相关内容"
    )
    parser.add_argument(
        "--links",
        action="store_true",
        help="附加页面链接列表"
    )

    args = parser.parse_args()

    # 执行阅读
    result = web_reader(
        url=args.url,
        format=args.format,
        lite_mode=args.lite,
        include_images=not args.no_images,
        max_words=args.max_words,
        read_timeout=args.timeout,
        topic=args.topic,
        link_summary=args.links
    )

    print(result)


if __name__ == "__main__":
    main()
