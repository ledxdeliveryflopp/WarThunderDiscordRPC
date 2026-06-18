import time

from loguru import logger
from pypresence import ActivityType, PipeClosed, Presence
from pypresence.utils import get_ipc_path

from src.const import const
from src.logger import app_logger
from src.service.api import WtApi
from src.service.builder import Builder
from src.service.parser import parser
from src.service.spawner import gv_service
from src.settings import settings
from src.shemas.api import MainInfoSchemas


class PresenceService(Presence, WtApi, Builder):

    def __init__(self, client_id: str = '1344195597485211790'):
        self.start_time = time.time()
        super().__init__(client_id=client_id)

    def get_discord_pipe(self):
        try:
            ipc_pipe = get_ipc_path(self.pipe)
            app_logger.debug(f'Discord pipe -> {ipc_pipe}')
            return ipc_pipe
        except Exception as e:
            app_logger.warning(e)
            return None

    @logger.catch(exclude=(AssertionError, PipeClosed, RuntimeError))
    def set_menu_presence(self) -> None:
        app_logger.info('Set lobby presence')
        details = const.presence_lang.hangar[settings.lang]
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

    @logger.catch(exclude=(AssertionError, PipeClosed, RuntimeError))
    def set_loading_presence(self) -> None:
        app_logger.info('Set loading presence')
        details = const.presence_lang.loading[settings.lang]
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

    @logger.catch(exclude=(AssertionError, PipeClosed, RuntimeError))
    def set_air_presence(
            self, indicator_schemas: MainInfoSchemas,
    ) -> None:
        gevent_tasks = []
        vehicle_name = indicator_schemas.vehicle_tech_name
        if settings.custom_images is True:
            vehicle_image_task = gv_service.spawn_task(
                target=parser.get_custom_vehicle_image,
                target_args=vehicle_name,
            )
            gevent_tasks.append(vehicle_image_task)
        else:
            vehicle_image_task = gv_service.spawn_task(
                target=self.get_vehicle_image,
                target_args=vehicle_name,
            )
            gevent_tasks.append(vehicle_image_task)
        readable_name_task = gv_service.spawn_task(
            target=parser.get_readable_air_name,
            target_args=vehicle_name,
        )
        gevent_tasks.append(readable_name_task)
        details_info = const.presence_lang.details[settings.lang]
        if settings.show_indicators is True:
            states_schemas = self.get_air_state_request()
            state_task = gv_service.spawn_task(
                target=self.build_air_state,
                target_args=[indicator_schemas, states_schemas],
            )
            gevent_tasks.append(state_task)
        gv_service.run_tasks(gevent_tasks)
        results = [task.value for task in gevent_tasks]
        logger.info(f'Gevent results -> {results}')
        vehicle_image = results[0]
        readable_name = results[1]
        state = results[2] if settings.show_indicators is True else None
        details = f'{details_info}: {readable_name}'
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

    @logger.catch(exclude=(AssertionError, PipeClosed, RuntimeError))
    def set_tank_presence(self, indicator_schemas: MainInfoSchemas) -> None:
        vehicle_name = indicator_schemas.vehicle_tech_name
        gevent_tasks = []
        tank_parsed_name = parser.parse_tank_name(
            tank_tech_name=vehicle_name,
        )
        readable_name_task = gv_service.spawn_task(
            target=parser.get_readable_tank_name,
            target_args=tank_parsed_name,
        )
        gevent_tasks.append(readable_name_task)
        if settings.custom_images is True:
            vehicle_image_task = gv_service.spawn_task(
                target=parser.get_custom_vehicle_image,
                target_args=tank_parsed_name,
            )
            gevent_tasks.append(vehicle_image_task)
        else:
            vehicle_image_task = gv_service.spawn_task(
                target=self.get_vehicle_image,
                target_args=tank_parsed_name,
            )
            gevent_tasks.append(vehicle_image_task)
        details_info = const.presence_lang.details[settings.lang]
        gv_service.run_tasks(gevent_tasks)
        result = [task.value for task in gevent_tasks]
        readable_name = result[0]
        vehicle_image = result[1]
        details = f'{details_info}: {readable_name}'
        if settings.show_indicators is True:
            state = self.build_ground_state(
                indicators_schemas=indicator_schemas,
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

    @logger.catch(exclude=(AssertionError, PipeClosed, RuntimeError))
    def set_presence(self) -> None:
        try:
            app_logger.info('----Set presence----')
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
            app_logger.info('----Finish set presence----')
        except (AssertionError, PipeClosed) as error:
            app_logger.warning(error)
            app_logger.debug('Trying to connect discord')
            self.connect()


presence_service = PresenceService()
