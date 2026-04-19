import os
from typing import Literal

import yaml
from loguru import logger
from yaml import SafeLoader

from src.shemas.settings import ApiSettings, PresenceSettings, AirInfoSettings


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
        self.custom_images_dict: dict | None = None
        self.loop_timeout: int | None = None
        self.show_update_notifications: bool | None = None

    async def __set_api_settings(self, settings_data: dict) -> None:
        validated = ApiSettings(**settings_data)
        logger.debug(f'api settings - {validated.model_dump()}')
        api_ip = validated.api.api_ip
        api_port = validated.api.api_port
        self.server = f'{api_ip}:{api_port}'
        self.indicators_endpoint = validated.api.indicators_endpoint
        self.map_endpoint = validated.api.map_endpoint
        self.air_info_endpoint = validated.api.air_info_endpoint

    async def __set_endpoints(self) -> None:
        self.main_info_url: str = f'http://{self.server}{self.indicators_endpoint}'
        self.map_info_url: str = f'http://{self.server}{self.map_endpoint}'
        self.air_info_url: str = f'http://{self.server}{self.air_info_endpoint}'
        logger.debug(f'main endpoints - {self.main_info_url}')
        logger.debug(f'map endpoints - {self.main_info_url}')
        logger.debug(f'air endpoints - {self.air_info_url}')

    async def __set_presence_settings(self, settings_data: dict) -> None:
        validated = PresenceSettings(**settings_data)
        logger.debug(
            f'presence settings - {validated.model_dump()}',
        )
        self.show_indicators = validated.presence.show_indicators
        self.lang = validated.presence.lang
        self.logo_theme = validated.presence.logo_theme
        self.custom_images = validated.presence.custom_images

    async def __set_air_vehicle_info(self, settings_data: dict) -> None:
        self.air_dict = settings_data

    async def __set_ground_vehicle_info(self, settings_data: dict) -> None:
        self.ground_dict = settings_data

    async def __set_air_info_settings(self, settings_data: dict) -> None:
        validated_settings = AirInfoSettings(**settings_data)
        logger.debug(
            f'air indicators settings - {validated_settings.model_dump()}',
        )
        self.air_speed_type = validated_settings.air_indicators.air_speed_type
        self.altitude_type = validated_settings.air_indicators.altitude_type

    @logger.catch(reraise=True)
    async def __load_main_settings(self) -> dict:
        with open('settings.yaml', 'r') as settings_data:
            data = yaml.load(settings_data, Loader=SafeLoader)
            return data['settings']

    @logger.catch(reraise=True)
    async def __load_custom_images(self) -> dict:
        with open('custom_images.yaml', 'r') as settings_data:
            data = yaml.load(settings_data, Loader=SafeLoader)
            return data['custom_images']

    @logger.catch(reraise=True)
    async def __load_air_vehicle_settings(self) -> dict:
        with open('air_vehicle.yaml', 'r', encoding='utf-8') as settings_data:
            data = yaml.load(settings_data, Loader=SafeLoader)
            logger.debug(f'Air list -> {data}')
            return data['air_list']

    @logger.catch(reraise=True)
    async def __load_ground_vehicle_settings(self) -> dict:
        with open('ground_vehicle.yaml', 'r', encoding='utf-8') as settings_data:
            data = yaml.load(settings_data, Loader=SafeLoader)
            logger.debug(f'Ground list -> {data}')
            return data['ground_list']

    @staticmethod
    async def __load_logs_settings() -> None:
        with open('settings.yaml', 'r') as settings_data:
            data = yaml.load(settings_data, Loader=SafeLoader)
        log_level = data['settings']['logger']['level']
        logger.add(
            'wt_presence_{time}.log',
            format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}",
            level=log_level.upper(),
        )
        logger.info(f'Log level -> {log_level}')

    async def set_settings(self) -> None:
        await self.__load_logs_settings()
        logger.info('----Configuring app----')
        os.makedirs('static', exist_ok=True)
        main_settings_data = await self.__load_main_settings()
        self.loop_timeout = main_settings_data['core']['timeout']
        show_notification = main_settings_data['core']['show_notification']
        self.show_update_notifications = show_notification
        await self.__set_api_settings(settings_data=main_settings_data)
        await self.__set_presence_settings(settings_data=main_settings_data)
        custom_images_data = await self.__load_custom_images()
        self.custom_images_dict = custom_images_data
        await self.__set_air_info_settings(settings_data=main_settings_data)
        air_vehicle_data = await self.__load_air_vehicle_settings()
        await self.__set_air_vehicle_info(settings_data=air_vehicle_data)
        ground_vehicle_data = await self.__load_ground_vehicle_settings()
        await self.__set_ground_vehicle_info(settings_data=ground_vehicle_data)
        await self.__set_endpoints()
        logger.info('----Settings loaded----')

    async def reset_air_vehicle_settings(self) -> None:
        logger.debug('Resetting air Vehicle Settings')
        air_vehicle_data = await self.__load_air_vehicle_settings()
        await self.__set_air_vehicle_info(settings_data=air_vehicle_data)

    async def reset_ground_vehicle_settings(self) -> None:
        logger.debug('Resetting ground Vehicle Settings')
        ground_vehicle_data = await self.__load_ground_vehicle_settings()
        await self.__set_ground_vehicle_info(settings_data=ground_vehicle_data)


settings = Settings()
