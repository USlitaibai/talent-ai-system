"""
Talent Recommender

AI 人才推荐报告
"""

import json

from ollama import chat

from app.core.config import OLLAMA_MODEL
from app.core.logger import logger


def generate_recommendation(
    resume: dict,
    jd: dict
) -> dict:
    """
    AI生成候选人推荐报告
    """

    logger.info("开始生成 AI 推荐报告")

    prompt = f"""
你是一名资深HR。

下面是岗位信息：

{json.dumps(jd, ensure_ascii=False)}

下面是候选人信息：

{json.dumps(resume, ensure_ascii=False)}

请只返回JSON，不要解释，不要Markdown。

格式：

{{
    "advantages": [
        ""
    ],
    "disadvantages": [
        ""
    ],
    "summary": "",
    "recommend": ""
}}

要求：

1. advantages、disadvantages 必须为数组
2. recommend 只能填写：
   建议进入下一轮
   建议保留
   不建议进入下一轮
"""

    response = chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.message.content.strip()

    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    logger.info("AI 推荐报告生成完成")

    return json.loads(result)