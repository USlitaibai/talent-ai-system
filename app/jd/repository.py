"""
JD Repository

岗位数据访问层

负责：

1. 保存岗位
2. 查询全部岗位
3. 查询单个岗位
"""

import json

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models.jd import Job


# ==========================================================
# 保存岗位
# ==========================================================

def save_job(data: dict):
    """
    保存岗位（重复检测）
    """

    db: Session = SessionLocal()

    try:

        exists = (
            db.query(Job)
            .filter(
                Job.position == data["position"],
                Job.company == data["company"]
            )
            .first()
        )

        if exists:

            return {
                "status": "duplicate",
                "id": exists.id
            }

        job = Job(

            position=data["position"],

            company=data["company"],

            education=data["education"],

            major=data["major"],

            experience=data["experience"],

            skills=json.dumps(
                data["skills"],
                ensure_ascii=False
            ),

            salary=data["salary"],

            city=data["city"],

            description=data["description"]

        )

        db.add(job)

        db.commit()

        db.refresh(job)

        return {

            "status": "created",

            "id": job.id

        }

    finally:

        db.close()


# ==========================================================
# 查询全部岗位
# ==========================================================

def get_all_jobs():

    db = SessionLocal()

    try:

        jobs = db.query(Job).all()

        result = []

        for item in jobs:

            result.append({

                "id": item.id,

                "position": item.position,

                "company": item.company,

                "education": item.education,

                "major": item.major,

                "experience": item.experience,

                "skills": json.loads(item.skills),

                "salary": item.salary,

                "city": item.city,

                "description": item.description,

                "created_at": str(item.created_at)

            })

        return result

    finally:

        db.close()


# ==========================================================
# 查询单个岗位
# ==========================================================

def get_job_by_id(job_id: int):

    db = SessionLocal()

    try:

        item = (

            db.query(Job)

            .filter(Job.id == job_id)

            .first()

        )

        if item is None:

            return None

        return {

            "id": item.id,

            "position": item.position,

            "company": item.company,

            "education": item.education,

            "major": item.major,

            "experience": item.experience,

            "skills": json.loads(item.skills),

            "salary": item.salary,

            "city": item.city,

            "description": item.description,

            "created_at": str(item.created_at)

        }

    finally:

        db.close()