"""
Knowledge Service

知识库业务层
"""

import time

from app.ai.cache import cache
from app.ai.llm import get_client
from app.ai.prompt import build_rag_prompt

from app.core.config import (
    OLLAMA_MODEL,
    RAG_MAX_CONTEXT_LINES,
    PRINT_CONTEXT,
)

from app.core.logger import logger

from app.knowledge.embedding import get_embedding
from app.knowledge.compressor import compress_context

# Hybrid Retrieval
from app.knowledge.hybrid import hybrid_search

from app.system.metrics import metrics


def ask(question: str):
    """
    RAG问答
    """

    rag_start = time.perf_counter()

    # =====================================================
    # L1 Cache
    # =====================================================

    answer = cache.get(question)

    if answer is not None:

        logger.info("命中 L1 Cache")

        metrics.inc("cache_hit")

        metrics.add_time(
            "rag_time",
            time.perf_counter() - rag_start
        )

        return {
            "question": question,
            "context": "L1 Cache",
            "answer": answer
        }

    metrics.inc("cache_miss")

    # =====================================================
    # Embedding
    # =====================================================

    question_embedding = get_embedding(question)

    # =====================================================
    # Semantic Cache
    # =====================================================

    answer = cache.semantic_search(question_embedding)

    if answer is not None:

        logger.info("命中 Semantic Cache")

        metrics.inc("cache_hit")

        cache.set(question, answer)

        metrics.add_time(
            "rag_time",
            time.perf_counter() - rag_start
        )

        return {
            "question": question,
            "context": "Semantic Cache",
            "answer": answer
        }

    # =====================================================
    # Hybrid Retrieval
    # =====================================================

    logger.info("开始 Hybrid Retrieval")

    docs = hybrid_search(
        question=question,
        embedding=question_embedding,
        top_k=5
    )

    context = "\n\n".join(
        item["text"]
        for item in docs
    )

    # =====================================================
    # Context Compress
    # =====================================================

    context = compress_context(
        context,
        max_lines=RAG_MAX_CONTEXT_LINES
    )

    if PRINT_CONTEXT:

        print("=" * 60)
        print("Knowledge Context:")
        print(context)
        print("=" * 60)

    if not context.strip():

        metrics.add_time(
            "rag_time",
            time.perf_counter() - rag_start
        )

        return {
            "question": question,
            "context": "",
            "answer": "知识库中暂无相关信息。"
        }

    # =====================================================
    # Prompt
    # =====================================================

    prompt = build_rag_prompt(
        question,
        context
    )

    # =====================================================
    # LLM
    # =====================================================

    logger.info("开始调用LLM")

    llm_start = time.perf_counter()

    response = get_client().chat(
        model=OLLAMA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    llm_elapsed = time.perf_counter() - llm_start

    metrics.inc("llm_calls")

    metrics.add_time(
        "llm_time",
        llm_elapsed
    )

    logger.info(
        f"LLM耗时: {llm_elapsed:.3f}s"
    )

    answer = response.message.content.strip()

    logger.info("RAG回答完成")

    # =====================================================
    # Cache
    # =====================================================

    cache.set(
        question,
        answer
    )

    cache.semantic_add(
        question,
        question_embedding,
        answer
    )

    rag_elapsed = time.perf_counter() - rag_start

    metrics.add_time(
        "rag_time",
        rag_elapsed
    )

    logger.info(
        f"RAG耗时: {rag_elapsed:.3f}s"
    )

    return {
        "question": question,
        "context": context,
        "answer": answer
    }


if __name__ == "__main__":

    print("=" * 60)

    result = ask(
        "谁熟悉Python开发？"
    )

    print(result["answer"])

    print("=" * 60)

    print("Metrics:")

    print(metrics.get())

    print("=" * 60)