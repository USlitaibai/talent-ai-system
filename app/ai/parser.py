"""
AI 返回结果解析器

负责：

1. 清理 Markdown
2. JSON解析
"""

import json


def clean_response(content: str) -> str:
    """
    清理 Markdown
    """

    content = content.replace("```json", "")
    content = content.replace("```", "")

    return content.strip()


def parse_json(content: str) -> dict:
    """
    JSON解析
    """

    content = clean_response(content)

    return json.loads(content)