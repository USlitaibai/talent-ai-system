"""
Review Service

人工审核业务层

负责：

1. 获取审核列表
2. 查询简历
3. 修改简历（同步知识库）
4. 删除简历（同步知识库）
"""

from app.review.repository import (
    get_review,
    get_review_list,
    update_review,
    delete_review,
    review_count,
)

from app.knowledge.repository import (
    update_document_by_resume,
    delete_document_by_resume,
)


# ==========================================================
# 构建知识文本
# ==========================================================

def build_resume_text(data: dict):
    """
    将简历转换成知识库文本
    """

    skills = data.get("skills", [])

    if isinstance(skills, list):
        skills = "、".join(skills)

    return f"""
姓名：{data.get("name", "")}

学校：{data.get("school", "")}

专业：{data.get("major", "")}

研究方向：{data.get("research_direction", "")}

技能：

{skills}

论文：

{data.get("papers", "")}
""".strip()


# ==========================================================
# 获取列表
# ==========================================================

def list_reviews():

    return get_review_list()


# ==========================================================
# 获取详情
# ==========================================================

def get_review_detail(
    resume_id: int
):

    return get_review(resume_id)


# ==========================================================
# 修改
# ==========================================================

def update_review_result(
    resume_id: int,
    data: dict
):
    """
    修改数据库
    同步更新知识库
    """

    result = update_review(
        resume_id,
        data
    )

    if result is None:

        raise ValueError("简历不存在")

    knowledge = build_resume_text(data)

    update_document_by_resume(
        resume_id=resume_id,
        text=knowledge,
        source="resume"
    )

    return result


# ==========================================================
# 删除
# ==========================================================

def delete_review_result(
    resume_id: int
):
    """
    删除数据库
    同步删除知识库
    """

    ok = delete_review(
        resume_id
    )

    if not ok:

        raise ValueError("简历不存在")

    delete_document_by_resume(
        resume_id
    )

    return {

        "status": "success",

        "id": resume_id

    }


# ==========================================================
# 数量
# ==========================================================

def review_total():

    return review_count()


# ==========================================================
# 测试
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)

    print(list_reviews())

    print("=" * 60)

    print(get_review_detail(1))

    print("=" * 60)

    print(review_total())

    print("=" * 60)