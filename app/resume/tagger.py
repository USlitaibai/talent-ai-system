"""
AI人才标签模块

以后所有标签统一从这里生成。
"""

from typing import List


TAG_RULES = {

    "Python": [
        "Python",
        "Flask",
        "Django",
        "FastAPI"
    ],

    "Java": [
        "Java",
        "Spring",
        "SpringBoot"
    ],

    "AI": [
        "人工智能",
        "机器学习",
        "深度学习",
        "神经网络"
    ],

    "LLM": [
        "大模型",
        "LLM",
        "LangChain",
        "RAG",
        "Prompt"
    ],

    "CV": [
        "OpenCV",
        "目标检测",
        "图像识别",
        "YOLO"
    ],

    "NLP": [
        "NLP",
        "自然语言处理",
        "文本分类"
    ],

    "数据库": [
        "MySQL",
        "Redis",
        "MongoDB"
    ],

    "数据分析": [
        "Pandas",
        "NumPy",
        "Matplotlib"
    ]

}


def generate_tags(resume: dict) -> List[str]:
    """
    根据技能和研究方向生成标签
    """

    tags = []

    text = ""

    skills = resume.get("skills", [])

    if isinstance(skills, list):

        text += " ".join(skills)

    text += " "

    text += resume.get(
        "research_direction",
        ""
    )

    for tag, keywords in TAG_RULES.items():

        for keyword in keywords:

            if keyword.lower() in text.lower():

                tags.append(tag)

                break

    return sorted(
        list(
            set(tags)
        )
    )