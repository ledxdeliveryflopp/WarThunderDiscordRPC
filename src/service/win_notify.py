import os
import signal
import time

from loguru import logger
from windows_toasts import (
    InteractableWindowsToaster, Toast,
    ToastDisplayImage, ToastImagePosition, ToastDuration, ToastButton,
    ToastActivatedEventArgs,
)

from src.const import const
from src.service.github import GitHubService

from src.settings import settings
from src.shemas.repos import ReleaseSchemas


class WinNotificationService(GitHubService):

    def __init__(self):
        super().__init__()
        self.notify_logger = logger.bind(source='notify')
        self.icon = f'{os.getcwd()}/notify_img.png'

    @logger.catch
    def start_notify(self, app_version: str) -> None:
        toaster = InteractableWindowsToaster('WTDRP')
        start_text = const.presence_lang.app_start_notify[settings.lang]
        new_toast = Toast(
            [f'{start_text}{app_version}.'],
            duration=ToastDuration.Short,
        )
        test = ToastDisplayImage.fromPath(self.icon)
        test.position = ToastImagePosition.AppLogo
        test.circleCrop = True
        new_toast.AddImage(test)
        toaster.show_toast(new_toast)

    @logger.catch
    def error_notify(self, error: str) -> None:
        toaster = InteractableWindowsToaster('WTDRP')
        new_toast = Toast([error], duration=ToastDuration.Short)
        test = ToastDisplayImage.fromPath(self.icon)
        test.position = ToastImagePosition.AppLogo
        test.circleCrop = True
        new_toast.AddImage(test)
        toaster.show_toast(new_toast)

    @logger.catch
    def __update_callback(self, event_arg: ToastActivatedEventArgs):
        result = event_arg.arguments
        self.notify_logger.debug(f'ActivatedEventArgs -> {result}')
        if result == 'update':
            check_file = os.path.exists('updater.exe')
            if check_file is True:
                self.notify_logger.info('Start updater')
                os.startfile('updater.exe')
                os.kill(os.getpid(), signal.SIGTERM)
            else:
                self.notify_logger.warning('updater.exe dont found')
                self.error_notify(
                    error=const.presence_lang.updater_dont_found[
                        settings.lang
                    ]
                )

    def __check_update(self) -> ReleaseSchemas | None:
        latest_release_data = self.get_latest_release()
        latest_tag = latest_release_data.tag_name
        compare_result = self.compare_apps_version(
            current_version=const.APP_VERSION, latest_version=latest_tag,
        )
        if compare_result is True:
            return latest_release_data
        return None

    def __show_update_available_notify(
            self, release_data: ReleaseSchemas,
    ) -> None:
        created_at = release_data.created_at
        latest_tag = release_data.tag_name
        title = const.presence_lang.update_header.get(
            settings.lang
        )
        message_base = const.presence_lang.update_message.get(
            settings.lang
        )
        if settings.lang == 'ru':
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
        self.notify_logger.debug('Show notification')
        self.notify_logger.debug(f'Notify title -> {title}')
        self.notify_logger.debug(f'Notify message -> {message}')
        toaster = InteractableWindowsToaster('WTDRP')
        new_toast = Toast([message])
        test = ToastDisplayImage.fromPath(self.icon)
        test.position = ToastImagePosition.AppLogo
        test.circleCrop = True
        new_toast.AddImage(test)
        new_toast.AddAction(
            ToastButton(
                const.presence_lang.update_button[settings.lang],
                'update'
            )
        )
        new_toast.AddAction(
            ToastButton(
                const.presence_lang.skip_update_button[
                    settings.lang],
                'skip'
            )
        )
        new_toast.on_activated = self.__update_callback
        toaster.show_toast(new_toast)

    @logger.catch
    def check_update_notify(self) -> None:
        logger.info('User request update status')
        latest_release_data = self.__check_update()
        if latest_release_data is None:
            message = const.presence_lang.update_dont_found[settings.lang]
            toaster = InteractableWindowsToaster('WTDRP')
            new_toast = Toast([message])
            test = ToastDisplayImage.fromPath(self.icon)
            test.position = ToastImagePosition.AppLogo
            test.circleCrop = True
            new_toast.AddImage(test)
            toaster.show_toast(new_toast)
        else:
            self.__show_update_available_notify(latest_release_data)

    @logger.catch
    def win_notify_loop(self) -> None:
        """Win notify loop"""
        while True:
            latest_release_data = self.__check_update()
            if latest_release_data is None:
                time.sleep(10800)
                continue
            self.__show_update_available_notify(latest_release_data)
            time.sleep(10800)


notify_service = WinNotificationService()
