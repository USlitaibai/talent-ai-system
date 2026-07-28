"""
System API

用户接口

负责：

1. 用户注册
2. 用户登录
3. 查询所有用户
4. 查询单个用户
"""

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from app.common.response import success
from app.system.schema import (
    UserCreate,
    UserLogin,
)
from app.system.service import (
    register,
    login,
    list_users,
    get_user,
)
from app.system.user import get_current_user

router = APIRouter(
    prefix="/system",
    tags=["用户系统"],
)


@router.post("/register")
def register_api(data: UserCreate):
    """
    用户注册
    """

    try:

        user = register(
            username=data.username,
            password=data.password,
        )

        return success(
            data=user,
            message="注册成功",
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.post("/login")
def login_api(data: UserLogin):
    """
    用户登录
    """

    try:

        token = login(
            username=data.username,
            password=data.password,
        )

        return success(
            data=token,
            message="登录成功",
        )

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )


@router.get("/users")
def list_user_api(
    current_user=Depends(get_current_user),
):
    """
    查询全部用户（需要登录）
    """

    return success(
        data=list_users()
    )


@router.get("/users/{user_id}")
def get_user_api(
    user_id: int,
    current_user=Depends(get_current_user),
):
    """
    查询单个用户（需要登录）
    """

    user = get_user(user_id)

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="用户不存在",
        )

    return success(
        data=user
    )


if __name__ == "__main__":

    print("=" * 60)

    print(router)

    print("=" * 60)