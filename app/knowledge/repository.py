"""
Knowledge Repository

知识库数据访问层
"""

from app.knowledge.embedding import get_embedding
from app.knowledge.vector_store import VectorStore

store = VectorStore()


# ==========================================================
# 新增
# ==========================================================

def add_document(
    text: str,
    source: str = "resume",
    resume_id: int | None = None,
    job_id: int | None = None
):
    """
    添加知识
    """

    embedding = get_embedding(text)

    return store.add(
        text=text,
        embedding=embedding,
        source=source,
        resume_id=resume_id,
        job_id=job_id
    )


# ==========================================================
# 删除
# ==========================================================

def delete_document(
    knowledge_id: int
):

    return store.delete(
        knowledge_id
    )


# ==========================================================
# 更新
# ==========================================================

def update_document(
    knowledge_id: int,
    text: str,
    source: str = "resume",
    resume_id: int | None = None,
    job_id: int | None = None
):

    embedding = get_embedding(text)

    return store.update(
        knowledge_id=knowledge_id,
        new_text=text,
        embedding=embedding,
        source=source,
        resume_id=resume_id,
        job_id=job_id
    )


# ==========================================================
# 搜索
# ==========================================================

def search_document(
    query: str,
    top_k: int = 5
):

    embedding = get_embedding(query)

    return store.search(
        embedding=embedding,
        top_k=top_k
    )


# ==========================================================
# 已有Embedding搜索
# ==========================================================

def search_by_embedding(
    embedding: list[float],
    top_k: int = 5
):

    return store.search(
        embedding=embedding,
        top_k=top_k
    )


# ==========================================================
# 数量
# ==========================================================

def document_count():

    return store.count()


# ==========================================================
# 全部
# ==========================================================

def list_documents():

    return store.metadata


# ==========================================================
# 根据ID查询
# ==========================================================

def get_document(
    knowledge_id: int
):

    for item in store.metadata:

        if item["id"] == knowledge_id:

            return item

    return None


# ==========================================================
# Resume 更新
# ==========================================================

def update_document_by_resume(
    resume_id: int,
    text: str,
    source: str = "resume"
):

    item = store.find_by_resume(resume_id)

    embedding = get_embedding(text)

    if item is None:

        return store.add(
            text=text,
            embedding=embedding,
            source=source,
            resume_id=resume_id
        )

    return store.update(
        knowledge_id=item["id"],
        new_text=text,
        embedding=embedding,
        source=source,
        resume_id=resume_id
    )


# ==========================================================
# Resume 删除
# ==========================================================

def delete_document_by_resume(
    resume_id: int
):

    return store.delete_by_resume(resume_id)


# ==========================================================
# Job 更新
# ==========================================================

def update_document_by_job(
    job_id: int,
    text: str,
    source: str = "job"
):

    item = store.find_by_job(job_id)

    embedding = get_embedding(text)

    if item is None:

        return store.add(
            text=text,
            embedding=embedding,
            source=source,
            job_id=job_id
        )

    return store.update(
        knowledge_id=item["id"],
        new_text=text,
        embedding=embedding,
        source=source,
        job_id=job_id
    )


# ==========================================================
# Job 删除
# ==========================================================

def delete_document_by_job(
    job_id: int
):

    return store.delete_by_job(job_id)