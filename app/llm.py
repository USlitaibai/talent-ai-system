from ollama import chat


def extract_resume_info(text: str):
    prompt = f"""
你现在是一名专业的人才信息抽取助手。

请从下面简历中提取信息。

要求：
1. 只返回JSON。
2. 不要解释。
3. 没有的信息填写空字符串。
4. skills返回数组。

格式如下：

{{
    "name":"",
    "school":"",
    "major":"",
    "research_direction":"",
    "skills":[],
    "papers":""
}}

简历内容：

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

    return response.message.content


if __name__ == "__main__":

    resume = """
姓名：张伟

学校：上海交通大学

专业：计算机科学与技术

研究方向：人工智能、机器学习

技能：
Python
PyTorch
深度学习

论文：
3篇
"""

    result = extract_resume_info(resume)

    print(result)