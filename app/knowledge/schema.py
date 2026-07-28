"""
Knowledge Schema

知识库数据结构
"""

from pydantic import BaseModel, Field


# ==========================================================
# 新增知识
# ==========================================================

class KnowledgeCreate(BaseModel):
    """
    新增知识
    """

    text: str = Field(
        ...,
        description="知识内容"
    )

    source: str = Field(
        default="resume",
        description="知识来源"
    )


# ==========================================================
# 更新知识
# ==========================================================

class KnowledgeUpdate(BaseModel):
    """
    更新知识
    """

    text: str = Field(
        ...,
        description="新的知识内容"
    )

    source: str = Field(
        default="resume",
        description="知识来源"
    )


# ==========================================================
# 相似搜索
# ==========================================================

class KnowledgeSearch(BaseModel):
    """
    相似搜索
    """

    query: str = Field(
        ...,
        description="搜索内容"
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="返回数量"
    )


# ==========================================================
# RAG问答
# ==========================================================

class KnowledgeChat(BaseModel):
    """
    RAG问答
    """

    question: str = Field(
        ...,
        description="用户问题"
    )


# ==========================================================
# 返回结果
# ==========================================================

class KnowledgeResponse(BaseModel):
    """
    查询结果
    """

    id: int | None = None

    source: str | None = None

    text: str

    score: float | None = None

    created_at: str | None = None

    class Config:
        from_attributes = True


# ==========================================================
# 知识统计
# ==========================================================

class KnowledgeCount(BaseModel):
    """
    知识数量
    """

    count: int