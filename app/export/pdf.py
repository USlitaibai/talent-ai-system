"""
PDF 导出
"""

from pathlib import Path

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph

# ==========================
# 注册中文字体（Windows）
# ==========================

font_path = r"C:\Windows\Fonts\msyh.ttc"

if Path(font_path).exists():
    pdfmetrics.registerFont(
        TTFont("微软雅黑", font_path)
    )
    FONT_NAME = "微软雅黑"
else:
    FONT_NAME = "Helvetica"


def export_pdf(data: dict, save_path: str):
    """
    导出 PDF
    """

    doc = SimpleDocTemplate(save_path)

    styles = getSampleStyleSheet()

    style = styles["BodyText"]
    style.fontName = FONT_NAME

    story = []

    for key, value in data.items():

        if isinstance(value, list):
            value = "、".join(value)

        story.append(
            Paragraph(f"<b>{key}</b>：{value}", style)
        )

    doc.build(story)

    return save_path


if __name__ == "__main__":

    demo = {
        "姓名": "张伟",
        "学校": "上海交通大学",
        "专业": "计算机科学",
        "技能": [
            "Python",
            "FastAPI",
            "Docker",
        ],
    }

    export_pdf(
        demo,
        "resume.pdf"
    )

    print("PDF 导出成功")