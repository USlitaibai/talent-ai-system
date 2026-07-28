"""
Resume Batch Parser

批量解析整个目录下的简历

流程：

扫描目录
    ↓
解析简历
    ↓
AI提取
    ↓
保存数据库
    ↓
写入知识库
    ↓
统计结果
"""

from pathlib import Path

from app.ai.llm import extract_resume_info
from app.core.logger import logger
from app.knowledge.repository import add_document
from app.resume.parser import parse_resume
from app.resume.repository import save_resume


SUPPORTED_SUFFIX = {
    ".pdf",
    ".docx",
    ".txt"
}


def build_knowledge_text(data: dict) -> str:
    """
    构建知识库文本
    """

    skills = data.get("skills", [])

    if isinstance(skills, list):
        skills = "、".join(skills)

    return f"""
姓名：{data.get("name","")}

学校：{data.get("school","")}

专业：{data.get("major","")}

研究方向：
{data.get("research_direction","")}

技能：
{skills}

论文：
{data.get("papers","")}
""".strip()


def batch_parse(directory: str | Path):

    directory = Path(directory)

    result = {
        "total": 0,
        "success": 0,
        "duplicate": 0,
        "failed": 0,
        "detail": []
    }

    if not directory.exists():

        raise FileNotFoundError(directory)

    logger.info(f"开始批量解析：{directory}")

    for file in directory.iterdir():

        if not file.is_file():
            continue

        if file.suffix.lower() not in SUPPORTED_SUFFIX:
            continue

        result["total"] += 1

        logger.info(f"处理：{file.name}")

        try:

            resume_text = parse_resume(file)

            info = extract_resume_info(resume_text)

            db = save_resume(info)

            if db["status"] == "duplicate":

                result["duplicate"] += 1

                result["detail"].append({
                    "file": file.name,
                    "status": "duplicate"
                })

                continue

            knowledge = build_knowledge_text(info)

            add_document(knowledge)

            result["success"] += 1

            result["detail"].append({
                "file": file.name,
                "status": "success"
            })

        except Exception as e:

            logger.exception(e)

            result["failed"] += 1

            result["detail"].append({
                "file": file.name,
                "status": "failed",
                "reason": str(e)
            })

    logger.info("批量解析结束")

    return result


if __name__ == "__main__":

    BASE = Path(__file__).resolve().parents[2]

    folder = BASE / "data" / "resumes"

    print(batch_parse(folder))