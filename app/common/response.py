"""
统一 API 返回格式
"""

from typing import Any


def success(
    data: Any = None,
    message: str = "success"
):
    """
    成功返回
    """

    return {
        "code": 200,
        "message": message,
        "data": data
    }


def fail(
    code: int = 400,
    message: str = "fail",
    data: Any = None
):
    """
    失败返回
    """

    return {
        "code": code,
        "message": message,
        "data": data
    }