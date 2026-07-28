"""
Export Service

导出业务层

负责：

1. 查询简历
2. 导出Excel
"""

from app.export.excel import export_excel
from app.resume.repository import (
    get_all_resumes,
    get_resume_by_id,
)


def export_all():
    """
    导出全部简历
    """

    resumes = get_all_resumes()

    filepath = export_excel(resumes)

    return {
        "file": filepath,
        "count": len(resumes)
    }


def export_by_ids(
    ids: list[int]
):
    """
    导出指定简历
    """

    resumes = []

    for resume_id in ids:

        resume = get_resume_by_id(
            resume_id
        )

        if resume:

            resumes.append(
                resume
            )

    filepath = export_excel(resumes)

    return {
        "file": filepath,
        "count": len(resumes)
    }


if __name__ == "__main__":

    print("=" * 60)

    print(export_all())

    print("=" * 60)

    print(export_by_ids([1, 2]))

    print("=" * 60)