import time

from loguru import logger

from src.const import const
from src.service.presence import presence_service
from src.settings import settings

if __name__ == '__main__':
    settings.set_settings()
    logger.info(f'App version -> {const.APP_VERSION}')
    while True:
        discord_status = presence_service.get_discord_pipe()
        if discord_status is None:
            logger.warning('Discord pipe is empty')
            time.sleep(60)
        else:
            presence_service.set_presence()
            time.sleep(2)
