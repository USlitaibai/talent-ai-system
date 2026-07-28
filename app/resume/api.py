"""
简历模块 API

负责：

1. 上传单份简历
2. 批量上传简历
3. ZIP 上传简历
4. 查询简历
"""

import shutil
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, File, UploadFile

from app.common.response import success, fail
from app.resume.service import (
    parse_and_save_resume,
    batch_parse_and_save_resume,
    zip_parse_and_save_resume,
    list_resumes,
    get_resume,
)

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)

BASE = Path(__file__).resolve().parents[2]

UPLOAD_DIR = BASE / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_SUFFIX = {
    ".txt",
    ".docx",
    ".pdf"
}


# ==========================================================
# 上传单份简历
# ==========================================================

@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...)
):
    """
    上传单份简历
    """

    suffix = Path(file.filename).suffix.lower()

    if suffix not in ALLOWED_SUFFIX:

        return fail(
            code=400,
            message="仅支持 txt、docx、pdf 文件"
        )

    save_path = UPLOAD_DIR / file.filename

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    result = parse_and_save_resume(save_path)

    return success(result)


# ==========================================================
# 批量上传（多个文件）
# ==========================================================

@router.post("/batch-upload")
async def batch_upload(
    files: Annotated[list[UploadFile], File(...)]
):
    """
    批量上传多个简历
    """

    for file in files:

        suffix = Path(file.filename).suffix.lower()

        if suffix not in ALLOWED_SUFFIX:
            continue

        save_path = UPLOAD_DIR / file.filename

        with open(save_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

    result = batch_parse_and_save_resume(
        UPLOAD_DIR
    )

    return success(result)


# ==========================================================
# ZIP 上传
# ==========================================================

@router.post("/zip-upload")
async def zip_upload(
    file: UploadFile = File(...)
):
    """
    上传 ZIP 压缩包
    """

    suffix = Path(file.filename).suffix.lower()

    if suffix != ".zip":

        return fail(
            code=400,
            message="仅支持 zip 文件"
        )

    save_path = UPLOAD_DIR / file.filename

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    result = zip_parse_and_save_resume(
        save_path
    )

    return success(result)


# ==========================================================
# 查询全部简历
# ==========================================================

@router.get("/")
def get_resume_list():
    """
    查询全部简历
    """

    return success(
        list_resumes()
    )


# ==========================================================
# 查询单份简历
# ==========================================================

@router.get("/{resume_id}")
def get_resume_detail(
    resume_id: int
):
    """
    查询单份简历
    """

    result = get_resume(resume_id)

    if result is None:

        return fail(
            code=404,
            message="简历不存在"
        )

    return success(result)