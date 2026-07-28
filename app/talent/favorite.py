"""
Talent Favorite

人才收藏模块
"""

from app.resume.repository import get_resume_by_id

# ==========================
# 收藏列表（临时）
# 后续可替换为数据库
# ==========================

_favorite_ids = set()


def add_favorite(resume_id: int):
    """
    收藏人才
    """

    resume = get_resume_by_id(resume_id)

    if resume is None:
        return False

    _favorite_ids.add(resume_id)

    return True


def remove_favorite(resume_id: int):
    """
    取消收藏
    """

    _favorite_ids.discard(resume_id)

    return True


def list_favorite():
    """
    获取收藏列表
    """

    result = []

    for resume_id in _favorite_ids:

        resume = get_resume_by_id(resume_id)

        if resume is not None:
            result.append(resume)

    return result


def is_favorite(resume_id: int):
    """
    是否已收藏
    """

    return resume_id in _favorite_ids