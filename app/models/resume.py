from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func

from app.models import Base


class Resume(Base):
    """
    简历数据表
    """

    __tablename__ = "resume"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(50), nullable=False)

    school = Column(String(100))

    major = Column(String(100))

    research_direction = Column(String(255))

    skills = Column(Text)

    papers = Column(String(50))

    created_at = Column(
        DateTime,
        server_default=func.now()
    )