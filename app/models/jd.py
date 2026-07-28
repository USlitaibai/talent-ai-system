from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from app.models import Base


class Job(Base):
    """
    岗位表
    """

    __tablename__ = "job"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    position = Column(
        String(100),
        nullable=False
    )

    company = Column(
        String(100)
    )

    education = Column(
        String(50)
    )

    major = Column(
        String(100)
    )

    experience = Column(
        String(100)
    )

    skills = Column(
        Text
    )

    salary = Column(
        String(100)
    )

    city = Column(
        String(100)
    )

    description = Column(
        Text
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )