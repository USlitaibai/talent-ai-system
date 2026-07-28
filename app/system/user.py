"""
当前登录用户工具

负责：

1. 获取当前登录用户
"""

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.system.auth import verify_token
from app.system.repository import get_user_by_username

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    """
    获取当前登录用户
    """

    token = credentials.credentials

    username = verify_token(token)

    if username is None:

        raise HTTPException(
            status_code=401,
            detail="Token无效",
        )

    user = get_user_by_username(username)

    if user is None:

        raise HTTPException(
            status_code=401,
            detail="用户不存在",
        )

    return user


if __name__ == "__main__":

    print("=" * 60)

    print("Current User Dependency OK")

    print("=" * 60)