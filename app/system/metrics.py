"""
System Metrics

系统运行指标统计
"""

from threading import Lock


class Metrics:

    def __init__(self):

        self.lock = Lock()

        self.data = {

            # Resume
            "resume_upload": 0,

            # Knowledge
            "knowledge_search": 0,

            # AI
            "llm_calls": 0,

            "embedding_calls": 0,

            # Cache
            "cache_hit": 0,

            "cache_miss": 0,

            # Time
            "llm_time": 0.0,

            "embedding_time": 0.0,

            "rag_time": 0.0,
        }

    # -------------------------
    # 累加
    # -------------------------

    def inc(self, key: str):

        with self.lock:

            if key in self.data:

                self.data[key] += 1

    # -------------------------
    # 累加时间
    # -------------------------

    def add_time(
        self,
        key: str,
        seconds: float
    ):

        with self.lock:

            if key in self.data:

                self.data[key] += seconds

    # -------------------------
    # 获取
    # -------------------------

    def get(self):

        with self.lock:

            result = dict(self.data)

        llm = result["llm_calls"]

        emb = result["embedding_calls"]

        result["avg_llm"] = (

            result["llm_time"] / llm

            if llm else 0

        )

        result["avg_embedding"] = (

            result["embedding_time"] / emb

            if emb else 0

        )

        total_cache = (

            result["cache_hit"]

            + result["cache_miss"]

        )

        result["cache_hit_rate"] = (

            result["cache_hit"] / total_cache

            if total_cache else 0

        )

        return result

    # -------------------------
    # 重置
    # -------------------------

    def reset(self):

        with self.lock:

            for key in self.data:

                self.data[key] = 0


metrics = Metrics()


if __name__ == "__main__":

    metrics.inc("llm_calls")

    metrics.inc("cache_hit")

    metrics.add_time("llm_time", 2.4)

    print(metrics.get())