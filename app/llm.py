import json

from ollama import chat

from app.config import OLLAMA_MODEL


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
        model=OLLAMA_MODEL,
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


if __name__ == "__main__":
    test_text = """
姓名：张伟
学校：上海交通大学
专业：计算机科学与技术
研究方向：人工智能、机器学习
技能：Python、PyTorch、深度学习
发表论文：3篇
"""

    print(extract_resume_info(test_text))