import json

from app.database import SessionLocal
from app.models import Resume


def save_resume(data: dict):
    """
    保存简历到数据库
    """

    db = SessionLocal()

    try:
        resume = Resume(
            name=data.get("name", ""),
            school=data.get("school", ""),
            major=data.get("major", ""),
            research_direction=data.get("research_direction", ""),
            skills=json.dumps(
                data.get("skills", []),
                ensure_ascii=False
            ),
            papers=data.get("papers", "")
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        print(f"✅ 数据已保存，ID={resume.id}")

        return resume

    finally:
        db.close()


def get_all_resumes():
    """
    查询所有简历
    """

    db = SessionLocal()

    try:

        resumes = db.query(Resume).all()

        result = []

        for r in resumes:

            result.append({
                "id": r.id,
                "name": r.name,
                "school": r.school,
                "major": r.major,
                "research_direction": r.research_direction,
                "skills": json.loads(r.skills) if r.skills else [],
                "papers": r.papers,
                "created_at": str(r.created_at)
            })

        return result

    finally:
        db.close()


def get_resume_by_id(resume_id: int):
    """
    根据ID查询简历
    """

    db = SessionLocal()

    try:

        r = db.query(Resume).filter(
            Resume.id == resume_id
        ).first()

        if r is None:
            return None

        return {
            "id": r.id,
            "name": r.name,
            "school": r.school,
            "major": r.major,
            "research_direction": r.research_direction,
            "skills": json.loads(r.skills) if r.skills else [],
            "papers": r.papers,
            "created_at": str(r.created_at)
        }

    finally:
        db.close()