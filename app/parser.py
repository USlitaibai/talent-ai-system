from pathlib import Path
import fitz

# 项目根目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 数据目录
DATA_DIR = BASE_DIR / "data"
RESUME_DIR = DATA_DIR / "resumes"


def parse_txt(file_path):
    """
    读取TXT文件
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


def parse_pdf(file_path):
    """
    读取PDF文件
    """
    text = ""

    pdf = fitz.open(file_path)

    for page in pdf:
        text += page.get_text()

    pdf.close()

    return text


if __name__ == "__main__":

    txt = parse_txt(RESUME_DIR / "test.txt")

    print(txt)
