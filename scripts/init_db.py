"""
数据库初始化脚本

统一创建所有 ORM 数据表

运行方式：

python -m scripts.init_db
"""

from app.core.database import Base, engine

# ========= 导入所有 ORM =========
from app.models.resume import Resume

# 后期新增模型，只需要继续导入即可
# from app.models.jd import JD
# from app.models.user import User


def init_database():
    print("=" * 60)
    print("开始创建数据库...")
    print("=" * 60)

    Base.metadata.create_all(bind=engine)

    print("=" * 60)
    print("数据库初始化完成！")
    print("=" * 60)


if __name__ == "__main__":
    init_database()