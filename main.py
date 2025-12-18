import time

from loguru import logger

from src.service.presence import presence_service
from src.settings import settings

if __name__ == '__main__':
    logger.add(
        'wt_presence_{time}.log',
        format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}",
        level='INFO',
        diagnose=False,
    )
    settings.set_settings()
    while True:
        presence_service.set_presence()
        time.sleep(2)
