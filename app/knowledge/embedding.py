"""
Knowledge Embedding

负责生成文本向量（Embedding）
"""

import time

from ollama import embed

from app.core.config import OLLAMA_EMBED_MODEL
from app.core.logger import logger
from app.system.metrics import metrics


def get_embedding(text: str) -> list[float]:
    """
    生成文本向量
    """

    start = time.perf_counter()

    logger.info(f"Embedding: {OLLAMA_EMBED_MODEL}")

    response = embed(
        model=OLLAMA_EMBED_MODEL,
        input=text
    )

    elapsed = time.perf_counter() - start

    # ==========================
    # Metrics
    # ==========================

    metrics.inc("embedding_calls")

    metrics.add_time(
        "embedding_time",
        elapsed
    )

    logger.info(
        f"Embedding耗时: {elapsed:.3f}s"
    )

    return response["embeddings"][0]


if __name__ == "__main__":

    vector = get_embedding(
        "Python 开发工程师，熟悉 FastAPI、MySQL、Docker"
    )

    print("=" * 60)

    print(type(vector))

    print(len(vector))

    print(vector[:10])

    print("=" * 60)

    print(metrics.get())