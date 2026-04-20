import os
import shutil
import time

import httpx
import py7zr
import requests
import yaml
from loguru import logger

from schemas.git import ReleaseSchemas
from service.notify import NotifyService
from service.local import localization


class UpdaterService(NotifyService):

    def __init__(self):
        self.__set_logger()
        self.git_api: str = 'https://api.github.com/repos/'
        self.owner: str = 'ledxdeliveryflopp'
        self.repo: str = 'WarThunderDiscordRPC'
        self.git_path: str = '/releases/latest'

        self.latest_url = f'{self.git_api}{self.owner}/{self.repo}{self.git_path}'  # noqa
        self.lang = None
        self.set_lang_settings()
        super().__init__(self.lang)

    def set_lang_settings(self) -> None:
        with open('settings.yaml', 'r') as file:
            data = yaml.safe_load(file)
        logger.debug(f'Settings loaded -> {data}')
        self.lang = data['settings']['presence']['lang']

    @staticmethod
    def __set_logger():
        logger.add('updater.log', level='DEBUG')

    def get_latest_release(self) -> ReleaseSchemas | None:
        try:
            toaster = self.show_endless_notify(
                progress_text=localization.release_data[self.lang],
            )
            response = httpx.get(url=self.latest_url, timeout=360)
            logger.debug(f'Github response status -> {response.status_code}')
            logger.debug(f'Github response data -> {response.json()}')
            time.sleep(6)
            toaster.clear_toasts()
            return ReleaseSchemas(**response.json())
        except Exception as e:
            logger.error(f'Error while get latest release: {e}')
            self.install_error_notify()
            return None

    def download_release_zip(self) -> None:
        try:
            release_data = self.get_latest_release()
            url = None
            for data in release_data.assets:
                if data.name == 'dist.7z':
                    url = data.browser_download_url
            if url is None:
                logger.error('No download url found for release')
                self.install_error_notify()
                return
            response = requests.get(url, stream=True)
            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0

            toaster, toast = self.download_notify()
            os.makedirs('temp', exist_ok=True)
            with open('temp/test.7z', 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if not chunk:
                        continue
                    file.write(chunk)
                    downloaded += len(chunk)
                    if total_size:
                        progress = min(downloaded / total_size, 1.0)
                        percent = progress * 100
                        toast.progress_bar.progress = progress
                        toast.progress_bar.progress_override = f'{percent:.0f}%'
                        toaster.update_toast(toast)
            logger.info('Download finished')
            toaster.clear_toasts()
            self.extract_release_zip()
        except Exception as e:
            logger.error(e)

    def extract_release_zip(self) -> None:
        notify = self.show_endless_notify(localization.unzip[self.lang])
        with py7zr.SevenZipFile('temp/test.7z', mode='r') as z:
            z.extractall(path='temp')
        time.sleep(5)
        notify.clear_toasts()
        self.copy_release_files()

    def copy_release_files(self) -> ...:
        notify = self.show_endless_notify(localization.update_files[self.lang])
        src_dir = os.path.abspath(f'{os.getcwd()}/temp')
        dst_dir = os.path.abspath(os.getcwd())

        for root, dirs, files in os.walk(src_dir):
            rel = os.path.relpath(root, src_dir)
            target_root = os.path.join(dst_dir, "" if rel == "." else rel)
            os.makedirs(target_root, exist_ok=True)
            for f in files:
                src_path = os.path.join(root, f)
                if 'updater.exe' in src_path:
                    logger.warning(f'Skipping -> {src_path}')
                    continue
                dst_path = os.path.join(target_root, f)
                logger.info(f'Copying {src_path} to {dst_path}')
                shutil.copy2(src_path, dst_path)
        time.sleep(5)
        notify.clear_toasts()
        toaster = self.finish_install_notify()
        time.sleep(2)
        toaster.clear_toasts()
        time.sleep(1)
        os.startfile('WTDRP.exe')


if __name__ == '__main__':
    updater = UpdaterService()
    updater.download_release_zip()
