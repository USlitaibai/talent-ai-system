"""
项目统一配置

负责：

1. 数据库
2. Ollama
3. RAG
4. Cache
5. 日志
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# ==========================================================
# 项目根目录
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# ==========================================================
# 加载 .env
# ==========================================================

load_dotenv(BASE_DIR / ".env")

# ==========================================================
# MySQL
# ==========================================================

DB_HOST = os.getenv("DB_HOST")

DB_PORT = os.getenv("DB_PORT")

DB_USER = os.getenv("DB_USER")

DB_PASSWORD = os.getenv("DB_PASSWORD")

DB_NAME = os.getenv("DB_NAME")

# ==========================================================
# Ollama
# ==========================================================

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL"
)

OLLAMA_EMBED_MODEL = os.getenv(
    "OLLAMA_EMBED_MODEL",
    "nomic-embed-text:latest"
)

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434"
)

# ==========================================================
# RAG 配置
# ==========================================================

# Retriever 返回文档数量
RAG_TOP_K = 5

# Context 最大保留行数
RAG_MAX_CONTEXT_LINES = 8

# ==========================================================
# Cache 配置
# ==========================================================

# L1 Cache 最大数量
STRING_CACHE_SIZE = 100

# Semantic Cache 最大数量
SEMANTIC_CACHE_SIZE = 100

# Semantic Cache 命中阈值
SEMANTIC_CACHE_THRESHOLD = 0.85

# ==========================================================
# Logger
# ==========================================================

LOG_LEVEL = "INFO"

# ==========================================================
# AI
# ==========================================================

# LLM 温度（目前 Ollama chat 未使用，可预留）
LLM_TEMPERATURE = 0

# 最大输出 Token（预留）
LLM_MAX_TOKENS = 1024

# ==========================================================
# Reranker
# ==========================================================

# 是否启用 CrossEncoder 二次重排
#
# True ：首次启动会从 HuggingFace 下载
#        BAAI/bge-reranker-v2-m3（约 2GB），效果最好
# False：不加载重排模型，改用 RRF 排名融合兜底，
#        启动快、镜像小，适合容器 / 演示环境
#
# 需要时在 .env 中设置 RERANK_ENABLED=false
RERANK_ENABLED = os.getenv(
    "RERANK_ENABLED",
    "true"
).lower() in ("1", "true", "yes", "on")

# ==========================================================
# Performance
# ==========================================================

# 是否打印调试信息
DEBUG = True

# 是否打印 Retriever Context
PRINT_CONTEXT = os.getenv(
    "PRINT_CONTEXT",
    "true"
).lower() in ("1", "true", "yes", "on")

# 是否回显 SQLAlchemy 执行的 SQL（开发排查用，默认关闭）
# 需要时在 .env 中设置 DEBUG_SQL=true
DEBUG_SQL = os.getenv("DEBUG_SQL", "false").lower() in ("1", "true", "yes", "on")