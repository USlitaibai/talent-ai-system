from sqlalchemy import text
from app.database import engine


def test_connection():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT VERSION();"))

        for row in result:
            print("=" * 50)
            print("数据库版本：", row[0])
            print("=" * 50)

    print("✅ 数据库连接成功！")


if __name__ == "__main__":
    test_connection()