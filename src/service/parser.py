from functools import lru_cache
from typing import Literal

import httpx
import yaml
from bs4 import BeautifulSoup
from loguru import logger
from yaml import SafeLoader

from src.logger import app_logger
from src.service.api import WtApi
from src.service.spawner import gv_service
from src.settings import settings


class ParserService:

    @staticmethod
    @logger.catch
    @lru_cache
    def parse_tank_name(tank_tech_name: str) -> str:
        parsed_name = tank_tech_name.replace('tankModels/', '').lower()
        app_logger.debug(f'tank parse name result -> {parsed_name}')
        readable_name = parser.get_readable_tank_name(
            tank_parsed_name=parsed_name,
        )
        return readable_name

    @logger.catch
    def get_readable_tank_name(self, tank_parsed_name: str) -> str:
        tank_readable_name = settings.ground_dict.get(tank_parsed_name, None)
        app_logger.info(f'Tank readable name -> {tank_readable_name}')
        if tank_readable_name is None:
            self.__get_vehicle_name_from_wiki(
                vehicle_code=tank_parsed_name, army_type='tank',
            )
            return tank_parsed_name
        return tank_readable_name[settings.lang]

    @logger.catch
    def get_readable_air_name(self, air_name: str) -> str:
        air_readable_name = settings.air_dict.get(air_name, None)
        app_logger.info(f'Air readable name -> {air_readable_name}')
        if air_readable_name is None:
            self.__get_vehicle_name_from_wiki(
                vehicle_code=air_name, army_type='air',
            )
            return air_name
        return air_readable_name[settings.lang]

    @staticmethod
    @logger.catch
    def get_custom_vehicle_image(vehicle_tech_code: str) -> str:
        app_logger.debug(f'Get custom image for -> {vehicle_tech_code}')
        custom_images = settings.custom_images_data
        if vehicle_tech_code in custom_images:
            return vehicle_tech_code
        else:
            wiki_image = WtApi().get_vehicle_image(vehicle_tech_code)
            return wiki_image

    @staticmethod
    @logger.catch
    def __update_air_vehicle_list(
            air_tech_name: str,
            air_readable_name_ru: str,
            air_readable_name_en: str,
    ) -> None:
        app_logger.info('Updating air vehicle list')
        app_logger.debug(f'air tech name -> {air_tech_name}')
        app_logger.debug(f'air readable name ru -> {air_readable_name_ru}')
        app_logger.debug(f'air readable name en -> {air_readable_name_en}')
        with open(settings.air_file, 'r', encoding='utf-8') as air_data:
            data = yaml.load(air_data, Loader=SafeLoader)
            new_entry = {
                'ru': f'🛦{air_readable_name_ru}',
                'en': f'🛦{air_readable_name_en}',
            }
            data['air_list'][air_tech_name] = new_entry
        with open(settings.air_file, 'w', encoding='utf-8') as new_air_data:
            yaml.dump(data, new_air_data, allow_unicode=True, sort_keys=False)
            settings.reset_air_vehicle_settings()

    @staticmethod
    @logger.catch
    def __update_ground_vehicle_list(
            ground_tech_name: str,
            ground_readable_name_ru: str,
            ground_readable_name_en: str,
    ) -> None:
        app_logger.info('Updating ground vehicle list')
        app_logger.debug(f'ground tech name -> {ground_tech_name}')
        app_logger.debug(
            f'ground readable name ru -> {ground_readable_name_ru}',
        )
        app_logger.debug(
            f'ground readable name en -> {ground_readable_name_en}',
        )
        with open(settings.ground_file, 'r', encoding='utf-8') as air_data:
            data = yaml.load(air_data, Loader=SafeLoader)
            new_entry = {
                'ru': f'⚔{ground_readable_name_ru}',
                'en': f'⚔{ground_readable_name_en}',
            }
            data['ground_list'][ground_tech_name] = new_entry
        with open(
                settings.ground_file, 'w', encoding='utf-8'
        ) as new_ground_data:
            yaml.dump(
                data, new_ground_data, allow_unicode=True, sort_keys=False,
            )
            settings.reset_ground_vehicle_settings()

    @staticmethod
    @logger.catch
    def __setup_parser(response_html: str) -> BeautifulSoup:
        return BeautifulSoup(response_html, 'html.parser')

    @staticmethod
    def __get_wiki_page(
            vehicle_code: str, lang: Literal['en', 'ru'],
    ) -> str | None:
        urls = {
            'en': f'https://wiki.warthunder.com/unit/{vehicle_code}',
            'ru': f'https://wiki.warthunder.ru/unit/{vehicle_code}',
        }
        target_url = urls[lang]
        logger.info(f'Target url -> {target_url}')
        ru_response = httpx.get(target_url)
        if ru_response.status_code == 302:
            logger.info('Wiki redirect status')
            new_url = ru_response.headers.get('location')
            logger.info(f'Redirect url -> {new_url}')
            if not new_url:
                logger.warning('Empty location header')
                return None
            ru_response = httpx.get(new_url)
            if ru_response.status_code != 200:
                logger.error(f'Failed ru request -> {ru_response.status_code}')
            else:
                return ru_response.text
        if ru_response.status_code != 200:
            logger.error(
                f'Error while get ru status -> {ru_response.status_code}',
            )
            return None
        return ru_response.text

    def __find_vehicle_name(self, html_text: str) -> str | None:
        html_parser = self.__setup_parser(response_html=html_text)
        title = html_parser.find(class_='game-unit_name')
        title_text = title.get_text(strip=True) if title else None
        logger.info(f'Title text -> {title_text}')
        return title_text

    @logger.catch
    def __get_vehicle_name_from_wiki(
            self, vehicle_code: str, army_type: Literal['tank', 'air'],
    ) -> None:
        app_logger.info('Start search vehicle readable name!')
        app_logger.debug(f'Empty vehicle name -> {vehicle_code}')
        app_logger.debug(f'army_type -> {army_type}')
        en_url = f'https://wiki.warthunder.com/unit/{vehicle_code}'
        logger.info(f'Wiki en url -> {en_url}')
        gevent_tasks = []
        en_response_task = gv_service.spawn_task(
            target=self.__get_wiki_page,
            target_args=[vehicle_code, 'en'],
        )
        ru_response_task = gv_service.spawn_task(
            target=self.__get_wiki_page,
            target_args=[vehicle_code, 'ru'],
        )
        gevent_tasks.append(en_response_task)
        gevent_tasks.append(ru_response_task)
        gv_service.run_tasks(gevent_tasks)
        result = [task.value for task in gevent_tasks]
        en_response = result[0]
        ru_response = result[1]
        if en_response is None or ru_response is None:
            logger.error('One of response is empty')
            return None
        en_title_text_task = gv_service.spawn_task(
            target=self.__find_vehicle_name,
            target_args=en_response,
        )
        ru_title_text_task = gv_service.spawn_task(
            target=self.__find_vehicle_name,
            target_args=ru_response,
        )
        gevent_tasks.clear()
        gevent_tasks.append(en_title_text_task)
        gevent_tasks.append(ru_title_text_task)
        gv_service.run_tasks(gevent_tasks)
        result = [task.value for task in gevent_tasks]
        en_title_text = result[0]
        ru_title_text = result[1]
        if ru_title_text is not None and en_title_text is not None:
            if army_type == 'air':
                self.__update_air_vehicle_list(
                    air_tech_name=vehicle_code,
                    air_readable_name_ru=ru_title_text,
                    air_readable_name_en=en_title_text,
                )
            elif army_type == 'tank':
                self.__update_ground_vehicle_list(
                    ground_tech_name=vehicle_code,
                    ground_readable_name_ru=ru_title_text,
                    ground_readable_name_en=en_title_text,
                )


parser = ParserService()
