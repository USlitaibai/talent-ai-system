"""
JD Schema
"""

from typing import List

from pydantic import BaseModel


class JDCreate(BaseModel):
    """
    创建岗位
    """

    position: str

    company: str = ""

    education: str = ""

    major: str = ""

    experience: str = ""

    skills: List[str] = []

    salary: str = ""

    city: str = ""

    description: str = ""


class JDResponse(BaseModel):
    """
    返回岗位
    """

    id: int

    position: str

    company: str

    education: str

    major: str

    experience: str

    skills: List[str]

    salary: str

    city: str

    description: str