"""
ORM 数据模型统一导出
"""

from sqlalchemy.orm import declarative_base

Base = declarative_base()

from app.models.resume import Resume
from app.models.user import User
from app.models.jd import Job

__all__ = [
    "Base",
    "Resume",
    "User",
    "Job",
]