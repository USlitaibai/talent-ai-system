"""
Knowledge API

知识库接口

负责：

1. 新增知识
2. 检索知识
3. RAG问答
4. 删除知识
5. 查询知识数量
"""

from fastapi import APIRouter, HTTPException

from app.common.response import success
from app.knowledge.repository import (
    add_document,
    delete_document,
    document_count,
)
from app.knowledge.retriever import retrieve
from app.knowledge.service import ask

router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge"]
)


@router.post("/add")
def add_api(text: str):
    """
    新增知识
    """

    ok = add_document(text)

    if not ok:

        raise HTTPException(
            status_code=400,
            detail="知识已存在"
        )

    return success(
        message="知识添加成功"
    )


@router.get("/search")
def search_api(
    keyword: str,
    top_k: int = 5
):
    """
    检索知识
    """

    result = retrieve(
        question=keyword,
        top_k=top_k
    )

    return success(
        data=result
    )


@router.post("/chat")
def chat_api(question: str):
    """
    RAG问答
    """

    result = ask(question)

    return success(
        data=result
    )


@router.delete("/delete/{knowledge_id}")
def delete_api(
    knowledge_id: int
):
    """
    删除知识
    """

    ok = delete_document(
        knowledge_id
    )

    if not ok:

        raise HTTPException(
            status_code=404,
            detail="知识不存在"
        )

    return success(
        message="删除成功"
    )


@router.get("/count")
def count_api():
    """
    知识数量
    """

    return success(
        data={
            "count": document_count()
        }
    )


if __name__ == "__main__":

    print("=" * 60)

    print(router)

    print("=" * 60)