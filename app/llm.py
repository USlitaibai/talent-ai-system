import json
from ollama import chat


def extract_resume_info(text: str) -> dict:
    """
    调用本地 Ollama 模型提取简历信息
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

    response = chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    result = response.message.content.strip()

    # 去掉 Markdown
    result = result.replace("```json", "")
    result = result.replace("```", "")
    result = result.strip()

    return json.loads(result)