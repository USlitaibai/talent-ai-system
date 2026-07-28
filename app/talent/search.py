"""
Talent Search

人才搜索模块
"""

from app.talent.repository import search_resume


def search(keyword: str):
    """
    人才搜索业务
    """

    return search_resume(keyword)