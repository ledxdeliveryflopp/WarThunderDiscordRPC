import os
import platform
import time

from loguru import logger
from win10toast import ToastNotifier
from win11toast import notify

from src.const import const
from src.service.github import GitHubService

from src.settings import Settings


class WinNotificationService(GitHubService):

    @property
    def win_version(self) -> str:
        version = platform.win32_ver()
        logger.info(f'Windows version -> {version}')
        return version[0]

    @logger.catch
    def win11_notify_loop(self, app_settings: Settings) -> None:
        """Win11 notify loop"""
        logger.add('win11_notify.log', level='DEBUG')
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
                    version_text = 'Версия: '
                    url_text = 'Нажмите что бы открыть релиз'
                else:
                    date = created_at.strftime(
                        '%m.%d.%Y'
                    )
                    date_msg = 'Release date: '
                    version_text = 'Version: '
                    url_text = 'Click to see the latest release'
                message_info = f'{version_text}{latest_tag} \n{date_msg}{date} \n{url_text}'
                message = f'{message_base}{message_info}'
                logger.debug('Show notification')
                logger.debug(f'Notify title -> {title}')
                logger.debug(f'Notify message -> {message}')
                icon = f'file://{os.getcwd()}/notify_img.png'
                notify(
                    title,
                    message_info,
                    icon=icon,
                    on_click=latest_release_data.html_url,
                )
            time.sleep(3600)

    @logger.catch
    def win10_notify_loop(self, app_settings: Settings) -> None:
        """Win10 notify loop"""
        logger.add('win10_notify.log', level='DEBUG')
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
                toaster = ToastNotifier()
                toaster.show_toast(
                    title=title,
                    msg=message,
                    icon_path='app_icon.ico',
                    duration=10
                )
            time.sleep(3600)


notify_service = WinNotificationService()
