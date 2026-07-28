"""
Talent Interview

人才面试管理
"""

from app.resume.repository import get_resume_by_id

# ==========================
# 面试列表（临时）
# 后续可替换数据库
# ==========================

_interview_ids = set()


def add_interview(resume_id: int):
    """
    加入面试
    """

    resume = get_resume_by_id(resume_id)

    if resume is None:
        return False

    _interview_ids.add(resume_id)

    return True


def remove_interview(resume_id: int):
    """
    取消面试
    """

    _interview_ids.discard(resume_id)

    return True


def list_interview():
    """
    获取面试列表
    """

    result = []

    for resume_id in _interview_ids:

        resume = get_resume_by_id(resume_id)

        if resume is not None:
            result.append(resume)

    return result


def is_interview(resume_id: int):
    """
    是否进入面试
    """

    return resume_id in _interview_ids