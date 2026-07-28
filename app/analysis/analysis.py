"""
Analysis

统一分析中心

负责：

1. Resume统计
2. JD统计
3. 人才画像
4. Dashboard图表
5. 首页摘要
"""

from collections import Counter

from app.resume.repository import (
    get_all_resumes,
)

from app.jd.repository import (
    get_all_jobs,
)


# ==========================================================
# 基础数量统计
# ==========================================================

def resume_count():
    """
    简历数量
    """

    return len(get_all_resumes())


def job_count():
    """
    岗位数量
    """

    return len(get_all_jobs())


# ==========================================================
# 学校统计
# ==========================================================

def top_schools(
    limit: int = 10
):

    counter = Counter()

    for resume in get_all_resumes():

        school = resume.get("school", "")

        if school:

            counter[school] += 1

    return counter.most_common(limit)


# ==========================================================
# 专业统计
# ==========================================================

def top_majors(
    limit: int = 10
):

    counter = Counter()

    for resume in get_all_resumes():

        major = resume.get("major", "")

        if major:

            counter[major] += 1

    return counter.most_common(limit)


# ==========================================================
# 技能统计
# ==========================================================

def top_skills(
    limit: int = 20
):

    counter = Counter()

    for resume in get_all_resumes():

        skills = resume.get(
            "skills",
            []
        )

        if isinstance(skills, str):

            skills = [skills]

        for skill in skills:

            if skill:

                counter[skill] += 1

    return counter.most_common(limit)


# ==========================================================
# 研究方向统计
# ==========================================================

def top_research(
    limit: int = 10
):

    counter = Counter()

    for resume in get_all_resumes():

        direction = resume.get(
            "research_direction",
            ""
        )

        if direction:

            counter[direction] += 1

    return counter.most_common(limit)
# ==========================================================
# 公司统计
# ==========================================================

def top_companies(
    limit: int = 10
):

    counter = Counter()

    for job in get_all_jobs():

        company = job.get("company", "")

        if company:

            counter[company] += 1

    return counter.most_common(limit)


# ==========================================================
# 岗位统计
# ==========================================================

def top_positions(
    limit: int = 10
):

    counter = Counter()

    for job in get_all_jobs():

        position = job.get("position", "")

        if position:

            counter[position] += 1

    return counter.most_common(limit)


# ==========================================================
# 城市统计
# ==========================================================

def top_cities(
    limit: int = 10
):

    counter = Counter()

    for job in get_all_jobs():

        city = job.get("city", "")

        if city:

            counter[city] += 1

    return counter.most_common(limit)


# ==========================================================
# 学历要求统计
# ==========================================================

def education_statistics():

    counter = Counter()

    for job in get_all_jobs():

        education = job.get("education", "")

        if education:

            counter[education] += 1

    return dict(counter)


# ==========================================================
# 薪资统计
# ==========================================================

def salary_statistics():

    counter = Counter()

    for job in get_all_jobs():

        salary = job.get("salary", "")

        if salary:

            counter[salary] += 1

    return dict(counter)


# ==========================================================
# 岗位技能统计
# ==========================================================

def job_skill_statistics():

    counter = Counter()

    for job in get_all_jobs():

        skills = job.get(
            "skills",
            []
        )

        if isinstance(skills, str):

            skills = [skills]

        for skill in skills:

            if skill:

                counter[skill] += 1

    return dict(counter)
# ==========================================================
# 图表数据
# ==========================================================

def chart_data():
    """
    返回前端图表数据
    """

    return {

        "schools": top_schools(),

        "majors": top_majors(),

        "skills": top_skills(),

        "research": top_research(),

        "companies": top_companies(),

        "positions": top_positions(),

        "cities": top_cities(),

        "education": education_statistics(),

        "salary": salary_statistics(),

        "job_skills": job_skill_statistics()

    }


# ==========================================================
# 人才画像
# ==========================================================

def talent_profile():
    """
    人才画像
    """

    resumes = get_all_resumes()

    jobs = get_all_jobs()

    return {

        "resume_count": len(resumes),

        "job_count": len(jobs),

        "top_school": (

            top_schools(1)[0][0]

            if top_schools(1)

            else ""

        ),

        "top_major": (

            top_majors(1)[0][0]

            if top_majors(1)

            else ""

        ),

        "top_skill": (

            top_skills(1)[0][0]

            if top_skills(1)

            else ""

        ),

        "top_company": (

            top_companies(1)[0][0]

            if top_companies(1)

            else ""

        ),

        "top_position": (

            top_positions(1)[0][0]

            if top_positions(1)

            else ""

        )

    }


# ==========================================================
# 首页摘要
# ==========================================================

def summary():
    """
    首页摘要
    """

    return {

        "resume_total": resume_count(),

        "job_total": job_count(),

        "school_total": len(top_schools()),

        "major_total": len(top_majors()),

        "company_total": len(top_companies()),

        "position_total": len(top_positions())

    }


# ==========================================================
# 测试
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)

    print("Summary")

    print(summary())

    print("=" * 60)

    print("Profile")

    print(talent_profile())

    print("=" * 60)

    print("Chart")

    print(chart_data())

    print("=" * 60)