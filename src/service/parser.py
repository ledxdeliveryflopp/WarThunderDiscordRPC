import asyncio
import os

import yaml
from loguru import logger
from pydoll.browser import Chrome
from pydoll.browser.options import ChromiumOptions
from yaml import SafeLoader

from src.settings import settings


class ParserService:

    @staticmethod
    @logger.catch
    def parse_tank_name(tank_tech_name: str) -> str:
        parsed_name = tank_tech_name.replace('tankModels/', '').lower()
        logger.debug(f'tank parse name result -> {parsed_name}')
        return parsed_name

    @staticmethod
    @logger.catch
    def get_readable_tank_name(tank_parsed_name: str) -> str:
        tank_readable_name = settings.ground_dict.get(tank_parsed_name, None)
        logger.debug(f'Tank readable name -> {tank_readable_name}')
        if tank_readable_name is None:
            return tank_parsed_name
        return tank_readable_name[settings.lang]

    @logger.catch
    def get_readable_air_name(self, air_name: str) -> str:
        air_readable_name = settings.air_dict.get(air_name, None)
        logger.debug(f'Air readable name -> {air_readable_name}')
        if air_readable_name is None:
            asyncio.run(self.__get_vehicle_name_from_wiki(vehicle_code=air_name))
            return air_name
        return air_readable_name[settings.lang]

    @staticmethod
    def __update_air_vehicle_list(
            air_tech_name: str, air_readable_name_ru: str, air_readable_name_en: str,
    ) -> None:
        with open('air_vehicle.yaml', 'r', encoding='utf-8') as air_data:
            data = yaml.load(air_data, Loader=SafeLoader)
            new_entry = {
                'ru': air_readable_name_ru,
                'en': air_readable_name_en,
            }
            data['air_list'][air_tech_name] = new_entry
        with open('air_vehicle.yaml', 'w', encoding='utf-8') as new_air_data:
            yaml.dump(data, new_air_data, allow_unicode=True, sort_keys=False)
            settings.reset_air_vehicle_settings()

    @staticmethod
    def __setup_browser() -> ChromiumOptions:
        options = ChromiumOptions()
        options.headless = True
        options.binary_location = 'chrome-win64/chrome.exe'
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--window-position=0,0')
        options.add_argument('--start-maximized')
        options.add_argument('--start-fullscreen')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-features=IsolateOrigins,site-per-process')
        options.add_argument('--use-gl=swiftshader')
        options.add_argument('--disable-features=WebGLDraftExtensions')
        options.add_argument('--force-webrtc-ip-handling-policy=disable_non_proxied_udp')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-background-networking')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-software-rasterizer')
        options.add_argument('--force-device-scale-factor=1')
        return options

    @logger.catch
    async def __get_vehicle_name_from_wiki(self, vehicle_code: str) -> None:
        options = self.__setup_browser()

        async with Chrome(options=options) as browser:
            tab = await browser.start()
            await tab.go_to(url=f'https://wiki.warthunder.com/unit/{vehicle_code}')
            await asyncio.sleep(3)
            screenshot_path = os.path.join(f'{os.getcwd()}/static', f'{vehicle_code}_en.png')
            await tab.take_screenshot(path=screenshot_path)
            en_title_bar = await tab.find(class_name='game-unit_name')
            if en_title_bar:
                en_title_text = await en_title_bar.text
                logger.debug(f'Vehicle title en -> {en_title_text}')
            else:
                logger.warning('Error while find en title locator')
            tab = await browser.start()
            await tab.go_to(url=f'https://wiki.warthunder.ru/unit/{vehicle_code}')
            await asyncio.sleep(3)
            screenshot_path = os.path.join(f'{os.getcwd()}/static', f'{vehicle_code}_ru.png')
            await tab.take_screenshot(path=screenshot_path)
            ru_title_bar = await tab.find(class_name='game-unit_name')
            if ru_title_bar:
                ru_title_text = await ru_title_bar.text
                logger.debug(f'Vehicle title ru -> {ru_title_text}')
            else:
                logger.debug('Error while find title ru locator')
            if ru_title_bar or en_title_bar:
                self.__update_air_vehicle_list(
                    air_tech_name=vehicle_code,
                    air_readable_name_ru=ru_title_text,
                    air_readable_name_en=en_title_text,
                )

    @logger.catch
    async def __get_vehicle_name_from_wiki_ru(self, vehicle_code: str) -> None:
        options = self.__setup_browser()

        async with Chrome(options=options) as browser:
            tab = await browser.start()
            await tab.go_to(url=f'https://wiki.warthunder.ru/unit/{vehicle_code}')
            await asyncio.sleep(3)
            screenshot_path = os.path.join(f'{os.getcwd()}/static', f'{vehicle_code}_ru.png')
            await tab.take_screenshot(path=screenshot_path)
            title_bar = await tab.find(class_name='game-unit_name')
            if title_bar:
                title_text = await title_bar.text
                logger.debug(f'Vehicle title ru -> {title_text}')
                self.__update_air_vehicle_list(air_tech_name=vehicle_code, air_readable_name=title_text)
            else:
                logger.debug('Error while find title locator')


parser = ParserService()
