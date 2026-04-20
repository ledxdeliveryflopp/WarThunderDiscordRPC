import os
import time

from loguru import logger
from windows_toasts import (
    InteractableWindowsToaster, Toast,
    ToastDisplayImage, ToastImagePosition, ToastDuration, ToastButton,
    ToastActivatedEventArgs,
)

from src.const import const
from src.service.github import GitHubService

from src.settings import Settings


class WinNotificationService(GitHubService):

    def __init__(self, app_settings: Settings):
        self.settings = app_settings

    @logger.catch
    def start_notify(self, app_version: str) -> None:
        icon = f'{os.getcwd()}/notify_img.png'
        toaster = InteractableWindowsToaster('WTDRP')
        start_text = const.presence_lang.app_start_notify[self.settings.lang]
        new_toast = Toast(
            [f'{start_text}{app_version}.'],
            duration=ToastDuration.Short,
        )
        test = ToastDisplayImage.fromPath(icon)
        test.position = ToastImagePosition.AppLogo
        test.circleCrop = True
        new_toast.AddImage(test)
        toaster.show_toast(new_toast)

    def activated_callback(self, event_arg: ToastActivatedEventArgs):
        result = event_arg.arguments
        logger.debug(f'ActivatedEventArgs -> {result}')
        if result == 'update':
            check_file = os.path.exists('updater.exe')
            if check_file is True:
                os.startfile('updater.exe')
                self.settings.kill_process(self.settings.main_pid)
                self.settings.kill_process(self.settings.notify_pid)
            else:
                logger.warning('updater.exe dont found')

    @logger.catch
    def win_notify_loop(self) -> None:
        """Win notify loop"""
        logger.add('win_notify.log', level='DEBUG')
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
                    self.settings.lang
                )
                message_base = const.presence_lang.update_message.get(
                    self.settings.lang
                )
                if self.settings.lang == 'ru':
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
                icon = f'{os.getcwd()}/notify_img.png'
                toaster = InteractableWindowsToaster('WTDRP')
                new_toast = Toast([message])
                test = ToastDisplayImage.fromPath(icon)
                test.position = ToastImagePosition.AppLogo
                test.circleCrop = True
                new_toast.AddImage(test)
                new_toast.AddAction(ToastButton(
                    const.presence_lang.update_button[self.settings.lang],
                    'update'
                )
                )
                new_toast.AddAction(ToastButton(
                        const.presence_lang.skip_update_button[self.settings.lang],
                    'skip'
                )
                )
                new_toast.on_activated = self.activated_callback
                toaster.show_toast(new_toast)
            time.sleep(3600)
