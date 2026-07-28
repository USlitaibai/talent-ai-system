"""
ZIP Import

负责：

1. 解压 ZIP
2. 递归扫描
3. 自动过滤垃圾文件
4. 返回所有简历路径
5. 清理临时目录
"""

import shutil
import tempfile
import zipfile
from pathlib import Path

from app.core.logger import logger


# ==========================================================
# 支持格式
# ==========================================================

SUPPORTED_SUFFIX = {
    ".pdf",
    ".docx",
    ".txt"
}


# ==========================================================
# 自动忽略文件
# ==========================================================

IGNORE_NAMES = {
    "Thumbs.db",
    "desktop.ini",
    ".DS_Store"
}


# ==========================================================
# 自动忽略目录
# ==========================================================

IGNORE_DIRS = {
    "__MACOSX",
    ".git"
}


class ZipImporter:
    """
    ZIP 导入器
    """

    def __init__(self):

        self.temp_dir = None

    # ==========================================================
    # 解压 ZIP
    # ==========================================================

    def extract(self, zip_path: str | Path):

        zip_path = Path(zip_path)

        if not zip_path.exists():
            raise FileNotFoundError(zip_path)

        self.temp_dir = Path(
            tempfile.mkdtemp(
                prefix="talent_ai_zip_"
            )
        )

        logger.info(
            f"ZIP 解压目录：{self.temp_dir}"
        )

        with zipfile.ZipFile(zip_path, "r") as z:

            # 检查 ZIP 是否损坏
            bad_file = z.testzip()

            if bad_file is not None:

                raise zipfile.BadZipFile(
                    f"ZIP 文件损坏：{bad_file}"
                )

            z.extractall(self.temp_dir)

        logger.info("ZIP 解压完成")

        return self.temp_dir

    # ==========================================================
    # 递归扫描
    # ==========================================================

    def scan(self):

        if self.temp_dir is None:
            return []

        files = []

        for file in self.temp_dir.rglob("*"):

            if not file.is_file():
                continue

            # 忽略特殊目录
            if any(
                part in IGNORE_DIRS
                for part in file.parts
            ):
                continue

            # 忽略特殊文件
            if file.name in IGNORE_NAMES:
                continue

            # 忽略隐藏文件
            if file.name.startswith("."):
                continue

            # 过滤文件类型
            if file.suffix.lower() not in SUPPORTED_SUFFIX:
                continue

            files.append(file)

        files.sort()

        logger.info(
            f"""
ZIP 扫描完成

共发现 {len(files)} 份简历

扫描目录：
{self.temp_dir}
"""
        )

        return files

    # ==========================================================
    # 清理临时目录
    # ==========================================================

    def cleanup(self):

        if self.temp_dir is None:
            return

        if self.temp_dir.exists():

            logger.info(
                f"删除临时目录：{self.temp_dir}"
            )

            shutil.rmtree(
                self.temp_dir,
                ignore_errors=True
            )

        self.temp_dir = None


# ==========================================================
# 一键导入（工具函数）
# ==========================================================

def import_zip(zip_path):

    importer = ZipImporter()

    try:

        importer.extract(zip_path)

        return importer.scan()

    finally:

        importer.cleanup()


# ==========================================================
# 测试
# ==========================================================

if __name__ == "__main__":

    BASE = Path(__file__).resolve().parents[2]

    zip_file = BASE / "data" / "test.zip"

    importer = ZipImporter()

    try:

        importer.extract(zip_file)

        files = importer.scan()

        print("=" * 60)

        print(f"共发现 {len(files)} 个文件")

        print("=" * 60)

        for file in files:
            print(file)

        print("=" * 60)

    finally:

        importer.cleanup()