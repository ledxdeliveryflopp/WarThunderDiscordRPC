import asyncio
import os
import signal
import time
from loguru import logger
import multiprocessing as mp

from src.const import const
from src.service.api import WtApi
from src.service.presence import presence_service
from src.service.win_notify import notify_service
from src.settings import settings


async def main() -> None:
    await settings.set_settings()
    logger.info(f'App version -> {const.APP_VERSION}')
    logger.info('Starting notify process')
    try:
        notify_process = mp.Process(
            target=notify_service.notify_loop,
            name='NotifyProcess',
            args=(settings,),
            daemon=False,
        )
        notify_process.start()
        notify_pid = notify_process.pid
        logger.info(f'Notify process pid: {notify_pid}')
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
    finally:
        logger.debug(f'Stopping notify process')
        notify_process.terminate()
        try:
            os.kill(notify_pid, signal.SIGTERM)
        except Exception as e:
            logger.warning(e)

if __name__ == '__main__':
    asyncio.run(main())
