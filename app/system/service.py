"""
System Service

用户业务层

负责：

1. 用户注册
2. 用户登录
3. 用户查询
"""

from app.system.auth import (
    create_access_token,
    hash_password,
    verify_password,
)
from app.system.repository import (
    create_user,
    get_all_users,
    get_user_by_id,
    get_user_by_username,
)


def _user_to_dict(user):
    """
    User ORM -> dict
    """

    if user is None:
        return None

    return {
        "id": user.id,
        "username": user.username,
        "created_at": str(user.created_at),
    }


def register(
    username: str,
    password: str,
):
    """
    用户注册
    """

    user = get_user_by_username(username)

    if user:

        raise ValueError("用户名已存在")

    password = hash_password(password)

    user = create_user(
        username=username,
        password=password,
    )

    return _user_to_dict(user)


def login(
    username: str,
    password: str,
):
    """
    用户登录
    """

    user = get_user_by_username(username)

    if user is None:

        raise ValueError("用户名不存在")

    if not verify_password(
        password,
        user.password,
    ):

        raise ValueError("密码错误")

    token = create_access_token(
        username=user.username
    )

    return {
        "access_token": token,
        "token_type": "bearer",
    }


def list_users():
    """
    查询全部用户
    """

    users = get_all_users()

    return [
        _user_to_dict(user)
        for user in users
    ]


def get_user(user_id: int):
    """
    查询单个用户
    """

    user = get_user_by_id(user_id)

    return _user_to_dict(user)


if __name__ == "__main__":

    print("=" * 60)

    try:

        user = register(
            username="admin",
            password="123456",
        )

        print(user)

    except Exception as e:

        print(e)

    print("=" * 60)

    try:

        token = login(
            username="admin",
            password="123456",
        )

        print(token)

    except Exception as e:

        print(e)

    print("=" * 60)

    print(list_users())

    print("=" * 60)

    print(get_user(1))

    print("=" * 60)