# ==========================================================
# Talent AI System
#
# 说明：
#   依赖中包含 torch / sentence-transformers（约 500MB），
#   因此镜像体积较大、首次构建较慢，属预期现象。
#
#   若不需要 CrossEncoder 精排，可在 compose 中设置
#   RERANK_ENABLED=false，系统会自动改用 RRF 排名融合，
#   功能可正常使用（效果略降），但省掉 2GB 模型下载。
# ==========================================================

FROM python:3.12-slim

# ==========================================================
# 基础环境
# ==========================================================

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    TZ=Asia/Shanghai

WORKDIR /app

# ==========================================================
# 系统依赖（PyMuPDF / MySQL 客户端 / 健康检查）
# ==========================================================

RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        libglib2.0-0 \
        libgl1 \
        default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# ==========================================================
# Python 依赖（单独一层，利用构建缓存）
# ==========================================================

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# ==========================================================
# 业务代码
# ==========================================================

COPY app/ ./app/

# 预置向量库（若存在）：让容器启动即有知识可检索
COPY docker/vectors/ ./data/vectors/

# ==========================================================
# 运行目录与非 root 用户
# ==========================================================

RUN mkdir -p \
        data/uploads \
        data/output \
        data/resumes \
        app/logs \
    && useradd -m -u 1000 appuser \
    && chown -R appuser:appuser /app

USER appuser

# ==========================================================
# 启动
#
# 注意：必须用 app.server:app
# 项目内部使用 "from app.xxx import ..." 绝对导入，
# 在 /app/app 目录下启动会找不到 app 包。
# ==========================================================

EXPOSE 8000

# 说明：LLM 抽取与 RAG 生成属于长耗时请求（可达数分钟），
# 单 worker 期间健康检查可能排队，因此超时放宽到 15s，
# 并加大 start-period 以覆盖首次加载索引等初始化。
HEALTHCHECK --interval=30s --timeout=15s --start-period=60s --retries=5 \
    CMD curl -fsS http://localhost:8000/ || exit 1

CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000"]
