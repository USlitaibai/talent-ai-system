"""
Query Rewrite

查询改写
"""

from app.ai.llm import get_client
from app.core.config import OLLAMA_MODEL
from app.core.logger import logger


SYSTEM_PROMPT = """
你是一名HR检索助手。

请把用户问题改写成最适合知识库检索的一句话。

要求：

1 不回答问题

2 不解释

3 不扩写太长

4 保留关键词

5 输出一句话即可
"""


def rewrite(question: str):

    logger.info("开始 Query Rewrite")

    response = get_client().chat(

        model=OLLAMA_MODEL,

        messages=[

            {

                "role": "system",

                "content": SYSTEM_PROMPT

            },

            {

                "role": "user",

                "content": question

            }

        ]

    )

    result = response.message.content.strip()

    logger.info(f"Rewrite -> {result}")

    return result


if __name__ == "__main__":

    print("=" * 60)

    print(
        rewrite(
            "谁熟悉Python？"
        )
    )

    print("=" * 60)