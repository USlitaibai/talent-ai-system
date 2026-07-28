"""
Analysis API

统计分析接口

负责：

1. Dashboard
2. 人才画像
3. 首页摘要
4. 图表数据
5. 完整分析报告
6. Resume-JD匹配
"""

from fastapi import APIRouter
from pydantic import BaseModel

from app.common.response import success, fail

from app.analysis.service import (
    get_dashboard,
    get_profile,
    get_report,
    get_summary,
    get_chart,
    get_match_result,
)

router = APIRouter(
    prefix="/analysis",
    tags=["Analysis"],
)


# ==========================================================
# 匹配请求模型
# ==========================================================

class MatchRequest(BaseModel):

    resume_id: int

    job_id: int


# ==========================================================
# Dashboard
# ==========================================================

@router.get("/dashboard")
def dashboard():

    return success(
        data=get_dashboard()
    )


# ==========================================================
# 人才画像
# ==========================================================

@router.get("/profile")
def profile():

    return success(
        data=get_profile()
    )


# ==========================================================
# 首页摘要
# ==========================================================

@router.get("/summary")
def summary():

    return success(
        data=get_summary()
    )


# ==========================================================
# 图表
# ==========================================================

@router.get("/chart")
def chart():

    return success(
        data=get_chart()
    )


# ==========================================================
# 完整报告
# ==========================================================

@router.get("/report")
def report():

    return success(
        data=get_report()
    )


# ==========================================================
# Resume ↔ JD 匹配
# ==========================================================

@router.post("/match")
def match(data: MatchRequest):

    try:

        result = get_match_result(

            resume_id=data.resume_id,

            job_id=data.job_id

        )

        return success(data=result)

    except Exception as e:

        return fail(

            code=400,

            message=str(e)

        )


# ==========================================================
# 测试
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)

    print(router)

    print("=" * 60)