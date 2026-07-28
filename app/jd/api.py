"""
JD API
"""

import shutil
from pathlib import Path

from fastapi import APIRouter, File, UploadFile

from app.common.response import success, fail

from app.jd.service import (

    parse_job_description,

    list_jobs,

    get_job,

)

router = APIRouter(

    prefix="/jd",

    tags=["JD"]

)

BASE = Path(__file__).resolve().parents[2]

UPLOAD_DIR = BASE / "data" / "uploads"

UPLOAD_DIR.mkdir(

    parents=True,

    exist_ok=True

)

ALLOWED_SUFFIX = {

    ".txt",

    ".docx",

    ".pdf"

}


# ==========================================================
# 上传JD
# ==========================================================

@router.post("/upload")
async def upload_jd(

    file: UploadFile = File(...)

):

    suffix = Path(file.filename).suffix.lower()

    if suffix not in ALLOWED_SUFFIX:

        return fail(

            code=400,

            message="仅支持 txt/docx/pdf 文件"

        )

    save_path = UPLOAD_DIR / file.filename

    with open(save_path, "wb") as f:

        shutil.copyfileobj(file.file, f)

    result = parse_job_description(save_path)

    return success(result)


# ==========================================================
# 查询全部岗位
# ==========================================================

@router.get("/")
def get_job_list():

    return success(

        list_jobs()

    )


# ==========================================================
# 查询岗位详情
# ==========================================================

@router.get("/{job_id}")
def get_job_detail(

    job_id: int

):

    result = get_job(job_id)

    if result is None:

        return fail(

            code=404,

            message="岗位不存在"

        )

    return success(result)