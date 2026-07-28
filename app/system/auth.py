"""
JWT认证模块

负责：

1. 密码加密
2. 密码校验
3. JWT生成
4. JWT解析
"""

from datetime import datetime, timedelta, UTC

from jose import JWTError, jwt
from passlib.context import CryptContext

# ==========================
# JWT配置
# ==========================

SECRET_KEY = "talent-ai-system-secret-key"

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

# ==========================
# 密码加密器
# ==========================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(password: str) -> str:
    """
    密码加密
    """

    return pwd_context.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str
) -> bool:
    """
    校验密码
    """

    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(username: str) -> str:
    """
    创建JWT
    """

    expire = datetime.now(UTC) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload = {
        "sub": username,
        "exp": expire
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )


def verify_token(token: str):
    """
    校验JWT
    """

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload.get("sub")

    except JWTError:

        return None


if __name__ == "__main__":

    print("=" * 60)

    password = "123456"

    hashed = hash_password(password)

    print("Hash:", hashed)

    print(
        verify_password(
            password,
            hashed
        )
    )

    token = create_access_token("admin")

    print(token)

    print(
        verify_token(token)
    )

    print("=" * 60)