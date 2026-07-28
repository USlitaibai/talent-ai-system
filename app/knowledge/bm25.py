"""
BM25 Retriever

关键词检索
"""

from rank_bm25 import BM25Okapi
import jieba

from app.knowledge.repository import list_documents
from app.core.logger import logger


class BM25Retriever:

    def __init__(self):

        self.documents = []
        self.corpus = []
        self.bm25 = None

        # ==========================
        # 启动时直接建立索引
        # ==========================
        self.build()

    # ==========================================================
    # 构建索引
    # ==========================================================

    def build(self):

        self.documents = list_documents()

        self.corpus = []

        for item in self.documents:

            text = item["text"]

            tokens = list(
                jieba.cut(
                    text.lower()
                )
            )

            self.corpus.append(tokens)

        if self.corpus:

            self.bm25 = BM25Okapi(self.corpus)

            logger.info(
                f"BM25 建立完成 ({len(self.corpus)} 条)"
            )

        else:

            self.bm25 = None

            logger.info(
                "BM25 建立完成 (0 条)"
            )

    # ==========================================================
    # 刷新索引
    # ==========================================================

    def refresh(self):
        """
        新增、删除、更新知识后调用
        """
        self.build()

    # ==========================================================
    # 搜索
    # ==========================================================

    def search(
        self,
        query: str,
        top_k: int = 5
    ):

        if self.bm25 is None:
            return []

        query_tokens = list(
            jieba.cut(
                query.lower()
            )
        )

        scores = self.bm25.get_scores(
            query_tokens
        )

        ranked = sorted(
            zip(scores, self.documents),
            key=lambda x: x[0],
            reverse=True
        )

        result = []

        for score, item in ranked[:top_k]:

            doc = item.copy()

            doc["bm25_score"] = float(score)

            result.append(doc)

        return result


bm25 = BM25Retriever()


if __name__ == "__main__":

    docs = bm25.search(

        "Python FastAPI",

        top_k=5

    )

    print()

    print("=" * 60)

    for doc in docs:

        print(doc)

    print("=" * 60)