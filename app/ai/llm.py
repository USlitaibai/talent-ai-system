"""
LLM Service

负责：

1. 调用本地 Ollama
2. 构建 Prompt
3. 返回结构化 JSON
"""

from ollama import chat

from app.ai.parser import parse_json
from app.core.config import OLLAMA_MODEL
from app.core.logger import logger


def _chat(prompt: str) -> dict:
    """
    调用 Ollama，并解析 JSON
    """

    logger.info(f"开始调用 Ollama 模型：{OLLAMA_MODEL}")

    try:

        response = chat(
            model=OLLAMA_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        logger.info("Ollama 返回成功")

        result = response.message.content

        logger.info("开始解析 AI 返回 JSON")

        data = parse_json(result)

        logger.info("JSON 解析成功")

        return data

    except Exception as e:

        logger.exception(f"Ollama 调用失败：{e}")

        raise


def extract_resume_info(text: str) -> dict:
    """
    提取简历信息
    """

    prompt = f"""
你是一名专业HR。

请从下面简历中提取信息。

要求：

1. 只返回JSON
2. 不要解释
3. 不要输出Markdown
4. skills必须是数组
5. 缺失字段填空字符串

格式：

{{
    "name":"",
    "school":"",
    "major":"",
    "research_direction":"",
    "skills":[],
    "papers":""
}}

简历：

{text}
"""

    return _chat(prompt)


def extract_jd_info(text: str) -> dict:
    """
    提取岗位JD信息
    """

    prompt = f"""
你是一名资深HR。

请阅读下面岗位JD。

提取岗位信息。

要求：

1. 只能返回JSON
2. 不要解释
3. 不要Markdown
4. skills必须是数组
5. 缺失字段填写空字符串

格式：

{{
    "position":"",
    "company":"",
    "education":"",
    "major":"",
    "experience":"",
    "skills":[],
    "salary":"",
    "city":"",
    "description":""
}}

岗位JD：

{text}
"""

    return _chat(prompt)