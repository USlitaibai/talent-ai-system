from app.database import engine
from app.models import Base

print("=" * 50)
print("开始创建数据表...")
print("=" * 50)

Base.metadata.create_all(bind=engine)

print("=" * 50)
print("数据表创建完成！")
print("=" * 50)