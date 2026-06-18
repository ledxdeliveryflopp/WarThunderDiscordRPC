import asyncio
import json
import os.path
import time

import httpx
from bs4 import BeautifulSoup
from loguru import logger


class MetricsService:

    url = 'https://api.github.com/repos/ledxdeliveryflopp/WarThunderDiscordRPC/releases' # noqa
    ru_steam = 'https://steamcommunity.com/sharedfiles/filedetails/?id=3713937093' # noqa
    en_steam = 'https://steamcommunity.com/sharedfiles/filedetails/?id=3713947315' # noqa

    async def get_releases_data(self) -> list[dict]:
        async with httpx.AsyncClient() as client:
            response = await client.get(self.url)
            releases = response.json()[:3]
            return releases

    async def git_download_counts(self):
        releases = await self.get_releases_data()
        revers = reversed(releases)
        for release in revers:
            release_tag = release['tag_name']
            download_count = release['assets'][0]['download_count']
            print('-' * 10)
            print(f'Release -> {release_tag}')
            print(f'Download Count -> {download_count}')
            print('-' * 10)
        return releases

    async def get_en_steam_stats(self) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(self.en_steam)
            soup = BeautifulSoup(response.text, 'html.parser')
            result = {}
            for tr in soup.select('table.stats_table tr'):
                cells = [td.get_text(strip=True) for td in tr.find_all('td')]
                if len(cells) >= 2:
                    result[cells[1]] = cells[0]
            print('*' * 10 + 'EN STEAM' + '*' * 10)
            print(result)
            return result

    async def get_ru_steam_stats(self) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(self.ru_steam)
            soup = BeautifulSoup(response.text, 'html.parser')
            result = {}
            for tr in soup.select('table.stats_table tr'):
                cells = [td.get_text(strip=True) for td in tr.find_all('td')]
                if len(cells) >= 2:
                    result[cells[1]] = cells[0]
            print('*' * 10 + 'RU STEAM' + '*' * 10)
            print(result)
            return result

    @staticmethod
    async def save_metrics(
            git_download: dict,
            steam_visitors: dict,
            steam_fav: dict,
    ) -> None:
        check = os.path.exists('metrics.json')
        save_data = {
                'git_download': git_download,
                'steam_visitors': steam_visitors,
                'steam_fav': steam_fav,
        }
        if not check:
            with open('metrics.json', 'w+') as file:
                data = {time.time(): save_data}
                file.write(json.dumps(data, indent=4))
        else:
            with open('metrics.json', 'r') as file:
                data = json.load(file)
            data[time.time()] = save_data
            with open('metrics.json', 'w+') as file:
                file.write(json.dumps(data, indent=4))

    async def get_metrics(self) -> None:
        git_releases = await self.git_download_counts()
        en_steam_data = await self.get_en_steam_stats()
        ru_steam_data = await self.get_ru_steam_stats()
        steam_visitors = {
            'en': en_steam_data['Unique Visitors'],
            'ru': ru_steam_data['Unique Visitors'],
        }
        steam_favorite = {
            'en': en_steam_data['Current Favorites'],
            'ru': ru_steam_data['Current Favorites'],
        }
        git_info = git_releases[:3]
        git_data = {}
        for release in git_info:
            release_tag = release['tag_name']
            download_count = release['assets'][0]['download_count']
            git_data[release_tag] = {'download_count': download_count}
        await self.save_metrics(
            git_download=git_data,
            steam_visitors=steam_visitors,
            steam_fav=steam_favorite,
        )


if __name__ == '__main__':
    metrics = MetricsService()
    while True:
        asyncio.run(metrics.get_metrics())
        time.sleep(500)
