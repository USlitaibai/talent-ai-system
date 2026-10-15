"""
简历模块 API
"""

import shutil
from pathlib import Path

from fastapi import APIRouter, File, UploadFile, BackgroundTasks

from app.common.response import success, fail
from app.resume.service import (
    parse_and_save_resume,
    start_zip_import_task,
    get_import_task,
    list_import_tasks,
    _process_zip_task,
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

ALLOWED_SUFFIX = {".txt", ".docx", ".pdf"}


@router.post("/upload", summary="上传单份简历")
async def upload_resume(file: UploadFile = File(..., description="简历文件，支持 PDF / DOCX / TXT")):
    """上传单份简历文件，自动解析并入库"""
    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_SUFFIX:
        return fail(code=400, message="仅支持 txt、docx、pdf 文件")

    save_path = UPLOAD_DIR / file.filename
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    result = parse_and_save_resume(save_path)
    return success(result)


@router.post("/batch-upload", summary="批量上传简历")
async def batch_upload(files: list[UploadFile] = File(..., description="简历文件列表，支持多文件同时上传")):
    """批量上传多个简历文件，自动解析并入库"""
    statistics = {
        "total": 0, "success": 0, "duplicate": 0, "failed": 0, "detail": []
    }

    for file in files:
        statistics["total"] += 1
        suffix = Path(file.filename).suffix.lower()

        if suffix not in ALLOWED_SUFFIX:
            statistics["failed"] += 1
            statistics["detail"].append({
                "file": file.filename,
                "status": "failed",
                "error": f"不支持的文件类型：{suffix}"
            })
            continue

        save_path = UPLOAD_DIR / file.filename
        counter = 1
        while save_path.exists():
            stem = Path(file.filename).stem
            ext = Path(file.filename).suffix
            save_path = UPLOAD_DIR / f"{stem}_{counter}{ext}"
            counter += 1

        try:
            with open(save_path, "wb") as f:
                shutil.copyfileobj(file.file, f)

            data = parse_and_save_resume(save_path)
            status = data["database"]["status"]

            if status == "created":
                statistics["success"] += 1
            elif status == "duplicate":
                statistics["duplicate"] += 1

            statistics["detail"].append({
                "file": file.filename,
                "saved_as": save_path.name,
                "status": status,
                "resume_id": data["database"]["id"],
                "name": data["resume"].get("name", ""),
            })

        except Exception as e:
            statistics["failed"] += 1
            statistics["detail"].append({
                "file": file.filename,
                "status": "failed",
                "error": str(e)
            })

    return success(statistics)


# ==========================================================
# ZIP 上传（异步任务模式）
# ==========================================================

@router.post("/zip-upload", summary="ZIP批量导入（异步）")
async def zip_upload(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(..., description="ZIP压缩包，内含多份简历")
):
    """上传ZIP压缩包，后台异步解析，立即返回任务ID"""
    suffix = Path(file.filename).suffix.lower()
    if suffix != ".zip":
        return fail(code=400, message="仅支持 zip 文件")

    save_path = UPLOAD_DIR / file.filename
    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    task_id = start_zip_import_task(save_path)
    background_tasks.add_task(_process_zip_task, task_id, save_path)

    return success({
        "task_id": task_id,
        "message": "ZIP已上传，正在后台解析，可通过任务ID查询进度和结果"
    })


@router.get("/import-status/{task_id}", summary="查询导入任务进度和结果")
def import_status(task_id: str):
    """查询ZIP导入任务的执行进度和解析结果"""
    task = get_import_task(task_id)
    if task is None:
        return fail(code=404, message="任务不存在")
    return success(task)


@router.get("/import-tasks", summary="查看所有导入任务（调试用）")
def list_all_import_tasks():
    """查看所有导入任务列表（调试用）"""
    return success(list_import_tasks())


@router.get("/", summary="简历列表")
def get_resume_list():
    return success(list_resumes())


@router.get("/{resume_id}", summary="简历详情")
def get_resume_detail(resume_id: int):
    result = get_resume(resume_id)
    if result is None:
        return fail(code=404, message="简历不存在")
    return success(result)
