import time

from loguru import logger
from pypresence import Presence, ActivityType

from src.const import const
from src.service.api import WtApi
from src.service.parser import parser
from src.settings import settings


class PresenceService(Presence, WtApi):

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

    def set_air_presence(self, vehicle_name: str) -> None:
        vehicle_image = self.get_vehicle_image(vehicle_tech_name=vehicle_name)
        readable_name = parser.get_readable_air_name(air_parsed_name=vehicle_name)
        details = f'Играет на: {readable_name}'
        state = None
        self.update(
            activity_type=ActivityType.PLAYING,
            details=details,
            state=state,
            large_image=vehicle_image,
            large_text=vehicle_name,
            small_text=const.game_name,
            small_image=settings.logo_theme,
            start=self.start_time
        )

    def set_tank_presence(self, vehicle_name: str) -> None:
        tank_parsed_name = parser.parse_tank_name(tank_tech_name=vehicle_name)
        vehicle_image = self.get_vehicle_image(vehicle_tech_name=tank_parsed_name)
        readable_name = parser.get_readable_tank_name(tank_parsed_name=tank_parsed_name)
        details = f'Играет на: {readable_name}'
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
        logger.debug('----Set presence----')
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
            self.set_air_presence(vehicle_name=vehicle_name)
        elif army_type == 'tank':
            self.set_tank_presence(vehicle_name=vehicle_name)
        logger.debug('----Finish set presence----')


presence_service = PresenceService()
