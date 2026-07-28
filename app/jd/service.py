"""
JD Service

岗位业务层

负责：

1. 解析JD

2. AI提取

3. 保存数据库

4. 查询岗位
"""

from pathlib import Path

from app.ai.llm import extract_jd_info

from app.jd.parser import parse_jd

from app.jd.repository import (

    save_job,

    get_all_jobs,

    get_job_by_id,

)

from app.knowledge.repository import add_document


# ==========================================================
# 构建知识库文本
# ==========================================================

def _build_job_document(data):

    skills = data.get("skills", [])

    if isinstance(skills, list):

        skills = "、".join(skills)

    return f"""
岗位：

{data.get("position","")}

公司：

{data.get("company","")}

学历：

{data.get("education","")}

专业：

{data.get("major","")}

经验：

{data.get("experience","")}

技能：

{skills}

薪资：

{data.get("salary","")}

城市：

{data.get("city","")}

岗位描述：

{data.get("description","")}
""".strip()


# ==========================================================
# 上传岗位
# ==========================================================

def parse_job_description(file_path: str | Path):

    text = parse_jd(file_path)

    result = extract_jd_info(text)

    db_result = save_job(result)

    if db_result["status"] == "created":

        add_document(

            _build_job_document(result),

            source="jd"

        )

    return {

        "job": result,

        "database": db_result

    }


# ==========================================================
# 查询全部
# ==========================================================

def list_jobs():

    return get_all_jobs()


# ==========================================================
# 查询单个
# ==========================================================

def get_job(job_id):

    return get_job_by_id(job_id)