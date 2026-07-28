"""
数据库初始化脚本

作用：
1. 创建所有数据表
2. 后续新增 ORM 模型，无需修改本文件
"""

from app.core.database import engine
from app.models import Base

# 导入所有模型（非常重要）
from app.models.resume import Resume

# 后期继续新增即可
# from app.models.jd import JD
# from app.models.user import User


def create_tables():
    """
    创建数据库所有数据表
    """
    print("=" * 50)
    print("开始创建数据库表...")
    print("=" * 50)

    Base.metadata.create_all(bind=engine)

    print("=" * 50)
    print("数据库表创建完成！")
    print("=" * 50)


if __name__ == "__main__":
    create_tables()