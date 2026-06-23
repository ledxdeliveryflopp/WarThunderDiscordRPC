import os
import stat
from pathlib import Path

from loguru import logger


class Utils:

    @staticmethod
    def check_read_only(path: Path) -> bool:
        file_info = os.stat(path)
        result = bool(
            file_info.st_file_attributes & stat.FILE_ATTRIBUTE_READONLY
        )
        logger.info(f'File -> {path.name} stats result -> {result}')
        return result

    @staticmethod
    def drop_file_chmod(path: Path) -> None:
        logger.warning(f'Change chmod for file -> {path.name}')
        os.chmod(path, stat.S_IWRITE)


utils = Utils()
