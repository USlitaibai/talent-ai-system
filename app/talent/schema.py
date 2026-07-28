"""
Talent Schema

人才模块数据模型
"""

from pydantic import BaseModel


class FavoriteRequest(BaseModel):
    """
    收藏人才
    """

    resume_id: int


class InterviewRequest(BaseModel):
    """
    面试人才
    """

    resume_id: int


class OfferRequest(BaseModel):
    """
    Offer人才
    """

    resume_id: int


class FilterRequest(BaseModel):
    """
    人才筛选
    """

    school: str | None = None
    major: str | None = None
    skill: str | None = None
    keyword: str | None = None