from loguru import logger

from src.settings import settings


class ParserService:

    @staticmethod
    def parse_tank_name(tank_tech_name: str) -> str:
        parsed_name = tank_tech_name.replace('tankModels/', '')
        logger.debug(f'tank parse name result -> {parsed_name}')
        return parsed_name

    @staticmethod
    def get_readable_tank_name(tank_parsed_name: str) -> str:
        tank_readable_name = settings.ground_dict.get(tank_parsed_name, None)[settings.lang]
        logger.debug(f'Tank readable name -> {tank_readable_name}')
        if tank_readable_name is None:
            return tank_parsed_name
        return tank_readable_name

    @staticmethod
    def get_readable_air_name(air_name: str) -> str:
        air_readable_name = settings.air_dict.get(air_name, None)[settings.lang]
        logger.debug(f'Air readable name -> {air_readable_name}')
        if air_readable_name is None:
            return air_name
        return air_readable_name


parser = ParserService()
