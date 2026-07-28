"""
Review Core

简历评审核心
"""


def review_resume(resume: dict):
    """
    简历评审

    返回：
    {
        score: 总分,
        advantages: [],
        disadvantages: [],
        suggestion: ""
    }
    """

    score = 0

    advantages = []
    disadvantages = []

    # ==========================
    # 学校
    # ==========================

    school = resume.get("school", "")

    if school:
        score += 20
        advantages.append("具有完整教育背景")
    else:
        disadvantages.append("缺少学校信息")

    # ==========================
    # 专业
    # ==========================

    major = resume.get("major", "")

    if major:
        score += 15
    else:
        disadvantages.append("缺少专业信息")

    # ==========================
    # 技能
    # ==========================

    skills = resume.get("skills", [])

    if isinstance(skills, str):
        skills = [skills]

    score += min(len(skills) * 10, 30)

    if len(skills) >= 3:
        advantages.append("技能较丰富")
    else:
        disadvantages.append("技能数量较少")

    # ==========================
    # 论文
    # ==========================

    papers = resume.get("papers", "")

    if papers:
        score += 15
        advantages.append("具有科研成果")

    # ==========================
    # 研究方向
    # ==========================

    if resume.get("research_direction"):
        score += 20

    # ==========================
    # 建议
    # ==========================

    if score >= 90:
        suggestion = "建议优先录用"

    elif score >= 75:
        suggestion = "建议安排面试"

    elif score >= 60:
        suggestion = "可以进入人才库继续观察"

    else:
        suggestion = "建议继续完善简历"

    return {
        "score": score,
        "advantages": advantages,
        "disadvantages": disadvantages,
        "suggestion": suggestion,
    }


if __name__ == "__main__":

    demo = {
        "school": "上海交通大学",
        "major": "计算机科学",
        "research_direction": "人工智能",
        "skills": [
            "Python",
            "FastAPI",
            "Docker",
        ],
        "papers": "3篇",
    }

    print(review_resume(demo))