import http
import os
import platform
import shutil
import time
from pathlib import Path
from typing import Literal

import httpx
import yaml
from loguru import logger
from yaml import SafeLoader

from src.const import const
from src.logger import app_logger
from src.service.spawner import gv_service
from src.shemas.settings import (
    ApiSettings,
    PresenceSettings,
    AirInfoSettings,
    CoreSettings,
)
from src.utils import utils


class Settings:

    def __init__(self):
        self.server: str | None = None
        self.indicators_endpoint: str | None = None
        self.map_endpoint: str | None = None
        self.air_info_endpoint: str | None = None
        self.show_indicators: bool | None = None
        self.air_speed_type: Literal['IAS', 'TAS'] | None = None
        self.altitude_type: Literal['RADIO', 'ABSOLUTE'] | None = None
        self.custom_images: bool | None = None
        self.lang: str | None = None
        self.logo_theme: str | None = None
        self.main_info_url: str | None = None
        self.map_info_url: str | None = None
        self.air_info_url: str | None = None
        self.air_dict: dict | None = None
        self.ground_dict: dict | None = None
        self.custom_images_data: set = set()
        self.loop_timeout: int | None = None
        self.show_update_notifications: bool | None = None
        self.settings_file = Path('settings.yaml')
        self.air_file = Path('air_vehicle.yaml')
        self.ground_file = Path('ground_vehicle.yaml')
        self.logs_path = Path('logs')

    def __set_api_settings(self, settings_data: dict) -> None:
        validated = ApiSettings(**settings_data)
        app_logger.debug(f'api settings - {validated.model_dump()}')
        api_ip = validated.api.api_ip
        api_port = validated.api.api_port
        self.server = f'{api_ip}:{api_port}'
        self.indicators_endpoint = validated.api.indicators_endpoint
        self.map_endpoint = validated.api.map_endpoint
        self.air_info_endpoint = validated.api.air_info_endpoint

    def __set_endpoints(self) -> None:
        self.main_info_url: str = f'http://{self.server}{self.indicators_endpoint}'
        self.map_info_url: str = f'http://{self.server}{self.map_endpoint}'
        self.air_info_url: str = f'http://{self.server}{self.air_info_endpoint}'
        app_logger.debug(f'main endpoints - {self.main_info_url}')
        app_logger.debug(f'map endpoints - {self.main_info_url}')
        app_logger.debug(f'air endpoints - {self.air_info_url}')

    def __set_presence_settings(self, settings_data: dict) -> None:
        validated = PresenceSettings(**settings_data)
        app_logger.debug(
            f'presence settings - {validated.model_dump()}',
        )
        self.show_indicators = validated.presence.show_indicators
        self.lang = validated.presence.lang
        self.logo_theme = validated.presence.logo_theme
        self.custom_images = validated.presence.custom_images

    def __set_core_settings(self, settings_data: dict) -> None:
        validated = CoreSettings(**settings_data)
        app_logger.debug(
            f'core settings - {validated.model_dump()}',
        )
        self.loop_timeout = validated.core.timeout
        self.show_update_notifications = validated.core.show_notification

    def __set_air_vehicle_info(self, settings_data: dict) -> None:
        self.air_dict = settings_data

    def __set_ground_vehicle_info(self, settings_data: dict) -> None:
        self.ground_dict = settings_data

    def __set_air_info_settings(self, settings_data: dict) -> None:
        validated_settings = AirInfoSettings(**settings_data)
        app_logger.debug(
            f'air indicators settings - {validated_settings.model_dump()}',
        )
        self.air_speed_type = validated_settings.air_indicators.air_speed_type
        self.altitude_type = validated_settings.air_indicators.altitude_type

    @logger.catch(reraise=True)
    def __load_main_settings(self) -> dict:
        with open(self.settings_file, 'r') as settings_data:
            data = yaml.load(settings_data, Loader=SafeLoader)
            return data['settings']

    @logger.catch(reraise=True)
    def __load_custom_images(self) -> None:
        try:
            response = httpx.get(const.discord_static)
            logger.debug(f'Discord static status -> {response.status_code}')
            response_data = response.json()
            if response.status_code != http.HTTPStatus.OK:
                logger.warning(f'Discord static json -> {response_data}')
            logger.debug(f'Discord static json -> {response_data}')
            data = response.json()
            for static_info in data:
                self.custom_images_data.add(static_info['name'])
        except Exception as e:
            logger.error(f'Discord static status -> {e}')

    @logger.catch(reraise=True)
    def __load_air_vehicle_settings(self) -> dict:
        with open(self.air_file, 'r', encoding='utf-8') as settings_data:
            data = yaml.load(settings_data, Loader=SafeLoader)
            app_logger.debug(f'Air list -> {data}')
            return data['air_list']

    @logger.catch(reraise=True)
    def __load_ground_vehicle_settings(self) -> dict:
        with open(self.ground_file, 'r', encoding='utf-8') as settings_data:
            data = yaml.load(settings_data, Loader=SafeLoader)
            app_logger.debug(f'Ground list -> {data}')
            return data['ground_list']

    def __load_logs_settings(self) -> None:
        with open(self.settings_file, 'r') as settings_data:
            data = yaml.load(settings_data, Loader=SafeLoader)
        log_level = data['settings']['logger']['level']
        os.makedirs(self.logs_path.name, exist_ok=True)
        logger.add(
            self.logs_path.joinpath('wt_presence.log'),
            filter=lambda record: record['extra'].get('source') == 'app',
            level=log_level.upper(),
            rotation='300 MB',
        )
        logger.add(
            self.logs_path.joinpath('notify.log'),
            filter=lambda record: record['extra'].get('source') == 'notify',
            level='DEBUG',
            rotation='300 MB',
        )
        logger.add(
            self.logs_path.joinpath('gevent.log'),
            filter=lambda record: record['extra'].get('source') == 'gevent',
            level='DEBUG',
            rotation='300 MB',
        )
        logger.add(self.logs_path.joinpath('main.log'), level='DEBUG')
        app_logger.info(f'Log level -> {log_level}')

    def set_settings(self) -> None:
        self.__load_logs_settings()
        app_logger.info('----Configuring app----')
        os.makedirs('static', exist_ok=True)
        gevent_tasks = []
        main_settings_data = self.__load_main_settings()
        core_task = gv_service.spawn_task(
            target=self.__set_core_settings,
            target_args=main_settings_data,
        )
        gevent_tasks.append(core_task)
        api_task = gv_service.spawn_task(
            target=self.__set_api_settings,
            target_args=main_settings_data,
        )
        gevent_tasks.append(api_task)
        presence_task = gv_service.spawn_task(
            target=self.__set_presence_settings,
            target_args=main_settings_data,
        )
        gevent_tasks.append(presence_task)
        image_task = gv_service.spawn_task(target=self.__load_custom_images)
        gevent_tasks.append(image_task)
        air_task = gv_service.spawn_task(
            target=self.__set_air_info_settings,
            target_args=main_settings_data,
        )
        gevent_tasks.append(air_task)
        air_vehicle_data = self.__load_air_vehicle_settings()
        air_info_task = gv_service.spawn_task(
            target=self.__set_air_vehicle_info,
            target_args=air_vehicle_data,
        )
        gevent_tasks.append(air_info_task)
        ground_vehicle_data = self.__load_ground_vehicle_settings()
        ground_info_task = gv_service.spawn_task(
            target=self.__set_ground_vehicle_info,
            target_args=ground_vehicle_data,
        )
        gevent_tasks.append(ground_info_task)
        endpoint_task = gv_service.spawn_task(target=self.__set_endpoints)
        gevent_tasks.append(endpoint_task)
        win_task = gv_service.spawn_task(target=self.win_version)
        gevent_tasks.append(win_task)
        gv_service.run_tasks(tasks=gevent_tasks)
        app_logger.info('----Settings loaded----')

    def reset_air_vehicle_settings(self) -> None:
        app_logger.debug('Resetting air Vehicle Settings')
        air_vehicle_data = self.__load_air_vehicle_settings()
        self.__set_air_vehicle_info(settings_data=air_vehicle_data)

    def reset_ground_vehicle_settings(self) -> None:
        app_logger.debug('Resetting ground Vehicle Settings')
        ground_vehicle_data = self.__load_ground_vehicle_settings()
        self.__set_ground_vehicle_info(settings_data=ground_vehicle_data)

    @staticmethod
    def win_version() -> None:
        version = platform.win32_ver()
        app_logger.info(f'Windows data -> {version}')

    @staticmethod
    def clear_install_temp() -> None:
        temp_path = f'{os.getcwd()}/temp'
        app_logger.info(f'Clearing temp dir -> {temp_path}')
        if os.path.exists(temp_path) is True:
            shutil.rmtree(temp_path)
            app_logger.info('Temp dir removed')
        else:
            app_logger.info('Temp dir not found')

    @staticmethod
    @logger.catch
    def rename_updater():
        app_logger.info('Renaming updater')
        time.sleep(2)
        basic_updater_path = f'{os.getcwd()}/temp/updater.exe'
        new_updater = f'{os.getcwd()}/updater_new.exe'
        basic_exist = os.path.exists(basic_updater_path)
        renamed_temp_exist = os.path.exists(new_updater)
        save_path = f'{os.getcwd()}/updater.exe'
        if basic_exist is True:
            app_logger.debug('Basic updater exists')
            os.remove('updater.exe')
            os.rename(basic_updater_path, save_path)
            return
        if renamed_temp_exist is True:
            app_logger.debug('Renaming updater exists')
            os.remove('updater.exe')
            os.rename(new_updater, save_path)
            return

    def check_static_files_ro(self) -> None:
        file_list = [self.settings_file, self.air_file, self.ground_file]
        for file_path in file_list:
            check_ro_result = utils.check_read_only(file_path)
            if check_ro_result:
                utils.drop_file_chmod(file_path)


settings = Settings()
