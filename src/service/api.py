import httpx
from loguru import logger

from src.settings import settings
from src.shemas.api import MainInfoSchemas, MapInfoSchemas, AircraftInfoSchemas


class WtApi:

    @staticmethod
    @logger.catch
    def get_vehicle_image(vehicle_tech_name: str) -> str:
        url = f'https://static.encyclopedia.warthunder.com/images/{vehicle_tech_name}.png'
        logger.debug(f'Vehicle -> {vehicle_tech_name}, image url -> {url}')
        return f'https://static.encyclopedia.warthunder.com/images/{vehicle_tech_name}.png'

    @staticmethod
    @logger.catch
    def get_main_info() -> MainInfoSchemas:
        "Indicators"
        response = httpx.get(url=settings.main_info_url)
        logger.debug(f'main info response -> {response.json()}')
        validated = MainInfoSchemas(**response.json())
        return validated

    @staticmethod
    @logger.catch
    def get_map_info() -> MapInfoSchemas | None:
        try:
            response = httpx.get(url=settings.map_info_url)
            logger.debug(f'map info response -> {response.json()}')
            validated = MapInfoSchemas(**response.json())
            return validated
        except httpx.ConnectError as connect_err:
            logger.error(f'{connect_err}, url -> {settings.map_info_url}')
            return None

    @staticmethod
    @logger.catch
    def get_air_state_request() -> AircraftInfoSchemas:
        "STATE"
        response = httpx.get(url=settings.air_info_url)
        logger.debug(f'air info response -> {response.json()}')
        validated = AircraftInfoSchemas(**response.json())
        return validated
