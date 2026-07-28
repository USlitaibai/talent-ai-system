"""
Context Compressor

上下文压缩器
"""


def compress_context(
    context: str,
    max_lines: int = 8
) -> str:
    """
    压缩上下文
    """

    if not context.strip():
        return ""

    lines = []

    seen = set()

    for line in context.splitlines():

        line = line.strip()

        if not line:
            continue

        if line in seen:
            continue

        seen.add(line)

        lines.append(line)

    return "\n".join(
        lines[:max_lines]
    )


if __name__ == "__main__":

    text = """
Python

Python

FastAPI

FastAPI

MySQL

Docker

Docker

张伟

上海交通大学
"""

    print(
        compress_context(text)
    )