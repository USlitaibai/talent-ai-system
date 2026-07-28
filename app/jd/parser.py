from pathlib import Path

import fitz
from docx import Document

from app.core.logger import logger


def parse_txt(file_path):
    """
    解析 TXT 文件
    """
    logger.info(f"开始解析 TXT：{Path(file_path).name}")

    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    logger.info("TXT解析完成")

    return text


def parse_docx(file_path):
    """
    解析 DOCX 文件
    """
    logger.info(f"开始解析 DOCX：{Path(file_path).name}")

    doc = Document(file_path)

    text = ""

    for p in doc.paragraphs:
        text += p.text + "\n"

    logger.info("DOCX解析完成")

    return text


def parse_pdf(file_path):
    """
    解析 PDF 文件
    """
    logger.info(f"开始解析 PDF：{Path(file_path).name}")

    pdf = fitz.open(file_path)

    text = ""

    for page in pdf:
        text += page.get_text()

    pdf.close()

    logger.info("PDF解析完成")

    return text


def parse_jd(file_path):
    """
    自动识别 JD 文件格式
    """

    suffix = Path(file_path).suffix.lower()

    logger.info(f"识别文件类型：{suffix}")

    if suffix == ".txt":
        return parse_txt(file_path)

    elif suffix == ".docx":
        return parse_docx(file_path)

    elif suffix == ".pdf":
        return parse_pdf(file_path)

    else:
        logger.error(f"不支持的文件类型：{suffix}")
        raise ValueError(f"暂不支持文件类型：{suffix}")