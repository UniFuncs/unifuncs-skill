#!/usr/bin/env python3
"""
UniFuncs 深度搜索 CLI
=====================
使用 S2 深度搜索模型进行高速、准确、全面的信息检索。

环境变量:
    UNIFUNCS_API_KEY: UniFuncs API Key (必需)

使用示例:
    python3 search.py "Python 异步编程"
    python3 search.py "React hooks" --depth 15 --domain "reactjs.org,github.com"
"""

import os
import sys
import json
import argparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# API 配置
API_ENDPOINT = "https://api.unifuncs.com/deepsearch/v1/chat/completions"
REFERENCE_STYLES = ["link", "character", "hidden"]


def get_api_key() -> str:
    """获取 API Key"""
    return os.getenv("UNIFUNCS_API_KEY", "")


def deep_search(
    query: str,
    max_depth: int = 25,
    reference_style: str = "link",
    introduction: str = None,
    domain_scope: str = None,
    domain_blacklist: str = None,
    output_prompt: str = None,
    timeout: int = 900
) -> str:
    """执行深度搜索"""
    api_key = get_api_key()
    if not api_key:
        return "错误: 未设置 UNIFUNCS_API_KEY 环境变量\n请运行: export UNIFUNCS_API_KEY=\"sk-your-api-key\""

    # 构建请求体
    request_body = {
        "model": "s2",
        "messages": [{"role": "user", "content": query.strip()}],
        "stream": False,
        "max_depth": max_depth,
        "reference_style": reference_style
    }

    if introduction:
        request_body["introduction"] = introduction
    if domain_scope:
        request_body["domain_scope"] = domain_scope
    if domain_blacklist:
        request_body["domain_blacklist"] = domain_blacklist
    if output_prompt:
        request_body["output_prompt"] = output_prompt

    # 发送请求
    try:
        data = json.dumps(request_body).encode("utf-8")
        req = Request(
            API_ENDPOINT,
            data=data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            method="POST"
        )

        effective_timeout = max(timeout, 900)
        with urlopen(req, timeout=effective_timeout) as response:
            result = json.loads(response.read().decode("utf-8"))

            # 解析 OpenAI 兼容格式的响应
            if "choices" in result and len(result["choices"]) > 0:
                content = result["choices"][0].get("message", {}).get("content", "")
                if content:
                    return content

            return json.dumps(result, ensure_ascii=False, indent=2)

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
        description="UniFuncs 深度搜索 - 高速、准确、全面的信息检索",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "Python 异步编程"
  %(prog)s "React hooks" --depth 15
  %(prog)s "FastAPI 教程" --domain "fastapi.tiangolo.com,github.com"
  %(prog)s "机器学习" --blacklist "csdn.net,zhihu.com"

环境变量:
  UNIFUNCS_API_KEY    UniFuncs API Key (必需)
                      获取地址: https://unifuncs.com/account
        """
    )

    parser.add_argument("query", help="搜索查询内容")
    parser.add_argument(
        "--depth", "-d",
        type=int,
        default=25,
        choices=range(1, 26),
        metavar="1-25",
        help="搜索深度 (默认: 25)"
    )
    parser.add_argument(
        "--reference", "-r",
        choices=REFERENCE_STYLES,
        default="link",
        help="引用格式: link(默认), character, hidden"
    )
    parser.add_argument(
        "--intro", "-i",
        help="设定回答的角色和风格"
    )
    parser.add_argument(
        "--domain",
        help="限定搜索网站 (逗号分隔)"
    )
    parser.add_argument(
        "--blacklist", "-b",
        help="排除网站 (逗号分隔)"
    )
    parser.add_argument(
        "--prompt", "-p",
        help="自定义输出提示词"
    )
    parser.add_argument(
        "--timeout", "-t",
        type=int,
        default=900,
        help="API 请求超时时间，单位秒 (默认: 900)"
    )

    args = parser.parse_args()

    # 执行搜索
    result = deep_search(
        query=args.query,
        max_depth=args.depth,
        reference_style=args.reference,
        introduction=args.intro,
        domain_scope=args.domain,
        domain_blacklist=args.blacklist,
        output_prompt=args.prompt,
        timeout=args.timeout
    )

    print(result)


if __name__ == "__main__":
    main()
