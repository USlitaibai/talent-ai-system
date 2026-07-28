"""
Knowledge Chat

知识库聊天模块

负责：

1. 接收用户问题
2. 调用 RAG
3. 返回回答
"""

from app.ai.rag import ask


def chat(question: str) -> str:
    """
    知识库问答
    """

    return ask(question)


if __name__ == "__main__":

    print("=" * 60)

    answer = chat(
        "熟悉Python开发的人有哪些？"
    )

    print(answer)

    print("=" * 60)