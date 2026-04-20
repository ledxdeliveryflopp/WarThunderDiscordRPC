import os

from windows_toasts import (
    InteractableWindowsToaster, Toast,
    ToastDisplayImage, ToastImagePosition, ToastProgressBar, ToastDuration,
)

from service.local import localization


class NotifyService:

    def __init__(self, lang: str):
        self.lang = lang

    def download_notify(self) -> (InteractableWindowsToaster, Toast):
        toaster = InteractableWindowsToaster('WTDRP')
        new_toast = Toast([localization.install[self.lang]])
        img_path = f'{os.getcwd()}/notify_img.png'
        test = ToastDisplayImage.fromPath(img_path)
        test.position = ToastImagePosition.AppLogo
        test.circleCrop = True
        new_toast.AddImage(test)
        progress_bar = ToastProgressBar(
            localization.downloading_assets[self.lang], progress=0,
        )
        new_toast.progress_bar = progress_bar
        toaster.show_toast(new_toast)
        return toaster, new_toast

    def install_error_notify(self) -> None:
        toaster = InteractableWindowsToaster('WTDRP')
        message = localization.install_error[self.lang]
        new_toast = Toast([message])
        img_path = f'{os.getcwd()}/notify_img.png'
        test = ToastDisplayImage.fromPath(img_path)
        test.position = ToastImagePosition.AppLogo
        test.circleCrop = True
        new_toast.AddImage(test)
        toaster.show_toast(new_toast)

    def show_endless_notify(
            self, progress_text: str,
    ) -> InteractableWindowsToaster:
        toaster = InteractableWindowsToaster('WTDRP')
        new_toast = Toast(
            text_fields=[localization.install[self.lang]],
            duration=ToastDuration.Long,
        )
        img_path = f'{os.getcwd()}/notify_img.png'
        test = ToastDisplayImage.fromPath(img_path)
        test.position = ToastImagePosition.AppLogo
        test.circleCrop = True
        new_toast.AddImage(test)
        progress_bar = ToastProgressBar(
            progress_text,
            progress=None,
            progress_override=localization.waiting[self.lang],
        )
        new_toast.progress_bar = progress_bar
        toaster.show_toast(new_toast)
        return toaster

    def finish_install_notify(self) -> InteractableWindowsToaster:
        toaster = InteractableWindowsToaster('WTDRP')
        message = localization.install_complete[self.lang]
        new_toast = Toast([message])
        img_path = f'{os.getcwd()}/notify_img.png'
        test = ToastDisplayImage.fromPath(img_path)
        test.position = ToastImagePosition.AppLogo
        test.circleCrop = True
        new_toast.AddImage(test)
        toaster.show_toast(new_toast)
        return toaster
