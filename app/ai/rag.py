"""
RAG Pipeline

负责：

1. 检索知识
2. 查询AI缓存
3. 命中缓存直接返回
4. 未命中调用LLM
5. 写入缓存
"""

from ollama import chat

from app.ai.cache import cache
from app.ai.prompt import chat_prompt
from app.core.config import OLLAMA_MODEL
from app.core.logger import logger
from app.knowledge.retriever import retrieve_context


def ask(question: str):
    """
    RAG问答
    """

    logger.info("开始知识库检索")

    context = retrieve_context(question)

    print("=" * 60)
    print("Knowledge Context:")
    print(context)
    print("=" * 60)

    # ==================================================
    # 查询缓存
    # ==================================================

    answer = cache.get(
        question,
        context
    )

    if answer:

        logger.info("命中AI缓存")

        return {
            "question": question,
            "context": context,
            "answer": answer,
            "cache": True
        }

    # ==================================================
    # 构建Prompt
    # ==================================================

    prompt = chat_prompt(
        question=question,
        context=context
    )

    logger.info("开始调用LLM")

    response = chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    answer = response.message.content.strip()

    logger.info("LLM回答完成")

    # ==================================================
    # 写入缓存
    # ==================================================

    cache.set(
        question,
        context,
        answer
    )

    logger.info("已写入AI缓存")

    return {
        "question": question,
        "context": context,
        "answer": answer,
        "cache": False
    }


if __name__ == "__main__":

    print("=" * 60)

    result = ask(
        "谁熟悉Python开发？"
    )

    print("Question:")
    print(result["question"])

    print("=" * 60)

    print("Answer:")
    print(result["answer"])

    print("=" * 60)

    print("Cache:")
    print(result["cache"])

    print("=" * 60)

    print("第二次测试（应该命中缓存）")

    result = ask(
        "谁熟悉Python开发？"
    )

    print(result["answer"])

    print("=" * 60)

    print("Cache:")
    print(result["cache"])

    print("=" * 60)