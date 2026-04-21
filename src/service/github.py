from functools import lru_cache

import httpx
from loguru import logger
from packaging.version import Version

from src.const import const
from src.shemas.repos import ReleaseSchemas


class GitHubService:

    def __init__(self):
        self.notify_logger = logger.bind(source='notify')

    @lru_cache
    def compare_apps_version(
            self, current_version: str, latest_version: str,
    ) -> bool:
        self.notify_logger.debug(f'current app version -> {current_version}')
        self.notify_logger.debug(f'latest app version -> {latest_version}')
        if Version(current_version) < Version(latest_version):
            self.notify_logger.debug('current app version < latest version')
            return True
        else:
            self.notify_logger.debug('current app version > latest version')
            return False

    def get_latest_release(self) -> ReleaseSchemas | None:
        try:
            response = httpx.get(url=const.github.latest_url, timeout=360)
            self.notify_logger.debug(
                f'Github response status -> {response.status_code}',
            )
            self.notify_logger.debug(
                f'Github response data -> {response.json()}',
            )
            return ReleaseSchemas(**response.json())
        except Exception as e:
            self.notify_logger.warning(f'Error while get latest release: {e}')
            return None
