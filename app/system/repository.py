"""
System Repository

用户数据访问层
"""

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.models import User


def create_user(username: str, password: str):
    """
    创建用户
    """

    db: Session = SessionLocal()

    try:

        exists = (
            db.query(User)
            .filter(User.username == username)
            .first()
        )

        if exists:
            return None

        user = User(
            username=username,
            password=password
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        return user

    finally:

        db.close()


def get_user_by_username(username: str):
    """
    根据用户名查询
    """

    db: Session = SessionLocal()

    try:

        return (
            db.query(User)
            .filter(User.username == username)
            .first()
        )

    finally:

        db.close()


def get_user_by_id(user_id: int):
    """
    根据ID查询用户
    """

    db: Session = SessionLocal()

    try:

        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

    finally:

        db.close()


def get_all_users():
    """
    查询全部用户
    """

    db: Session = SessionLocal()

    try:

        return db.query(User).all()

    finally:

        db.close()


def delete_user(user_id: int):
    """
    删除用户
    """

    db: Session = SessionLocal()

    try:

        user = (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

        if user is None:
            return False

        db.delete(user)
        db.commit()

        return True

    finally:

        db.close()

if __name__ == "__main__":

    print("=" * 60)

    print(get_all_users())

    print("=" * 60)