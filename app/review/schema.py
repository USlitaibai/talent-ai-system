"""
Review Schema

人工审核数据模型
"""

from typing import List

from pydantic import BaseModel, Field


# ==========================================================
# 修改简历
# ==========================================================

class ReviewUpdate(BaseModel):
    """
    HR修改后的简历信息
    """

    name: str = Field(
        ...,
        description="姓名"
    )

    school: str = Field(
        ...,
        description="学校"
    )

    major: str = Field(
        ...,
        description="专业"
    )

    research_direction: str = Field(
        ...,
        description="研究方向"
    )

    skills: List[str] = Field(
        default_factory=list,
        description="技能列表"
    )

    papers: str = Field(
        default="",
        description="论文情况"
    )


# ==========================================================
# 简历详情
# ==========================================================

class ReviewDetail(BaseModel):
    """
    简历详情
    """

    id: int

    name: str

    school: str

    major: str

    research_direction: str

    skills: List[str]

    papers: str

    created_at: str

    class Config:
        from_attributes = True


# ==========================================================
# 修改结果
# ==========================================================

class ReviewResponse(BaseModel):
    """
    修改返回
    """

    id: int

    status: str

    message: str | None = None


# ==========================================================
# 数量统计
# ==========================================================

class ReviewCount(BaseModel):
    """
    简历数量
    """

    count: int