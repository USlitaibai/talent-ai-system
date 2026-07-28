"""
Analysis Report

分析报告模块

负责：

1. Dashboard
2. Summary
3. Talent Profile
4. Chart
5. AI Report
"""

from datetime import datetime

from app.analysis.dashboard import dashboard

from app.analysis.analysis import (
    summary,
    talent_profile,
    chart_data,
)


# ==========================================================
# Dashboard
# ==========================================================

def dashboard_report():
    """
    Dashboard
    """

    return dashboard()


# ==========================================================
# Summary
# ==========================================================

def summary_report():
    """
    首页摘要
    """

    return summary()


# ==========================================================
# Talent Profile
# ==========================================================

def profile_report():
    """
    人才画像
    """

    return talent_profile()


# ==========================================================
# Charts
# ==========================================================

def chart_report():
    """
    图表数据
    """

    return chart_data()


# ==========================================================
# AI分析（目前规则版）
# ==========================================================

def ai_report():
    """
    AI分析报告

    后续这里可以接 Ollama。
    """

    profile = talent_profile()

    return {

        "overall":

            f"当前系统共收录 {profile['resume_count']} 份简历，"
            f"{profile['job_count']} 个岗位。",

        "resume_analysis":

            f"主要人才来自【{profile.get('top_school','')}】，"
            f"主要专业为【{profile.get('top_major','')}】，"
            f"热门技能为【{profile.get('top_skill','')}】。",

        "job_analysis":

            f"企业需求主要来自【{profile.get('top_company','')}】，"
            f"热门岗位为【{profile.get('top_position','')}】。",

        "suggestion":

            "建议持续补充岗位JD，提高岗位覆盖率；同时增加高质量简历，进一步提升知识库检索效果。"

    }


# ==========================================================
# 完整报告
# ==========================================================

def generate_report():
    """
    返回完整分析报告
    """

    return {

        "generated_at": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "dashboard": dashboard_report(),

        "summary": summary_report(),

        "profile": profile_report(),

        "charts": chart_report(),

        "ai_report": ai_report()

    }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    from pprint import pprint

    pprint(generate_report())