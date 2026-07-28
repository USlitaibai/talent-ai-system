"""
项目日志模块

支持：

1. 控制台输出
2. 文件输出
3. Error 单独保存
4. 自动滚动日志
"""

import logging

from pathlib import Path
from logging.handlers import RotatingFileHandler

# ==========================================================
# 日志目录
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)

APP_LOG = LOG_DIR / "app.log"

ERROR_LOG = LOG_DIR / "error.log"

# ==========================================================
# Logger
# ==========================================================

logger = logging.getLogger("talent_ai_system")

if not logger.handlers:

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(

        "%(asctime)s | %(levelname)-8s | %(module)s | %(message)s"

    )

    # ======================================================
    # 控制台
    # ======================================================

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    console_handler.setLevel(logging.INFO)

    # ======================================================
    # app.log
    # ======================================================

    file_handler = RotatingFileHandler(

        APP_LOG,

        maxBytes=5 * 1024 * 1024,

        backupCount=5,

        encoding="utf-8"

    )

    file_handler.setFormatter(formatter)

    file_handler.setLevel(logging.INFO)

    # ======================================================
    # error.log
    # ======================================================

    error_handler = RotatingFileHandler(

        ERROR_LOG,

        maxBytes=5 * 1024 * 1024,

        backupCount=3,

        encoding="utf-8"

    )

    error_handler.setFormatter(formatter)

    error_handler.setLevel(logging.ERROR)

    # ======================================================
    # 注册
    # ======================================================

    logger.addHandler(console_handler)

    logger.addHandler(file_handler)

    logger.addHandler(error_handler)