"""
AI Cache

双层缓存

L1：
    Question -> Answer

L2：
    Embedding -> Answer
"""

from collections import OrderedDict
from datetime import datetime

import numpy as np

from app.core.config import (
    STRING_CACHE_SIZE,
    SEMANTIC_CACHE_SIZE,
    SEMANTIC_CACHE_THRESHOLD,
    PRINT_CONTEXT,
)


class AICache:

    def __init__(self):

        # ==================================================
        # L1 Cache
        # ==================================================

        self.string_cache = OrderedDict()

        # ==================================================
        # Semantic Cache
        # ==================================================

        self.semantic_cache = []

    # ==========================================================
    # L1 Cache
    # ==========================================================

    def get(self, question: str):

        item = self.string_cache.get(question)

        if item is None:
            return None

        # LRU
        self.string_cache.move_to_end(question)

        return item["answer"]

    def set(
        self,
        question: str,
        answer: str
    ):

        self.string_cache[question] = {

            "answer": answer,

            "time": datetime.now()

        }

        # LRU
        self.string_cache.move_to_end(question)

        # 超过容量
        while len(self.string_cache) > STRING_CACHE_SIZE:

            self.string_cache.popitem(last=False)

    # ==========================================================
    # Cosine
    # ==========================================================

    @staticmethod
    def cosine_similarity(v1, v2):

        v1 = np.array(v1, dtype="float32")

        v2 = np.array(v2, dtype="float32")

        denominator = (

            np.linalg.norm(v1)

            *

            np.linalg.norm(v2)

        )

        if denominator == 0:

            return 0

        return float(

            np.dot(v1, v2)

            /

            denominator

        )

    # ==========================================================
    # Semantic Search
    # ==========================================================

    def semantic_search(

        self,

        embedding,

        threshold=SEMANTIC_CACHE_THRESHOLD

    ):

        best_answer = None

        best_score = 0

        for item in self.semantic_cache:

            score = self.cosine_similarity(

                embedding,

                item["embedding"]

            )

            if PRINT_CONTEXT:

                print(

                    f'Compare: {item["question"]} -> {score:.4f}'

                )

            if score > best_score:

                best_score = score

                best_answer = item["answer"]

        if PRINT_CONTEXT:

            print(

                f"Best Score = {best_score:.4f}"

            )

        if best_score >= threshold:

            if PRINT_CONTEXT:

                print(

                    f"Semantic Cache Hit: {best_score:.4f}"

                )

            return best_answer

        return None

    # ==========================================================
    # Semantic Add
    # ==========================================================

    def semantic_add(

        self,

        question,

        embedding,

        answer

    ):

        self.semantic_cache.append(

            {

                "question": question,

                "embedding": embedding,

                "answer": answer,

                "time": datetime.now()

            }

        )

        # 超过容量
        while len(self.semantic_cache) > SEMANTIC_CACHE_SIZE:

            self.semantic_cache.pop(0)

    # ==========================================================
    # Clear
    # ==========================================================

    def clear(self):

        self.string_cache.clear()

        self.semantic_cache.clear()

    # ==========================================================
    # Count
    # ==========================================================

    def string_count(self):

        return len(self.string_cache)

    def semantic_count(self):

        return len(self.semantic_cache)

    def total_count(self):

        return (

            self.string_count()

            +

            self.semantic_count()

        )


cache = AICache()


if __name__ == "__main__":

    import random

    emb = [

        random.random()

        for _ in range(768)

    ]

    cache.set(

        "谁熟悉Python",

        "张伟"

    )

    cache.semantic_add(

        "谁熟悉Python",

        emb,

        "张伟"

    )

    print("=" * 60)

    print(cache.get("谁熟悉Python"))

    print(cache.semantic_search(emb))

    print(cache.string_count())

    print(cache.semantic_count())

    print("=" * 60)