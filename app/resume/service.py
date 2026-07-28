"""
Resume Service

简历业务层

负责：

1. 单份简历解析
2. 批量简历解析
3. AI提取信息
4. 保存数据库
5. 写入知识库
"""

from pathlib import Path

from app.ai.llm import extract_resume_info
from app.core.logger import logger
from app.knowledge.repository import add_document
from app.resume.parser import parse_resume
from app.resume.zip_import import ZipImporter
from app.resume.repository import (
    get_all_resumes,
    get_resume_by_id,
    save_resume,
)

SUPPORTED_SUFFIX = {
    ".pdf",
    ".docx",
    ".txt"
}


# ==========================================================
# 构建知识库文本
# ==========================================================

def _build_resume_document(data: dict) -> str:
    """
    将结构化简历转换为知识库文本
    """

    skills = data.get("skills", [])

    if isinstance(skills, list):
        skills = "、".join(skills)

    return f"""
姓名：{data.get("name", "")}

学校：{data.get("school", "")}

专业：{data.get("major", "")}

研究方向：
{data.get("research_direction", "")}

技能：
{skills}

论文：
{data.get("papers", "")}
""".strip()


# ==========================================================
# 单份解析
# ==========================================================

def parse_and_save_resume(file_path: str | Path):
    """
    解析一份简历
    """

    resume_text = parse_resume(file_path)

    result = extract_resume_info(resume_text)

    db_result = save_resume(result)

    # 数据库新增时才写入知识库
    if db_result["status"] == "created":

        knowledge_text = _build_resume_document(result)

        add_document(
            knowledge_text,
            source="resume"
        )

    return {
        "resume": result,
        "database": db_result
    }

# ==========================================================
# ZIP解析
# ==========================================================

def zip_parse_and_save_resume(zip_path: str | Path):
    """
    ZIP简历导入
    """

    importer = ZipImporter()

    try:

        importer.extract(zip_path)

        files = importer.scan()

        logger.info(f"ZIP 共发现 {len(files)} 份简历")

        statistics = {
            "total": 0,
            "success": 0,
            "duplicate": 0,
            "failed": 0,
            "detail": []
        }

        for file in files:

            statistics["total"] += 1

            try:

                data = parse_and_save_resume(file)

                status = data["database"]["status"]

                if status == "created":
                    statistics["success"] += 1
                else:
                    statistics["duplicate"] += 1

                statistics["detail"].append({

                    "file": file.name,

                    "status": status,

                    "resume_id": data["database"]["id"]

                })

            except Exception as e:

                logger.exception(e)

                statistics["failed"] += 1

                statistics["detail"].append({

                    "file": file.name,

                    "status": "failed",

                    "error": str(e)

                })

        return statistics

    finally:

        importer.cleanup()
        
# ==========================================================
# 批量解析
# ==========================================================

def batch_parse_and_save_resume(folder: str | Path):
    """
    批量解析目录中的所有简历
    """

    folder = Path(folder)

    if not folder.exists():
        raise FileNotFoundError(folder)

    logger.info(f"开始批量解析：{folder}")

    statistics = {
        "total": 0,
        "success": 0,
        "duplicate": 0,
        "failed": 0,
        "detail": []
    }

    for file in folder.iterdir():

        if not file.is_file():
            continue

        if file.suffix.lower() not in SUPPORTED_SUFFIX:
            continue

        statistics["total"] += 1

        logger.info(f"正在处理：{file.name}")

        try:

            data = parse_and_save_resume(file)

            status = data["database"]["status"]

            if status == "created":

                statistics["success"] += 1

            elif status == "duplicate":

                statistics["duplicate"] += 1

            statistics["detail"].append({

                "file": file.name,

                "status": status,

                "resume_id": data["database"]["id"]

            })

        except Exception as e:

            logger.exception(e)

            statistics["failed"] += 1

            statistics["detail"].append({

                "file": file.name,

                "status": "failed",

                "error": str(e)

            })

    logger.info("批量解析完成")

    return statistics


# ==========================================================
# 查询全部
# ==========================================================

def list_resumes():
    """
    查询全部简历
    """

    return get_all_resumes()


# ==========================================================
# 查询单份
# ==========================================================

def get_resume(resume_id: int):
    """
    查询单份简历
    """

    return get_resume_by_id(resume_id)


# ==========================================================
# 测试
# ==========================================================

if __name__ == "__main__":

    BASE = Path(__file__).resolve().parents[2]

    folder = BASE / "data" / "resumes"

    result = batch_parse_and_save_resume(folder)

    print(result)