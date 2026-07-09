import os
from pathlib import Path

from dotenv import load_dotenv

BASE = Path(__file__).resolve().parent.parent

load_dotenv(BASE / ".env")

# ========= MySQL =========

DB_HOST = os.getenv("DB_HOST")

DB_PORT = os.getenv("DB_PORT")

DB_USER = os.getenv("DB_USER")

DB_PASSWORD = os.getenv("DB_PASSWORD")

DB_NAME = os.getenv("DB_NAME")

# ========= Ollama =========

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL")