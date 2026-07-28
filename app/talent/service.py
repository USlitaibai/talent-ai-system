"""
Talent Service

人才业务层
"""

from app.talent.search import search
from app.talent.ranking import rank_resumes
from app.talent.recommender import generate_recommendation


def search_talent(keyword: str):
    """
    搜索人才
    """
    return search(keyword)


def rank_talent(jd: dict):
    """
    人才排序
    """
    return rank_resumes(jd)


def recommend_talent(resume: dict, jd: dict):
    """
    AI 推荐
    """
    return generate_recommendation(resume, jd)