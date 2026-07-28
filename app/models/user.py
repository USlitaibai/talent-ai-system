from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

from app.models import Base


class User(Base):
    """
    用户表
    """

    __tablename__ = "user"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    username = Column(
        String(50),
        unique=True,
        nullable=False
    )

    password = Column(
        String(255),
        nullable=False
    )

    created_at = Column(
        DateTime,
        server_default=func.now()
    )