"""
Resume <-> JD Matcher

负责：

1. 技能匹配
2. 专业匹配
3. 学历匹配
4. 综合评分
5. AI分析摘要
"""

from app.resume.repository import get_resume_by_id
from app.jd.repository import get_job_by_id


# ==========================================================
# 学历等级
# ==========================================================

EDUCATION_LEVEL = {
    "不限": 0,
    "专科": 1,
    "大专": 1,
    "本科": 2,
    "硕士": 3,
    "博士": 4
}


# ==========================================================
# 技能匹配
# ==========================================================

def skill_match(resume, job):

    resume_skills = set(resume.get("skills", []))
    job_skills = set(job.get("skills", []))

    matched = sorted(list(resume_skills & job_skills))
    missing = sorted(list(job_skills - resume_skills))

    if len(job_skills) == 0:
        score = 100
    else:
        score = int(len(matched) / len(job_skills) * 100)

    return {
        "score": score,
        "matched": matched,
        "missing": missing
    }


# ==========================================================
# 专业匹配
# ==========================================================

def major_match(resume, job):

    resume_major = resume.get("major", "")
    job_major = job.get("major", "")

    if not job_major:
        return True

    return job_major in resume_major


# ==========================================================
# 学历匹配
# ==========================================================

def education_match(resume, job):

    resume_text = resume.get("research_direction", "")

    job_edu = job.get("education", "")

    if job_edu == "":
        return True

    resume_level = 2

    if "博士" in resume_text:
        resume_level = 4

    elif "硕士" in resume_text:
        resume_level = 3

    elif "本科" in resume_text:
        resume_level = 2

    job_level = EDUCATION_LEVEL.get(job_edu, 0)

    return resume_level >= job_level


# ==========================================================
# 综合评分
# ==========================================================

def calculate_score(skill_score, major_ok, edu_ok):

    score = skill_score * 0.7

    if major_ok:
        score += 20

    if edu_ok:
        score += 10

    return round(score, 2)


# ==========================================================
# AI摘要（规则版）
# ==========================================================

def build_summary(score, missing):

    if score >= 90:

        summary = "候选人与岗位高度匹配，建议优先进入面试。"

    elif score >= 75:

        summary = "候选人与岗位较匹配，可安排进一步沟通。"

    elif score >= 60:

        summary = "候选人与岗位基本匹配，但存在部分能力差距。"

    else:

        summary = "候选人与岗位匹配度较低。"

    if missing:

        summary += " 建议补充：" + "、".join(missing)

    return summary


# ==========================================================
# 主入口
# ==========================================================

def match_resume_job(
    resume_id: int,
    job_id: int
):

    resume = get_resume_by_id(resume_id)

    if resume is None:

        raise ValueError("Resume不存在")

    job = get_job_by_id(job_id)

    if job is None:

        raise ValueError("Job不存在")

    skill = skill_match(resume, job)

    major = major_match(resume, job)

    education = education_match(resume, job)

    score = calculate_score(

        skill["score"],

        major,

        education

    )

    summary = build_summary(

        score,

        skill["missing"]

    )

    return {

        "resume_id": resume_id,

        "job_id": job_id,

        "score": score,

        "matched_skills": skill["matched"],

        "missing_skills": skill["missing"],

        "major_match": major,

        "education_match": education,

        "summary": summary

    }


# ==========================================================
# 测试
# ==========================================================

if __name__ == "__main__":

    print(

        match_resume_job(

            1,

            1

        )

    )