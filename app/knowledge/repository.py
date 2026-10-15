"""
Knowledge Repository

知识库数据访问层
"""

from app.core.logger import logger
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

def _locate_item(id_field: str, entity_id: int, text: str, source: str):
    """
    定位某个实体（简历/岗位）对应的知识条目

    1. 优先按实体 ID 精确匹配（存量知识可能缺少该字段，
       也可能 id 缺失，这里统一补齐后落盘）
    2. 兜底：按文本匹配并存量回填关联
    """

    meta = None

    for item in store.metadata:

        if item.get(id_field) == entity_id:

            meta = item

            break

    if meta is None:

        for item in store.metadata:

            if item.get("text") == text:

                meta = item

                break

    if meta is None:

        return None

    changed = False

    if meta.get(id_field) != entity_id:

        meta[id_field] = entity_id

        changed = True

    if not meta.get("source"):

        meta["source"] = source

        changed = True

    # 早期写入的存量知识可能没有 id，
    # 不补的话后续按 id 删除/更新会失败
    if meta.get("id") is None:

        meta["id"] = store.next_id()

        changed = True

    if changed:

        store.save()

        logger.info(
            f"回填知识关联 {id_field}={entity_id}（知识ID={meta.get('id')}）"
        )

    return meta


def update_document_by_resume(
    resume_id: int,
    text: str,
    source: str = "resume"
):
    """
    更新（或新增）某份简历对应的知识

    返回：新的知识 ID，或 None
    """

    item = _locate_item("resume_id", resume_id, text, source)

    embedding = get_embedding(text)

    if item is None:

        return store.add(
            text=text,
            embedding=embedding,
            source=source,
            resume_id=resume_id
        )

    return store.update(
        knowledge_id=item.get("id"),
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
    """
    更新（或新增）某个岗位对应的知识

    返回：新的知识 ID，或 None
    """

    item = _locate_item("job_id", job_id, text, source)

    embedding = get_embedding(text)

    if item is None:

        return store.add(
            text=text,
            embedding=embedding,
            source=source,
            job_id=job_id
        )

    return store.update(
        knowledge_id=item.get("id"),
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