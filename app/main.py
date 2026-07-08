from parser import parse_resume
from llm import extract_resume_info
from exporter import save_json

from pathlib import Path


BASE = Path(__file__).resolve().parent.parent

resume_path = BASE / "data" / "resumes" / "test.docx"
# 想测试其他格式时，只需改成：
# test.txt
# test.docx

print("=" * 40)
print("读取简历...")
print("=" * 40)

text = parse_resume(resume_path)

print(text)

print()

print("=" * 40)
print("AI解析中...")
print("=" * 40)

result = extract_resume_info(text)

print(result)

save_json(result)

print()

print("=" * 40)
print("保存成功")
print(BASE / "data" / "output" / "resume.json")
print("=" * 40)