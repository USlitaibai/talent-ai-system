"""
Talent Ranking

人才排序模块
"""

from app.talent.matcher import match_resume
from app.talent.repository import get_all_resumes


def rank_resumes(jd: dict):
    """
    根据岗位要求对候选人排序
    """

    resumes = get_all_resumes()

    ranking = []

    for resume in resumes:

        result = match_resume(
            resume,
            jd
        )

        ranking.append(
            {
                "id": resume["id"],
                "name": resume["name"],
                "school": resume["school"],
                "major": resume["major"],
                "score": result["score"],
                "matched_skills": result["matched_skills"],
                "missing_skills": result["missing_skills"]
            }
        )

    ranking.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return ranking