from pathlib import Path
import fitz
from docx import Document


def parse_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def parse_docx(file_path):
    doc = Document(file_path)

    text = ""

    for p in doc.paragraphs:
        text += p.text + "\n"

    return text


def parse_pdf(file_path):
    pdf = fitz.open(file_path)

    text = ""

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text


def parse_resume(file_path):
    """
    自动识别文件格式
    """

    suffix = Path(file_path).suffix.lower()

    if suffix == ".txt":
        return parse_txt(file_path)

    elif suffix == ".docx":
        return parse_docx(file_path)

    elif suffix == ".pdf":
        return parse_pdf(file_path)

    else:
        raise ValueError(f"暂不支持文件类型：{suffix}")


if __name__ == "__main__":

    BASE = Path(__file__).resolve().parent.parent
    RESUME_DIR = BASE / "data" / "resumes"

    print("=" * 60)
    print("TXT")
    print("=" * 60)
    print(parse_resume(RESUME_DIR / "test.txt"))

    print("=" * 60)
    print("DOCX")
    print("=" * 60)
    print(parse_resume(RESUME_DIR / "test.docx"))

    print("=" * 60)
    print("PDF")
    print("=" * 60)
    print(parse_resume(RESUME_DIR / "test.pdf"))