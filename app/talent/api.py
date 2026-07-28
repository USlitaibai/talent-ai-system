"""
Talent API

人才相关接口
"""

from fastapi import APIRouter

from app.common.response import success
from app.talent.service import (
    search_talent,
    rank_talent,
    recommend_talent
)

router = APIRouter(
    prefix="/talent",
    tags=["Talent"]
)


@router.get("/search")
def search(keyword: str):
    """
    搜索人才
    """

    return success(
        search_talent(keyword)
    )


@router.post("/ranking")
def ranking(jd: dict):
    """
    人才排序
    """

    return success(
        rank_talent(jd)
    )


@router.post("/recommend")
def recommend(
    resume: dict,
    jd: dict
):
    """
    AI 推荐
    """

    return success(
        recommend_talent(
            resume,
            jd
        )
    )