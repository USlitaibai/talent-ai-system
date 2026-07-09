from pathlib import Path
import shutil

from fastapi import FastAPI, File, UploadFile

from app.crud import (
    save_resume,
    get_all_resumes,
    get_resume_by_id
)
from app.llm import extract_resume_info
from app.parser import parse_resume
from app.response import success, fail

app = FastAPI(
    title="AI人才简历解析系统",
    version="2.0.0"
)

BASE = Path(__file__).resolve().parent.parent

UPLOAD_DIR = BASE / "data" / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_SUFFIX = {
    ".txt",
    ".docx",
    ".pdf"
}


@app.get("/")
def root():
    return success(
        message="AI Resume Parser API"
    )


@app.post("/parse")
async def parse(file: UploadFile = File(...)):

    suffix = Path(file.filename).suffix.lower()

    if suffix not in ALLOWED_SUFFIX:
        return fail(
            400,
            "Only txt/docx/pdf files are supported."
        )

    save_path = UPLOAD_DIR / file.filename

    with open(save_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    resume_text = parse_resume(save_path)

    result = extract_resume_info(resume_text)

    save_resume(result)

    return success(result)


@app.get("/resumes")
def get_resumes():

    return success(
        get_all_resumes()
    )


@app.get("/resume/{resume_id}")
def get_resume(resume_id: int):

    result = get_resume_by_id(resume_id)

    if result is None:
        return fail(
            404,
            "Resume not found."
        )

    return success(result)