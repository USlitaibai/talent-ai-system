"""
Talent Offer

人才录用管理
"""

from app.resume.repository import get_resume_by_id

# ==========================
# Offer列表（临时）
# 后续可替换数据库
# ==========================

_offer_ids = set()


def add_offer(resume_id: int):
    """
    发放 Offer
    """

    resume = get_resume_by_id(resume_id)

    if resume is None:
        return False

    _offer_ids.add(resume_id)

    return True


def remove_offer(resume_id: int):
    """
    撤销 Offer
    """

    _offer_ids.discard(resume_id)

    return True


def list_offer():
    """
    获取 Offer 列表
    """

    result = []

    for resume_id in _offer_ids:

        resume = get_resume_by_id(resume_id)

        if resume is not None:
            result.append(resume)

    return result


def is_offer(resume_id: int):
    """
    是否已发 Offer
    """

    return resume_id in _offer_ids