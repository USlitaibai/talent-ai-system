"""
Knowledge Vector Store

基于 FAISS 的本地向量数据库
"""

import json
from datetime import datetime
from pathlib import Path

import faiss
import numpy as np

from app.core.logger import logger

# ==========================================================
# 数据目录
# ==========================================================

BASE = Path(__file__).resolve().parent.parent.parent

VECTOR_DIR = BASE / "data" / "vectors"
VECTOR_DIR.mkdir(parents=True, exist_ok=True)

INDEX_PATH = VECTOR_DIR / "resume.index"
META_PATH = VECTOR_DIR / "resume.metadata.json"


class VectorStore:
    """
    本地 FAISS 向量数据库
    """

    def __init__(self, dimension: int = 768):

        self.dimension = dimension

        # ==========================
        # 加载索引
        # ==========================

        if INDEX_PATH.exists():

            logger.info("加载 FAISS 索引")

            self.index = faiss.read_index(
                str(INDEX_PATH)
            )

        else:

            logger.info("创建新的 FAISS 索引")

            self.index = faiss.IndexFlatL2(
                dimension
            )

        # ==========================
        # 加载元数据
        # ==========================

        if META_PATH.exists():

            with open(
                META_PATH,
                "r",
                encoding="utf-8"
            ) as f:

                self.metadata = json.load(f)

        else:

            self.metadata = []

    # ==========================================================
    # 保存
    # ==========================================================

    def save(self):

        faiss.write_index(
            self.index,
            str(INDEX_PATH)
        )

        with open(
            META_PATH,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.metadata,
                f,
                ensure_ascii=False,
                indent=4
            )

        logger.info("FAISS 已保存")

    # ==========================================================
    # 自动生成ID
    # ==========================================================

    def next_id(self):

        if not self.metadata:
            return 1

        return max(
            item.get("id", 0)
            for item in self.metadata
        ) + 1

    # ==========================================================
    # 判断重复
    # ==========================================================

    def exists(
        self,
        text: str
    ):

        for item in self.metadata:

            if item["text"] == text:
                return True

        return False

    # ==========================================================
    # 添加知识
    # ==========================================================

    def add(
        self,
        text: str,
        embedding: list[float],
        source: str = "resume",
        resume_id: int | None = None,
        job_id: int | None = None
    ):

        if self.exists(text):

            logger.info("知识已存在，跳过")

            return False

        vector = np.array(
            [embedding],
            dtype="float32"
        )

        self.index.add(vector)

        self.metadata.append({

            "id": self.next_id(),

            "source": source,

            "resume_id": resume_id,

            "job_id": job_id,

            "text": text,

            "created_at": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        })

        self.save()

        logger.info("新增知识成功")

        return True

    # ==========================================================
    # Resume 查询
    # ==========================================================

    def find_by_resume(
        self,
        resume_id: int
    ):

        for item in self.metadata:

            if item.get("resume_id") == resume_id:

                return item

        return None

    # ==========================================================
    # Job 查询
    # ==========================================================

    def find_by_job(
        self,
        job_id: int
    ):

        for item in self.metadata:

            if item.get("job_id") == job_id:

                return item

        return None

    # ==========================================================
    # 搜索
    # ==========================================================

    def search(
        self,
        embedding: list[float],
        top_k: int = 5
    ):

        if self.index.ntotal == 0:

            return []

        vector = np.array(
            [embedding],
            dtype="float32"
        )

        distances, indices = self.index.search(

            vector,

            min(
                top_k,
                self.index.ntotal
            )

        )

        result = []

        for distance, idx in zip(

            distances[0],

            indices[0]

        ):

            if idx == -1:
                continue

            item = self.metadata[idx].copy()

            item["score"] = float(distance)

            result.append(item)

        return result
    
    # ==========================================================
    # 根据 Resume 删除
    # ==========================================================

    def delete_by_resume(
        self,
        resume_id: int
    ):

        item = self.find_by_resume(resume_id)

        if item is None:
            return False

        return self.delete(item["id"])

    # ==========================================================
    # 根据 Job 删除
    # ==========================================================

    def delete_by_job(
        self,
        job_id: int
    ):

        item = self.find_by_job(job_id)

        if item is None:
            return False

        return self.delete(item["id"])

    # ==========================================================
    # 删除知识
    # ==========================================================

    def delete(
        self,
        knowledge_id: int
    ):

        new_metadata = []

        vectors = []

        deleted = False

        for i, item in enumerate(self.metadata):

            if item["id"] == knowledge_id:

                deleted = True

                continue

            new_metadata.append(item)

            vectors.append(
                self.index.reconstruct(i)
            )

        if not deleted:

            return False

        self.index = faiss.IndexFlatL2(
            self.dimension
        )

        if vectors:

            self.index.add(

                np.array(
                    vectors,
                    dtype="float32"
                )

            )

        self.metadata = new_metadata

        self.save()

        logger.info("删除知识成功")

        return True

    # ==========================================================
    # 更新知识
    # ==========================================================

    def update(
        self,
        knowledge_id: int,
        new_text: str,
        embedding: list[float],
        source: str = "resume",
        resume_id: int | None = None,
        job_id: int | None = None
    ):

        self.delete(
            knowledge_id
        )

        self.add(
            text=new_text,
            embedding=embedding,
            source=source,
            resume_id=resume_id,
            job_id=job_id
        )

    # ==========================================================
    # 数量
    # ==========================================================

    def count(self):

        return self.index.ntotal


# ==========================================================
# 测试
# ==========================================================

if __name__ == "__main__":

    from app.knowledge.embedding import get_embedding

    store = VectorStore()

    text = "Python FastAPI Docker MySQL"

    embedding = get_embedding(text)

    store.add(
        text=text,
        embedding=embedding,
        source="resume",
        resume_id=1
    )

    print("=" * 60)

    print("知识数量：", store.count())

    print("=" * 60)

    result = store.search(
        embedding,
        top_k=3
    )

    print(result)