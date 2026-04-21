from loguru import logger

from src.const import const
from src.logger import app_logger
from src.settings import settings
from src.shemas.api import MainInfoSchemas, AircraftInfoSchemas


class Builder:

    @staticmethod
    @logger.catch
    async def build_air_state(
            indicators_schemas: MainInfoSchemas,
            states_schemas: AircraftInfoSchemas,
    ) -> str:
        if settings.air_speed_type == 'TAS':
            speed = states_schemas.tas_speed
            state_info = const.presence_lang.tas_speed[settings.lang]
            speed_state = f'{state_info}: {speed}'
        elif settings.air_speed_type == 'IAS':
            speed = states_schemas.ias_speed
            state_info = const.presence_lang.ias_speed[settings.lang]
            speed_state = f'{state_info}: {speed}'
        alt_type = settings.altitude_type
        if alt_type == 'RADIO' and indicators_schemas.radio_altitude:
            altitude = int(indicators_schemas.radio_altitude)
            state_info = const.presence_lang.radio_altitude[settings.lang]
            altitude_state = f'{state_info}: {altitude}'
        elif alt_type == 'ABSOLUTE' or indicators_schemas.radio_altitude is None:
            altitude = int(states_schemas.water_altitude)
            state_info = const.presence_lang.absolute_altitude[settings.lang]
            altitude_state = f'{state_info}: {altitude}'
        state = f'{speed_state} | {altitude_state}'
        app_logger.debug(f'Air state -> {state}')
        return state

    @staticmethod
    @logger.catch
    async def build_ground_state(indicators_schemas: MainInfoSchemas) -> str:
        speed = int(indicators_schemas.speed)
        state_info = const.presence_lang.tank_speed[settings.lang]
        speed_state = f'{state_info}: {speed} km/h'
        current_crew_count = int(indicators_schemas.crew_current)
        total_crew_count = int(indicators_schemas.crew_total)
        crew_info = const.presence_lang.tank_crew[settings.lang]
        crew_state = f'{crew_info}: {current_crew_count}/{total_crew_count}'
        state = f'{speed_state} | {crew_state}'
        app_logger.debug(f'Ground state -> {state}')
        return state
