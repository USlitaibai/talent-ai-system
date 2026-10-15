"""
Resume Service

简历业务层
"""

import uuid
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

SUPPORTED_SUFFIX = {".pdf", ".docx", ".txt"}

# ==========================================================
# 任务状态表（内存存储，重启即丢，够演示用）
# ==========================================================

_import_tasks: dict[str, dict] = {}


def get_import_task(task_id: str) -> dict | None:
    """查询导入任务状态"""
    return _import_tasks.get(task_id)


def list_import_tasks() -> list[dict]:
    """列出所有导入任务"""
    return list(_import_tasks.values())


def _build_resume_document(data: dict) -> str:
    """将结构化简历转换为知识库文本"""
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


def parse_and_save_resume(file_path: str | Path):
    """解析一份简历"""
    resume_text = parse_resume(file_path)
    result = extract_resume_info(resume_text)
    db_result = save_resume(result)

    if db_result["status"] == "created":
        knowledge_text = _build_resume_document(result)
        add_document(knowledge_text, source="resume")

    return {
        "resume": result,
        "database": db_result
    }


# ==========================================================
# ZIP解析（同步核心逻辑，供后台任务调用）
# ==========================================================

def _process_zip_task(task_id: str, zip_path: str | Path):
    """后台执行ZIP导入任务"""
    task = _import_tasks[task_id]
    task["status"] = "processing"

    importer = ZipImporter()

    try:
        importer.extract(zip_path)
        files = importer.scan()

        task["total"] = len(files)
        logger.info(f"ZIP任务 {task_id} 共发现 {len(files)} 份简历")

        for i, file in enumerate(files):
            try:
                data = parse_and_save_resume(file)
                status = data["database"]["status"]

                if status == "created":
                    task["success"] += 1
                elif status == "duplicate":
                    task["duplicate"] += 1

                # 把每份简历的解析结果都存下来
                task["detail"].append({
                    "file": file.name,
                    "status": status,
                    "resume_id": data["database"]["id"],
                    "name": data["resume"].get("name", ""),
                    "skills": data["resume"].get("skills", []),
                })

            except Exception as e:
                logger.exception(e)
                task["failed"] += 1
                task["detail"].append({
                    "file": file.name,
                    "status": "failed",
                    "error": str(e)
                })

            task["progress"] = f"{i + 1}/{len(files)}"

        task["status"] = "done"
        logger.info(f"ZIP任务 {task_id} 完成")

    except Exception as e:
        logger.exception(e)
        task["status"] = "failed"
        task["error"] = str(e)

    finally:
        importer.cleanup()


def start_zip_import_task(zip_path: str | Path) -> str:
    """启动ZIP导入后台任务，返回任务ID"""
    task_id = uuid.uuid4().hex[:8]

    _import_tasks[task_id] = {
        "task_id": task_id,
        "status": "pending",
        "total": 0,
        "success": 0,
        "duplicate": 0,
        "failed": 0,
        "progress": "0/0",
        "detail": [],
        "error": None,
    }

    return task_id


def batch_parse_and_save_resume(folder: str | Path):
    """批量解析目录中的所有简历"""
    folder = Path(folder)
    if not folder.exists():
        raise FileNotFoundError(folder)

    statistics = {
        "total": 0, "success": 0, "duplicate": 0, "failed": 0, "detail": []
    }

    for file in folder.iterdir():
        if not file.is_file():
            continue
        if file.suffix.lower() not in SUPPORTED_SUFFIX:
            continue

        statistics["total"] += 1

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

    return statistics


def list_resumes():
    return get_all_resumes()


def get_resume(resume_id: int):
    return get_resume_by_id(resume_id)
