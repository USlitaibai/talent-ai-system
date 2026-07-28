"""
Analysis Service

分析业务层

负责：

1. Dashboard
2. 人才画像
3. 首页摘要
4. 图表数据
5. 完整分析报告
6. Resume-JD智能匹配
"""

from app.analysis.dashboard import dashboard
from app.analysis.report import generate_report
from app.analysis.analysis import (
    talent_profile,
    summary,
    chart_data,
)

from app.analysis.matcher import match_resume_job


# ==========================================================
# Dashboard
# ==========================================================

def get_dashboard():
    """
    获取Dashboard
    """

    return dashboard()


# ==========================================================
# 人才画像
# ==========================================================

def get_profile():
    """
    获取人才画像
    """

    return talent_profile()


# ==========================================================
# 首页摘要
# ==========================================================

def get_summary():
    """
    获取首页摘要
    """

    return summary()


# ==========================================================
# 图表数据
# ==========================================================

def get_chart():
    """
    获取图表数据
    """

    return chart_data()


# ==========================================================
# 完整分析报告
# ==========================================================

def get_report():
    """
    获取完整分析报告
    """

    return generate_report()


# ==========================================================
# Resume ↔ JD 匹配
# ==========================================================

def get_match_result(
    resume_id: int,
    job_id: int
):
    """
    获取简历岗位匹配结果
    """

    return match_resume_job(
        resume_id=resume_id,
        job_id=job_id
    )


# ==========================================================
# 测试
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)

    print("Dashboard")

    print(get_dashboard())

    print("=" * 60)

    print("Profile")

    print(get_profile())

    print("=" * 60)

    print("Summary")

    print(get_summary())

    print("=" * 60)

    print("Chart")

    print(get_chart())

    print("=" * 60)

    print("Report")

    print(get_report())

    print("=" * 60)

    print("Match")

    print(

        get_match_result(

            1,

            1

        )

    )

    print("=" * 60)