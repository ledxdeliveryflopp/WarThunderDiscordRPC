import asyncio
import time

from loguru import logger

from src.const import const
from src.service.api import WtApi
from src.service.presence import presence_service
from src.settings import settings


async def main() -> None:
    await settings.set_settings()
    logger.info(f'App version -> {const.APP_VERSION}')
    while True:
        discord_status = await presence_service.get_discord_pipe()
        if discord_status is None:
            logger.warning('Discord pipe is empty')
            time.sleep(settings.loop_timeout)
            continue
        game_status = await WtApi().health_check()
        if game_status is False:
            logger.warning('Game status is false')
            if discord_status is not None:
                try:
                    logger.debug('Close discord connection')
                    await presence_service.clear()
                except (AssertionError, RuntimeError) as err:
                    logger.warning(
                        f'Error while clear status -> {err}',
                    )
                    pass
            time.sleep(settings.loop_timeout)
            continue
        else:
            try:
                await presence_service.set_presence()
                time.sleep(3)
            except (AssertionError, RuntimeError) as exc:
                logger.warning(exc)
                await presence_service.connect()


if __name__ == '__main__':
    asyncio.run(main())
