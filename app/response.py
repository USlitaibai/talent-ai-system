def success(data=None, message="success"):
    return {
        "code": 200,
        "message": message,
        "data": data
    }


def fail(code=400, message="error"):
    return {
        "code": code,
        "message": message,
        "data": None
    }