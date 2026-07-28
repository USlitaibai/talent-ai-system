"""
Hybrid Retrieval

FAISS + BM25 + Reranker
"""

from app.ai.reranker import rerank
from app.core.logger import logger
from app.knowledge.bm25 import bm25
from app.knowledge.repository import search_by_embedding


def hybrid_search(
    question: str,
    embedding: list[float],
    top_k: int = 5,
):
    """
    Hybrid Retrieval

    top_k：
        最终返回多少条

    内部自动：
        FAISS 取 top_k*4
        BM25 取 top_k*4
        Merge
        Rerank
    """

    # ===============================
    # 为Reranker多准备一点候选
    # ===============================

    faiss_top_k = max(top_k * 4, 10)
    bm25_top_k = max(top_k * 4, 10)

    # ===============================
    # FAISS
    # ===============================

    faiss_docs = search_by_embedding(
        embedding=embedding,
        top_k=faiss_top_k
    )

    logger.info(
        f"FAISS 返回 {len(faiss_docs)} 条"
    )

    # ===============================
    # BM25
    # ===============================

    bm25_docs = bm25.search(
        question,
        top_k=bm25_top_k
    )

    logger.info(
        f"BM25 返回 {len(bm25_docs)} 条"
    )

    # ===============================
    # Merge 去重
    # ===============================

    merged = []

    seen = set()

    for doc in faiss_docs + bm25_docs:

        text = doc["text"]

        if text in seen:
            continue

        seen.add(text)

        merged.append(doc)

    logger.info(
        f"Merge 后 {len(merged)} 条"
    )

    # ===============================
    # Reranker
    # ===============================

    reranked = rerank(
        question=question,
        docs=merged,
        top_k=top_k
    )

    logger.info(
        f"Reranker 保留 {len(reranked)} 条"
    )

    return reranked


if __name__ == "__main__":

    from app.knowledge.embedding import get_embedding

    query = "谁熟悉Python开发？"

    emb = get_embedding(query)

    docs = hybrid_search(
        question=query,
        embedding=emb,
        top_k=5
    )

    print("=" * 60)

    for d in docs:
        print(d)

    print("=" * 60)