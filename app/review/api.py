"""
Review API

人工审核接口

负责：

1. 获取全部简历
2. 获取简历详情
3. 修改简历
4. 删除简历
5. 获取简历数量
"""

from fastapi import APIRouter, HTTPException

from app.common.response import success
from app.review.schema import ReviewUpdate
from app.review.service import (
    list_reviews,
    get_review_detail,
    update_review_result,
    delete_review_result,
    review_total,
)

router = APIRouter(
    prefix="/review",
    tags=["Review"],
)


# ==========================================================
# 全部简历
# ==========================================================

@router.get("/list")
def review_list():
    """
    获取全部简历
    """

    return success(
        data=list_reviews()
    )


# ==========================================================
# 简历详情
# ==========================================================

@router.get("/{resume_id}")
def review_detail(
    resume_id: int
):
    """
    获取简历详情
    """

    result = get_review_detail(
        resume_id
    )

    if result is None:

        raise HTTPException(
            status_code=404,
            detail="简历不存在"
        )

    return success(
        data=result
    )


# ==========================================================
# 修改简历
# ==========================================================

@router.put("/{resume_id}")
def review_update(
    resume_id: int,
    data: ReviewUpdate
):
    """
    修改简历
    """

    try:

        result = update_review_result(
            resume_id,
            data.model_dump()
        )

        return success(
            data=result,
            message="修改成功"
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


# ==========================================================
# 删除简历
# ==========================================================

@router.delete("/{resume_id}")
def review_delete(
    resume_id: int
):
    """
    删除简历
    """

    try:

        result = delete_review_result(
            resume_id
        )

        return success(
            data=result,
            message="删除成功"
        )

    except ValueError as e:

        raise HTTPException(
            status_code=404,
            detail=str(e)
        )


# ==========================================================
# 简历数量
# ==========================================================

@router.get("/count")
def review_count():
    """
    获取简历数量
    """

    return success(
        data={
            "count": review_total()
        }
    )


# ==========================================================
# 测试
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)

    print(router)

    print("=" * 60)