"""
Statistics

统计模块

负责：

1. Resume统计
2. JD统计
3. Dashboard统计
"""

from app.analysis.analysis import (
    resume_count,
    job_count,
    top_schools,
    top_majors,
    top_skills,
    top_research,
    top_companies,
    top_positions,
    top_cities,
    education_statistics,
    salary_statistics,
    job_skill_statistics,
)


# ==========================================================
# 总览
# ==========================================================

def overview():
    """
    返回统计总览
    """

    return {

        # ==========================
        # 数量统计
        # ==========================

        "resume_count": resume_count(),

        "job_count": job_count(),

        # ==========================
        # Resume统计
        # ==========================

        "schools": dict(top_schools()),

        "majors": dict(top_majors()),

        "skills": dict(top_skills()),

        "research": dict(top_research()),

        # ==========================
        # JD统计
        # ==========================

        "companies": dict(top_companies()),

        "positions": dict(top_positions()),

        "cities": dict(top_cities()),

        "education": education_statistics(),

        "salary": salary_statistics(),

        "job_skills": job_skill_statistics(),

    }


# ==========================================================
# 测试
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(overview())