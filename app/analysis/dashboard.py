"""
Dashboard

首页仪表盘数据
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
)


def dashboard():
    """
    首页Dashboard数据
    """

    schools = top_schools(5)
    majors = top_majors(5)
    skills = top_skills(10)
    research = top_research(10)

    companies = top_companies(5)
    positions = top_positions(5)
    cities = top_cities(5)

    return {

        # =====================
        # 基础统计
        # =====================

        "resume_count": resume_count(),

        "job_count": job_count(),

        # =====================
        # 首页卡片
        # =====================

        "top_school":
            schools[0][0] if schools else "",

        "top_major":
            majors[0][0] if majors else "",

        "top_skill":
            skills[0][0] if skills else "",

        "top_company":
            companies[0][0] if companies else "",

        "top_position":
            positions[0][0] if positions else "",

        # =====================
        # 图表
        # =====================

        "top_schools": schools,

        "top_majors": majors,

        "top_skills": skills,

        "top_research": research,

        "top_companies": companies,

        "top_positions": positions,

        "top_cities": cities,

    }


if __name__ == "__main__":

    from pprint import pprint

    pprint(dashboard())