from parser import parse_txt
from llm import extract_resume_info
from exporter import save_json

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

resume_file = BASE_DIR / "data" / "resumes" / "test.txt"


def main():

    print("=" * 40)
    print("读取简历...")
    print("=" * 40)

    text = parse_txt(resume_file)

    print(text)

    print("\n")

    print("=" * 40)
    print("AI解析中...")
    print("=" * 40)

    result = extract_resume_info(text)

    print(result)

    save_path = save_json(result)

    print("\n")

    print("=" * 40)
    print("保存成功")
    print(save_path)
    print("=" * 40)


if __name__ == "__main__":
    main()