#!/usr/bin/env python3
"""
UniFuncs 深度研究 CLI
=====================
使用 U2 深度研究模型进行多轮迭代研究，产出专业的万字报告。

环境变量:
    UNIFUNCS_API_KEY: UniFuncs API Key (必需)

使用示例:
    python3 research.py "大语言模型的幻觉问题"
    python3 research.py "Rust vs Go 性能对比" --type zhihu-article
    python3 research.py "2024年AI发展趋势" --type summary --length 2000
"""

import os
import sys
import json
import argparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

# API 配置
API_ENDPOINT = "https://api.unifuncs.com/deepresearch/v1/chat/completions"
REFERENCE_STYLES = ["link", "character", "hidden"]
OUTPUT_TYPES = [
    "report",           # 万字报告
    "summary",          # 精炼摘要
    "wechat-article",   # 微信公众号文章
    "xiaohongshu-article",  # 小红书文章
    "toutiao-article",  # 头条文章
    "zhihu-article",    # 知乎文章
    "zhihu-answer",     # 知乎回答
    "weibo-article"     # 微博博文
]


def get_api_key() -> str:
    """获取 API Key"""
    return os.getenv("UNIFUNCS_API_KEY", "")


def deep_research(
    topic: str,
    max_depth: int = 25,
    output_type: str = "report",
    output_length: int = 10000,
    reference_style: str = "link",
    plan_approval: bool = False,
    introduction: str = None,
    domain_scope: str = None,
    domain_blacklist: str = None,
    output_prompt: str = None,
    timeout: int = 1800
) -> str:
    """执行深度研究"""
    api_key = get_api_key()
    if not api_key:
        return "错误: 未设置 UNIFUNCS_API_KEY 环境变量\n请运行: export UNIFUNCS_API_KEY=\"sk-your-api-key\""

    # 构建请求体
    request_body = {
        "model": "u2",
        "messages": [{"role": "user", "content": topic.strip()}],
        "stream": False,
        "max_depth": max_depth,
        "output_type": output_type,
        "output_length": output_length,
        "reference_style": reference_style,
        "plan_approval": plan_approval
    }

    if introduction:
        request_body["introduction"] = introduction
    if domain_scope:
        request_body["domain_scope"] = domain_scope
    if domain_blacklist:
        request_body["domain_blacklist"] = domain_blacklist
    if output_prompt:
        request_body["output_prompt"] = output_prompt

    # 发送请求 (深度研究耗时较长，设置 30 分钟超时)
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

        print(f"正在进行深度研究，请耐心等待 (通常需要 2-10 分钟)...", file=sys.stderr)

        effective_timeout = max(timeout, 1800)
        with urlopen(req, timeout=effective_timeout) as response:  # 最低 30 分钟超时
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
        description="UniFuncs 深度研究 - 多轮迭代研究，产出专业报告",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s "大语言模型的幻觉问题"
  %(prog)s "Rust vs Go 性能对比" --type zhihu-article
  %(prog)s "2024年AI发展趋势" --type summary --length 2000
  %(prog)s "新能源汽车市场分析" --depth 25

输出类型:
  report            万字深度报告 (默认)
  summary           精炼摘要 (1000-2000字)
  wechat-article    微信公众号文章风格
  xiaohongshu-article  小红书文章风格
  toutiao-article   头条文章风格
  zhihu-article     知乎专栏文章风格
  zhihu-answer      知乎回答风格
  weibo-article     微博长文风格

环境变量:
  UNIFUNCS_API_KEY    UniFuncs API Key (必需)
                      获取地址: https://unifuncs.com/account
        """
    )

    parser.add_argument("topic", help="研究主题")
    parser.add_argument(
        "--depth", "-d",
        type=int,
        default=25,
        choices=range(1, 26),
        metavar="1-25",
        help="研究深度 (默认: 25)"
    )
    parser.add_argument(
        "--type", "-t",
        choices=OUTPUT_TYPES,
        default="report",
        help="输出类型 (默认: report)"
    )
    parser.add_argument(
        "--length", "-l",
        type=int,
        default=10000,
        help="预期输出长度 (默认: 10000)"
    )
    parser.add_argument(
        "--reference", "-r",
        choices=REFERENCE_STYLES,
        default="link",
        help="引用格式 (默认: link)"
    )
    parser.add_argument(
        "--intro", "-i",
        help="设定研究员的角色和口吻"
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
        "--timeout",
        type=int,
        default=1800,
        help="API 请求超时时间，单位秒 (默认: 1800)"
    )

    args = parser.parse_args()

    # 执行研究
    result = deep_research(
        topic=args.topic,
        max_depth=args.depth,
        output_type=args.type,
        output_length=args.length,
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
