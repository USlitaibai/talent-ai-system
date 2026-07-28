"""
Talent Filter

人才筛选模块
"""

from app.resume.repository import get_all_resumes


def filter_resume(
    school: str | None = None,
    major: str | None = None,
    skill: str | None = None,
    keyword: str | None = None,
):
    """
    根据条件筛选人才
    """

    resumes = get_all_resumes()

    result = []

    for resume in resumes:

        # 学校
        if school:
            if school not in (resume.school or ""):
                continue

        # 专业
        if major:
            if major not in (resume.major or ""):
                continue

        # 技能
        if skill:
            if skill not in (resume.skills or ""):
                continue

        # 综合关键字
        if keyword:

            text = " ".join(
                [
                    resume.name or "",
                    resume.school or "",
                    resume.major or "",
                    resume.research_direction or "",
                    resume.skills or "",
                    resume.papers or "",
                ]
            )

            if keyword not in text:
                continue

        result.append(resume)

    return result