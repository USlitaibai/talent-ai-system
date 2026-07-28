"""
FastAPI 项目启动入口

整个项目唯一启动入口。

负责：

1. 创建 FastAPI
2. 注册所有业务 Router
3. 提供首页接口
"""

from fastapi import FastAPI

from app.common.response import success

from app.resume.api import router as resume_router
from app.talent.api import router as talent_router
from app.jd.api import router as jd_router

from app.knowledge.api import router as knowledge_router

from app.analysis.api import router as analysis_router

from app.review.api import router as review_router

from app.export.api import router as export_router

from app.core.database import engine
from app.models import Base

from app.system.api import router as system_router


app = FastAPI(
    title="TALENT-AI-SYSTEM",
    description="AI 人才知识库系统",
    version="1.0.0"
)
# ==========================
# 自动创建数据库表
# ==========================

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    """
    系统首页
    """

    return success(
        message="TALENT-AI-SYSTEM is running."
    )


# ==========================
# 注册业务模块
# ==========================

app.include_router(resume_router)
app.include_router(talent_router)
app.include_router(jd_router)
app.include_router(knowledge_router)
app.include_router(analysis_router)
app.include_router(review_router)
app.include_router(export_router)
app.include_router(system_router)
# 后续开发时继续添加
#
# app.include_router(talent_router)1
# app.include_router(review_router)1
# app.include_router(analysis_router)1
# app.include_router(knowledge_router)1
# app.include_router(export_router)1
# app.include_router(system_router)1

# ==========================================================
# 启动入口
# ==========================================================

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=False
    )