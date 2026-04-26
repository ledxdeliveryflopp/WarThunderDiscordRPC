import asyncio
import signal
import threading
import time
import sys
from loguru import logger

from src.const import const
from src.logger import app_logger
from src.service.api import WtApi
from src.service.presence import presence_service
from src.service.win_notify import notify_service
from src.settings import settings
from src.tray import setup_tray


async def rpc_loop() -> None:
    settings.rename_updater()
    settings.clear_install_temp()
    app_logger.info(f'App version -> {const.APP_VERSION}')
    notify_service.start_notify(app_version=const.APP_VERSION)
    if settings.show_update_notifications is True:
        app_logger.info('Start notify loop')
        notify_thread = threading.Thread(
            target=notify_service.win_notify_loop,
            daemon=True,
            name='NotifyService',
        )
        notify_thread.start()
        app_logger.debug(f'Notify thread -> {notify_thread.name}')
    while True:
        discord_status = await presence_service.get_discord_pipe()
        if discord_status is None:
            app_logger.warning('Discord pipe is empty')
            time.sleep(settings.loop_timeout)
            continue
        game_status = await WtApi().health_check()
        if game_status is False:
            app_logger.warning('Game status is false')
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


def signal_handler(signum, frame):
    app_logger.debug('Exit signal')
    sys.exit(0)


def main() -> None:
    signal.signal(signal.SIGTERM, signal_handler)

    asyncio.run(settings.set_settings())

    def run_rpc_loop():
        asyncio.run(rpc_loop())

    presence_thread = threading.Thread(target=run_rpc_loop, daemon=True)
    presence_thread.start()
    app_logger.debug('Presence thread started')
    setup_tray()


if __name__ == '__main__':
    main()
