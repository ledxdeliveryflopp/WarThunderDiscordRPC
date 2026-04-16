import argparse
import os
import sys
from http import HTTPStatus

import httpx
from dotenv import load_dotenv
from loguru import logger

load_dotenv()


class Const:

    owner = 'ledxdeliveryflopp'
    repo = 'WarThunderDiscordRPC'
    token = os.getenv('TOKEN')

    api_version = '2022-11-28'
    create_url = f'https://api.github.com/repos/{owner}/{repo}/releases'
    upload_asset_url = f'https://uploads.github.com/repos/{owner}/{repo}/releases/'


def get_release_note() -> str:
    logger.info('Parsing release notes')
    with open('scripts/release_note.md', 'r', encoding='utf-8') as f:
        data = f.read()
    return data


def create_release(release_version: str) -> str:
    logger.info(f'Creating release -> {release_version}')
    response = httpx.post(
        url=Const.create_url,
        headers={
            'Authorization': f'Bearer {Const.token}',
            'X-GitHub-Api-Version': Const.api_version,
            'Accept': 'application/vnd.github+json',
        },
        json={
            'tag_name': release_version,
            'name': release_version,
            'target_commitish': 'main',
            'body': get_release_note(),
            'draft': False,
            'prerelease': False,
            'generate_release_notes': False,
            'make_latest': 'true',
        }
    )
    response_data = response.json()
    if response.status_code == HTTPStatus.CREATED:
        logger.info('Release created successfully.')
        return response_data['id']
    else:
        logger.error(f'Failed to create release -> {response_data}')
        sys.exit()


def get_asset_name(asset_path: str) -> str:
    return asset_path.split('/')[-1]


def upload_assets(release_id: str, asset_list: list[str]) -> None:
    logger.info(f'Upload assets in release - > {release_id}')
    logger.debug(f'Asset list -> {', '.join(i for i in asset_list)}')
    for asset_path in asset_list:
        with open(asset_path, 'rb') as asset_file:
            file_data = asset_file.read()
            asset_content_type = 'application/octet-stream'
            asset_name = get_asset_name(asset_path=asset_path)
            logger.debug(f'Upload -> {asset_name}')
            logger.debug(f'content-type -> {asset_content_type}')
            response = httpx.post(
                url=f'{Const.upload_asset_url}{release_id}/assets?',
                params={'name': asset_name},
                headers={
                    'Authorization': f'Bearer {Const.token}',
                    'Accept': 'application/vnd.github+json',
                    'X-GitHub-Api-Version': Const.api_version,
                    'content-type': asset_content_type,
                },
                data=file_data,
                timeout=120,
            )
            if response.status_code == HTTPStatus.CREATED:
                logger.info(f'Assets {asset_name} uploaded!')
            else:
                logger.error(f'Failed to upload {asset_name}')
                logger.error(response.json())

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument('--tag', type=str, help='Тэг релиза', required=True)
    parser.add_argument(
        '--assets',
        nargs='*',
        help='Ассеты релиза',
        required=True,
    )

    args = parser.parse_args()
    return args


if __name__ == '__main__':
    cli_args = parse_args()
    logger.debug(f'Args: {cli_args}')
    release_tag = cli_args.tag
    asset_list = cli_args.assets
    release_id = create_release(release_version=release_tag)
    upload_assets(release_id=release_id, asset_list=asset_list)
