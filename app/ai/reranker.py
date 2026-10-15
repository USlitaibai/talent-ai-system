"""
Reranker

企业级二次排序

两种模式：

1. CrossEncoder 精排（RERANK_ENABLED=true，默认）
   使用 BAAI/bge-reranker-v2-m3 对候选做语义打分。

2. RRF 排名融合兜底（RERANK_ENABLED=false）
   不加载模型，改用 Reciprocal Rank Fusion 融合
   FAISS 与 BM25 两路排名，适合容器 / 演示环境。

模型采用懒加载：只有真正调用 rerank() 时才加载，
避免 import 阶段就拖慢启动。
"""

from threading import Lock

from app.core.config import RERANK_ENABLED
from app.core.logger import logger

MODEL_NAME = "BAAI/bge-reranker-v2-m3"

# RRF 平滑常数（业界常用取值 60）
RRF_K = 60

# ==========================================================
# 模型懒加载（整个服务生命周期只加载一次）
# ==========================================================

_model = None

_model_lock = Lock()

# 模型加载失败只提示一次，避免刷日志
_load_failed = False


def _get_model():
    """
    懒加载 CrossEncoder

    失败时返回 None，由调用方走兜底排序，
    保证检索功能不会因为模型不可用而整体挂掉。
    """

    global _model, _load_failed

    if _model is not None:

        return _model

    if _load_failed:

        return None

    with _model_lock:

        if _model is not None:

            return _model

        if _load_failed:

            return None

        try:

            logger.info(f"加载 Reranker：{MODEL_NAME}")

            from sentence_transformers import CrossEncoder

            _model = CrossEncoder(MODEL_NAME)

            logger.info("Reranker 加载完成")

        except Exception as e:

            _load_failed = True

            logger.warning(
                f"Reranker 加载失败，改用 RRF 兜底排序：{e}"
            )

            return None

    return _model


# ==========================================================
# FAISS L2 距离 -> 相似度
# ==========================================================

def _distance_to_score(distance) -> float:
    """
    FAISS 返回的是 L2 距离，越小越相似
    这里转成 0~1 的相似度，便于与 BM25 分数融合
    """

    try:

        distance = float(distance)

    except (TypeError, ValueError):

        return 0.0

    if distance < 0:

        return 0.0

    return 1.0 / (1.0 + distance)


# ==========================================================
# RRF / 分数融合兜底
# ==========================================================

def _fusion_rank(
    docs: list[dict],
    top_k: int
):
    """
    无重排模型时的兜底排序

    1. RRF：按 FAISS / BM25 两路排名融合
    2. 分数融合：把两路分数归一化后相加
       （只有单路来源时 RRF 无从比较，必须靠分数）
    """

    n = len(docs)

    result = []

    for index, item in enumerate(docs):

        x = item.copy()

        # 保底名次：合并列表中的顺序（越靠前越可信）
        x["_fallback_rank"] = index

        result.append(x)

    has_vector = any(
        "score" in x and x.get("score") is not None
        for x in result
    )

    has_bm25 = any(
        "bm25_score" in x and x.get("bm25_score") is not None
        for x in result
    )

    # ------------------------------
    # 两路都有：RRF 融合
    # ------------------------------

    if has_vector and has_bm25:

        vector_ranked = sorted(
            [x for x in result if x.get("score") is not None],
            key=lambda x: x.get("score", 0),
            reverse=True
        )

        bm25_ranked = sorted(
            [x for x in result if x.get("bm25_score") is not None],
            key=lambda x: x.get("bm25_score", 0),
            reverse=True
        )

        for rank, item in enumerate(vector_ranked):

            item["_vector_rank"] = rank

        for rank, item in enumerate(bm25_ranked):

            item["_bm25_rank"] = rank

        for item in result:

            rrf = 0.0

            if item.get("_vector_rank") is not None:

                rrf += 1.0 / (RRF_K + item["_vector_rank"])

            if item.get("_bm25_rank") is not None:

                rrf += 1.0 / (RRF_K + item["_bm25_rank"])

            item["rerank_score"] = round(rrf, 6)

    # ------------------------------
    # 只有单路：分数归一化融合
    # ------------------------------

    else:

        vector_max = max(
            (_distance_to_score(x.get("score")) for x in result),
            default=0.0
        )

        bm25_max = max(
            (float(x.get("bm25_score") or 0) for x in result),
            default=0.0
        )

        for item in result:

            score = 0.0

            if item.get("score") is not None:

                sim = _distance_to_score(item.get("score"))

                if vector_max > 0:

                    score += sim / vector_max

            if item.get("bm25_score") is not None:

                bm = float(item.get("bm25_score") or 0)

                if bm25_max > 0:

                    score += bm / bm25_max

            item["rerank_score"] = round(score, 6)

    # ------------------------------
    # 清理临时字段并排序
    # ------------------------------

    for item in result:

        item.pop("_fallback_rank", None)

        item.pop("_vector_rank", None)

        item.pop("_bm25_rank", None)

    result.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    return result[:top_k]


# ==========================================================
# 统一入口
# ==========================================================

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

    返回按相关性降序的前 top_k 条，每条带 rerank_score
    """

    if not docs:

        return []

    if not RERANK_ENABLED:

        return _fusion_rank(docs, top_k)

    model = _get_model()

    # 模型不可用时静默降级，保证检索不中断
    if model is None:

        return _fusion_rank(docs, top_k)

    pairs = [
        (question, item["text"])
        for item in docs
    ]

    scores = model.predict(pairs)

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
