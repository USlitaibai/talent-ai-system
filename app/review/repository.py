"""
Review Repository

人工审核数据库操作

实际操作 Resume 表
"""

import json

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.resume import Resume


# ==========================================================
# 全部简历
# ==========================================================

def get_review_list():
    """
    获取全部待审核简历
    """

    db: Session = SessionLocal()

    try:

        result = db.query(Resume).all()

        data = []

        for item in result:

            data.append({

                "id": item.id,

                "name": item.name,

                "school": item.school,

                "major": item.major,

                "research_direction": item.research_direction,

                "skills": json.loads(item.skills),

                "papers": item.papers,

                "created_at": str(item.created_at)

            })

        return data

    finally:

        db.close()


# ==========================================================
# 查询一份简历
# ==========================================================

def get_review(
    resume_id: int
):
    """
    获取单份简历
    """

    db: Session = SessionLocal()

    try:

        item = (
            db.query(Resume)
            .filter(
                Resume.id == resume_id
            )
            .first()
        )

        if item is None:

            return None

        return {

            "id": item.id,

            "name": item.name,

            "school": item.school,

            "major": item.major,

            "research_direction": item.research_direction,

            "skills": json.loads(item.skills),

            "papers": item.papers,

            "created_at": str(item.created_at)

        }

    finally:

        db.close()


# ==========================================================
# 更新审核结果
# ==========================================================

def update_review(
    resume_id: int,
    data: dict
):
    """
    更新审核后的简历
    """

    db: Session = SessionLocal()

    try:

        resume = (
            db.query(Resume)
            .filter(
                Resume.id == resume_id
            )
            .first()
        )

        if resume is None:

            return None

        resume.name = data["name"]

        resume.school = data["school"]

        resume.major = data["major"]

        resume.research_direction = data["research_direction"]

        resume.skills = json.dumps(
            data["skills"],
            ensure_ascii=False
        )

        resume.papers = data["papers"]

        db.commit()

        db.refresh(resume)

        return {

            "id": resume.id,

            "status": "success"

        }

    finally:

        db.close()


# ==========================================================
# 删除简历
# ==========================================================

def delete_review(
    resume_id: int
):
    """
    删除简历
    """

    db: Session = SessionLocal()

    try:

        resume = (
            db.query(Resume)
            .filter(
                Resume.id == resume_id
            )
            .first()
        )

        if resume is None:

            return False

        db.delete(resume)

        db.commit()

        return True

    finally:

        db.close()


# ==========================================================
# 数量
# ==========================================================

def review_count():
    """
    简历数量
    """

    db: Session = SessionLocal()

    try:

        return db.query(Resume).count()

    finally:

        db.close()


# ==========================================================
# 是否存在
# ==========================================================

def exists(
    resume_id: int
):
    """
    判断简历是否存在
    """

    db: Session = SessionLocal()

    try:

        return (
            db.query(Resume)
            .filter(
                Resume.id == resume_id
            )
            .first()
            is not None
        )

    finally:

        db.close()


# ==========================================================
# 测试
# ==========================================================

if __name__ == "__main__":

    print("=" * 60)

    print(get_review_list())

    print("=" * 60)

    print(get_review(1))

    print("=" * 60)

    print(review_count())

    print("=" * 60)

    print(exists(1))

    print("=" * 60)