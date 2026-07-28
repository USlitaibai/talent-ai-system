"""
Talent Repository

人才业务数据库操作层

整个 Talent 模块唯一数据库入口。
"""

import json

from sqlalchemy import or_

from app.core.database import SessionLocal
from app.models import Resume


def get_all_resumes():
    """
    获取全部人才
    """

    db = SessionLocal()

    try:

        result = db.query(Resume).all()

        data = []

        for item in result:

            data.append(
                {
                    "id": item.id,
                    "name": item.name,
                    "school": item.school,
                    "major": item.major,
                    "research_direction": item.research_direction,
                    "skills": json.loads(item.skills),
                    "papers": item.papers,
                    "created_at": str(item.created_at)
                }
            )

        return data

    finally:
        db.close()


def search_resume(keyword: str):
    """
    根据关键字搜索人才
    """

    db = SessionLocal()

    try:

        result = (
            db.query(Resume)
            .filter(
                or_(
                    Resume.name.contains(keyword),
                    Resume.school.contains(keyword),
                    Resume.major.contains(keyword),
                    Resume.research_direction.contains(keyword),
                    Resume.skills.contains(keyword),
                    Resume.papers.contains(keyword)
                )
            )
            .all()
        )

        data = []

        for item in result:

            data.append(
                {
                    "id": item.id,
                    "name": item.name,
                    "school": item.school,
                    "major": item.major,
                    "research_direction": item.research_direction,
                    "skills": json.loads(item.skills),
                    "papers": item.papers,
                    "created_at": str(item.created_at)
                }
            )

        return data

    finally:
        db.close()