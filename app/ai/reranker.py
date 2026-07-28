"""
Reranker

企业级二次排序
"""

from sentence_transformers import CrossEncoder

from app.core.logger import logger

MODEL_NAME = "BAAI/bge-reranker-v2-m3"

# ==========================================================
# 全局加载（整个服务生命周期只加载一次）
# ==========================================================

logger.info("加载 Reranker ...")

_model = CrossEncoder(MODEL_NAME)

logger.info("Reranker 加载完成")


def rerank(
    question: str,
    docs: list[dict],
    top_k: int = 5
):
    """
    docs:

    [
        {"text":"..."},
        {"text":"..."}
    ]
    """

    if not docs:
        return []

    pairs = [
        (question, item["text"])
        for item in docs
    ]

    scores = _model.predict(pairs)

    result = []

    for item, score in zip(docs, scores):

        x = item.copy()

        x["rerank_score"] = float(score)

        result.append(x)

    result.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return result[:top_k]


if __name__ == "__main__":

    docs = [

        {"text": "张伟 熟悉 Python FastAPI Docker"},

        {"text": "李四 熟悉 Java Spring"},

        {"text": "王五 熟悉 Python 深度学习"}

    ]

    result = rerank(
        "谁熟悉Python开发？",
        docs
    )

    print("=" * 60)

    for item in result:
        print(item)

    print("=" * 60)