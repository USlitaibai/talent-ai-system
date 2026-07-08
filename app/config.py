"""
config.py

项目配置（V1）
"""

from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 数据目录
DATA_DIR = BASE_DIR / "data"

# 简历目录
RESUME_DIR = DATA_DIR / "resumes"

# 输出目录
OUTPUT_DIR = DATA_DIR / "output"

# Ollama 模型
MODEL_NAME = "qwen3:4b"

# 支持的文件格式
SUPPORTED_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".docx"
}