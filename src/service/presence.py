import time

from loguru import logger
from pypresence import Presence, ActivityType

from src.const import const
from src.service.api import WtApi
from src.service.builder import Builder
from src.service.parser import parser
from src.settings import settings
from src.shemas.api import MainInfoSchemas


class PresenceService(Presence, WtApi, Builder):

    def __init__(self, client_id: str = '1344195597485211790'):
        self.start_time = time.time()
        super().__init__(client_id=client_id)
        self.connect()

    def set_menu_presence(self) -> None:
        logger.debug('Set lobby presence')
        details = 'В ангаре'
        state = None
        self.update(
            activity_type=ActivityType.PLAYING,
            details=details,
            state=state,
            large_image=settings.logo_theme,
            large_text=const.game_name,
            small_text=const.game_name,
            small_image=None,
            start=self.start_time
        )

    def set_loading_presence(self) -> None:
        logger.debug('Set loading presence')
        details = 'Загружается...'
        state = None
        self.update(
            activity_type=ActivityType.PLAYING,
            details=details,
            state=state,
            large_image=settings.logo_theme,
            large_text=const.game_name,
            small_text=const.game_name,
            small_image=None,
            start=self.start_time
        )

    def set_air_presence(self, indicator_schemas: MainInfoSchemas) -> None:
        vehicle_name = indicator_schemas.vehicle_tech_name
        vehicle_image = self.get_vehicle_image(vehicle_tech_name=vehicle_name)
        readable_name = parser.get_readable_air_name(air_name=vehicle_name)
        details_info = const.presence_lang.details[settings.lang]
        details = f'{details_info}: {readable_name}'
        if settings.show_indicators is True:
            states_schemas = self.get_air_state_request()
            state = self.build_air_state(
                indicators_schemas=indicator_schemas,
                states_schemas=states_schemas,
            )
        else:
            state = None
        self.update(
            activity_type=ActivityType.PLAYING,
            details=details,
            state=state,
            large_image=vehicle_image,
            large_text=readable_name,
            small_text=const.game_name,
            small_image=settings.logo_theme,
            start=self.start_time
        )

    def set_tank_presence(self, indicator_schemas: MainInfoSchemas) -> None:
        vehicle_name = indicator_schemas.vehicle_tech_name
        tank_parsed_name = parser.parse_tank_name(tank_tech_name=vehicle_name)
        vehicle_image = self.get_vehicle_image(vehicle_tech_name=tank_parsed_name)
        readable_name = parser.get_readable_tank_name(tank_parsed_name=tank_parsed_name)
        details_info = const.presence_lang.details[settings.lang]
        details = f'{details_info}: {readable_name}'
        if settings.show_indicators is True:
            state = self.build_ground_state(indicators_schemas=indicator_schemas)
        else:
            state = None
        self.update(
            activity_type=ActivityType.PLAYING,
            details=details,
            state=state,
            large_image=vehicle_image,
            large_text=readable_name,
            small_text=const.game_name,
            small_image=settings.logo_theme,
            start=self.start_time
        )

    def set_presence(self) -> None:
        logger.info('----Set presence----')
        map_info = self.get_map_info()
        if not map_info or map_info.valid is False:
            self.set_menu_presence()
            return
        main_info = self.get_main_info()
        army_type = main_info.army_type
        vehicle_name = main_info.vehicle_tech_name
        if army_type == 'dummy_plane' or vehicle_name == 'dummy_plane':
            self.set_loading_presence()
        elif army_type == 'air':
            self.set_air_presence(indicator_schemas=main_info)
        elif army_type == 'tank':
            self.set_tank_presence(indicator_schemas=main_info)
        logger.info('----Finish set presence----')


presence_service = PresenceService()
