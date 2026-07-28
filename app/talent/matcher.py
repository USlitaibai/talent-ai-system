"""
Talent Matcher

岗位匹配算法
"""

from typing import Dict


def calculate_match_score(
    resume: Dict,
    jd: Dict
) -> int:
    """
    根据技能计算匹配度
    """

    resume_skills = set(
        resume.get("skills", [])
    )

    jd_skills = set(
        jd.get("tags", [])
    )

    if not jd_skills:
        return 0

    matched = resume_skills & jd_skills

    score = int(
        len(matched)
        / len(jd_skills)
        * 100
    )

    return score


def match_resume(
    resume: Dict,
    jd: Dict
) -> Dict:
    """
    返回匹配结果
    """

    resume_skills = set(
        resume.get("skills", [])
    )

    jd_skills = set(
        jd.get("tags", [])
    )

    return {

        "score": calculate_match_score(
            resume,
            jd
        ),

        "matched_skills": list(
            resume_skills & jd_skills
        ),

        "missing_skills": list(
            jd_skills - resume_skills
        )

    }