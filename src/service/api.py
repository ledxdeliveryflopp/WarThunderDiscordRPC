import httpx
from loguru import logger

from src.settings import settings
from src.shemas.api import MainInfoSchemas, MapInfoSchemas, AircraftInfoSchemas


class WtApi:

    @staticmethod
    @logger.catch
    async def get_vehicle_image(vehicle_tech_name: str) -> str:
        url = f'https://static.encyclopedia.warthunder.com/images/{vehicle_tech_name}.png' # noqa
        logger.debug(f'Vehicle -> {vehicle_tech_name}, image url -> {url}')
        return f'https://static.encyclopedia.warthunder.com/images/{vehicle_tech_name}.png' # noqa

    @staticmethod
    @logger.catch(exclude=httpx.ConnectError)
    async def get_main_info() -> MainInfoSchemas | None:
        """Indicators"""
        try:
            response = httpx.get(url=settings.main_info_url)
        except httpx.ConnectError as connect_exc:
            logger.warning(f'Connect Error -> {connect_exc}')
            return None
        logger.debug(f'main info response -> {response.json()}')
        validated = MainInfoSchemas(**response.json())
        return validated

    @staticmethod
    @logger.catch(exclude=httpx.ConnectError)
    async def get_map_info() -> MapInfoSchemas | None:
        try:
            response = httpx.get(url=settings.map_info_url)
        except httpx.ConnectError as connect_exc:
            logger.warning(f'Connect Error -> {connect_exc}')
            return None
        logger.debug(f'map info response -> {response.json()}')
        validated = MapInfoSchemas(**response.json())
        return validated

    @staticmethod
    @logger.catch(exclude=httpx.ConnectError)
    async def get_air_state_request() -> AircraftInfoSchemas | None:
        try:
            response = httpx.get(url=settings.air_info_url)
        except httpx.ConnectError as connect_exc:
            logger.warning(f'Connect Error -> {connect_exc}')
            return None
        logger.debug(f'air info response -> {response.json()}')
        validated = AircraftInfoSchemas(**response.json())
        return validated

    @staticmethod
    async def health_check() -> bool:
        try:
            httpx.head(url=settings.main_info_url)
        except Exception:
            return False
