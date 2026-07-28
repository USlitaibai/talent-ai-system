"""
Export API

导出接口
"""

from fastapi import APIRouter, Query
from fastapi.responses import FileResponse

from app.export.service import (
    export_all,
    export_by_ids
)

router = APIRouter(
    prefix="/export",
    tags=["Export"]
)


@router.get("/excel")
def export_excel(
    ids: list[int] | None = Query(
        default=None,
        description="简历ID列表，可选"
    )
):
    """
    导出Excel
    """

    if ids:

        result = export_by_ids(ids)

    else:

        result = export_all()

    return FileResponse(
        path=result["file"],
        filename=result["file"].split("\\")[-1],
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )