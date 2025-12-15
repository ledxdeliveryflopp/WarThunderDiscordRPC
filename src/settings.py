import yaml
from loguru import logger
from yaml import SafeLoader

from src.shemas.settings import ApiSettings, PresenceSettings


class Settings:

    def __init__(self):
        self.server: str | None = None
        self.indicators_endpoint: str | None = None
        self.map_endpoint: str | None = None
        self.air_info_endpoint: str | None = None
        self.show_indicators: bool | None = None
        self.lang: str | None = None
        self.logo_theme: str | None = None
        self.main_info_url: str | None = None
        self.map_info_url: str | None = None
        self.air_info_url: str | None = None
        self.air_dict: dict | None = None
        self.ground_dict: dict | None = None

    def __set_api_settings(self, settings_data: dict) -> None:
        validated = ApiSettings(**settings_data)
        logger.debug(f'api settings - {validated.model_dump()}')
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
        logger.debug(f'main endpoints - {self.main_info_url}')
        logger.debug(f'map endpoints - {self.main_info_url}')
        logger.debug(f'air endpoints - {self.air_info_url}')

    def __set_presence_settings(self, settings_data: dict) -> None:
        validated = PresenceSettings(**settings_data)
        logger.debug(f'presence settings - {validated.model_dump()}')
        self.show_indicators = validated.presence.show_indicators
        self.lang = validated.presence.lang
        self.logo_theme = validated.presence.logo_theme

    def __set_air_vehicle_info(self, settings_data: dict) -> None:
        self.air_dict = settings_data

    def __set_ground_vehicle_info(self, settings_data: dict) -> None:
        self.ground_dict = settings_data

    @logger.catch(reraise=True)
    def __load_main_settings(self) -> dict:
        with open('settings.yaml', 'r') as settings_data:
            data = yaml.load(settings_data, Loader=SafeLoader)
            return data['settings']

    @logger.catch(reraise=True)
    def __load_air_vehicle_settings(self) -> dict:
        with open('air_vehicle.yaml', 'r') as settings_data:
            data = yaml.load(settings_data, Loader=SafeLoader)
            return data['air_list']

    @logger.catch(reraise=True)
    def __load_ground_vehicle_settings(self) -> dict:
        with open('ground_vehicle.yaml', 'r') as settings_data:
            data = yaml.load(settings_data, Loader=SafeLoader)
            return data['ground_list']

    def set_settings(self) -> None:
        logger.info('----Configuring app----')
        main_settings_data = self.__load_main_settings()
        self.__set_api_settings(settings_data=main_settings_data)
        self.__set_presence_settings(settings_data=main_settings_data)
        air_vehicle_data = self.__load_air_vehicle_settings()
        self.__set_air_vehicle_info(settings_data=air_vehicle_data)
        ground_vehicle_data = self.__load_ground_vehicle_settings()
        self.__set_ground_vehicle_info(settings_data=ground_vehicle_data)
        self.__set_endpoints()
        logger.info('----Settings loaded----')


settings = Settings()
