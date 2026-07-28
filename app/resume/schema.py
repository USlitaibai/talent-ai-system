from pydantic import BaseModel
from typing import List


class ResumeCreate(BaseModel):
    """
    AI解析后的简历数据
    """

    name: str

    school: str

    major: str

    research_direction: str

    skills: List[str]

    papers: str


class ResumeResponse(BaseModel):
    """
    返回给前端的数据
    """

    id: int

    name: str

    school: str

    major: str

    research_direction: str

    skills: List[str]

    papers: str

    created_at: str