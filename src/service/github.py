from functools import lru_cache

import httpx
from loguru import logger
from packaging.version import Version

from src.const import const
from src.shemas.repos import ReleaseSchemas


class GitHubService:

    @logger.catch
    @lru_cache
    def compare_apps_version(
            self, current_version: str, latest_version: str,
    ) -> bool:
        logger.debug(f'current app version -> {current_version}')
        logger.debug(f'latest app version -> {latest_version}')
        if Version(current_version) < Version(latest_version):
            logger.debug('current app version < latest version')
            return True
        else:
            logger.debug('current app version > latest version')
            return False

    @staticmethod
    def get_latest_release() -> ReleaseSchemas | None:
        try:
            response = httpx.get(url=const.github.latest_url, timeout=360)
            logger.debug(f'Github response status -> {response.status_code}')
            logger.debug(f'Github response data -> {response.json()}')
            return ReleaseSchemas(**response.json())
        except Exception as e:
            logger.warning(f'Error while get latest release: {e}')
            return None
