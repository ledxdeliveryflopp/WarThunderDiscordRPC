import time

from loguru import logger

from src.const import const
from src.service.github import GitHubService

from plyer import notification as win_notify

from src.settings import Settings


class WinNotificationService(GitHubService):

    def notify_loop(self, app_settings: Settings) -> None:
        logger.add('notify.log', level='DEBUG')
        logger.debug(f'Notify settings -> {app_settings.__dict__}')
        while True:
            latest_release_data = self.get_latest_release()
            if latest_release_data is None:
                time.sleep(3600)
                continue
            latest_tag = latest_release_data.tag_name
            created_at = latest_release_data.created_at
            compare_result = self.compare_apps_version(
                current_version=const.APP_VERSION, latest_version=latest_tag,
            )
            if compare_result is True:
                title = const.presence_lang.update_header.get(
                    app_settings.lang
                )
                message_base = const.presence_lang.update_message.get(
                    app_settings.lang
                )
                if app_settings.lang == 'ru':
                    date = created_at.strftime(
                        '%d.%m.%Y'
                    )
                    date_msg = 'Дата релиза: '
                else:
                    date = created_at.strftime(
                        '%m.%d.%Y'
                    )
                    date_msg = 'Release date: '
                message_info = f'{latest_tag} \n{date_msg}{date}'
                message = f'{message_base}{message_info}'
                logger.debug('Show notification')
                logger.debug(f'Notify title -> {title}')
                logger.debug(f'Notify message -> {message}')
                win_notify.notify(
                    title=title,
                    message=message,
                    app_name='WTDRPC',
                    app_icon='app_icon.ico',
                    timeout=10,
                )
            time.sleep(3600)


notify_service = WinNotificationService()
