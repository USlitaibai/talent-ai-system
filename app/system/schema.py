"""
System Schema

用户权限相关数据模型
"""

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """
    创建用户
    """

    username: str = Field(
        ...,
        description="用户名"
    )

    password: str = Field(
        ...,
        min_length=6,
        description="密码"
    )


class UserLogin(BaseModel):
    """
    用户登录
    """

    username: str

    password: str


class UserResponse(BaseModel):
    """
    用户信息
    """

    id: int

    username: str

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """
    登录返回Token
    """

    access_token: str

    token_type: str = "bearer"