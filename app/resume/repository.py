import json

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models import Resume


def save_resume(data: dict):
    """
    保存简历（重复检测）
    """

    db: Session = SessionLocal()

    try:

        exists = (
            db.query(Resume)
            .filter(
                Resume.name == data["name"],
                Resume.school == data["school"],
                Resume.major == data["major"]
            )
            .first()
        )

        if exists:
            return {
                "status": "duplicate",
                "id": exists.id
            }

        resume = Resume(
            name=data["name"],
            school=data["school"],
            major=data["major"],
            research_direction=data["research_direction"],
            skills=json.dumps(
                data["skills"],
                ensure_ascii=False
            ),
            papers=data["papers"]
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        return {
            "status": "created",
            "id": resume.id
        }

    finally:
        db.close()


def get_all_resumes():
    """
    获取全部简历
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


def get_resume_by_id(resume_id: int):
    """
    根据ID查询简历
    """

    db: Session = SessionLocal()

    try:

        item = (
            db.query(Resume)
            .filter(Resume.id == resume_id)
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