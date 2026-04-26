import argparse
import logging
import os
import shutil

import PyInstaller.__main__
import yaml
from loguru import logger
from py7zr import py7zr


def build_app(build_info: list[str]) -> None:
    logger.info('Building app')
    PyInstaller.__main__.run(build_info)


def check_onefile(one_file_param: bool) -> str | None:
    if one_file_param is True:
        return '--onefile'
    else:
        return None


def check_windowed(windowed_param: bool) -> str | None:
    if windowed_param is True:
        return '--windowed'
    else:
        return None


def copy_additional_files(files: list[str]) -> None:
    logger.info('Copying additional files')
    for file_path in files:
        logger.info(f'Copying -> {file_path}')
        shutil.copy(file_path, 'dist')


def copy_browser_dir() -> None:
    logger.info('Copying browser directory')
    shutil.copytree('chrome-win64', 'dist/chrome-win64', dirs_exist_ok=True)


def copy_updater_service() -> None:
    logger.info('Copying updater service')
    shutil.copy2(
        'updater.exe',
        'dist/updater.exe',
    )


def get_release_files() -> list[str]:
    all_items = os.listdir('dist')
    return all_items


def set_default_vehicle_files() -> None:
    logger.info('Setting default vehicle list')
    with open('dist/ground_vehicle.yaml', 'w') as file:
        data = {'ground_list': {}}
        yaml.safe_dump(data, file)
    with open('dist/air_vehicle.yaml', 'w') as file:
        data = {'air_list': {}}
        yaml.safe_dump(data, file)


def set_default_app_settings() -> None:
    logger.info('Setting default app settings')
    with open('dist/settings.yaml', 'r') as file:
        data = yaml.safe_load(file)
    data['settings']['api']['api_ip'] = '127.0.0.1'
    data['settings']['api']['api_port'] = '8111'
    data['settings']['api']['indicators_endpoint'] = '/indicators'
    data['settings']['api']['map_endpoint'] = '/map_info.json'
    data['settings']['api']['air_info_endpoint'] = '/state'
    data['settings']['presence']['show_indicators'] = True
    data['settings']['presence']['lang'] = 'en'
    data['settings']['presence']['logo_theme'] = 'main_red'
    data['settings']['presence']['custom_images'] = True
    data['settings']['air_indicators']['air_speed_type'] = 'IAS'
    data['settings']['air_indicators']['altitude_type'] = 'ABSOLUTE'
    data['settings']['logger']['level'] = 'DEBUG'
    data['settings']['core']['timeout'] = 50
    data['settings']['core']['show_notification'] = True
    logger.debug(f'Settings -> {data}')
    with open('dist/settings.yaml', 'w') as file:
        yaml.safe_dump(data, file)


def zip_release():
    logger.info('Zipping release')
    files = get_release_files()
    with py7zr.SevenZipFile('dist/dist.7z', 'w') as archive:
        for file in files:
            file_path = f'dist/{file}'
            logger.debug(f'Zipping -> {file_path}')
            if os.path.isdir(file_path):
                archive.writeall(path=file_path, arcname=file)
            else:
                archive.write(file_path, arcname=file)


def build_app_spec(build_params: argparse.Namespace) -> list[str]:
    main_file_path = build_params.path
    main_file_ico = build_params.icon_path
    onefile = build_params.onefile
    windowed = build_params.windowed
    onefile_param = check_onefile(one_file_param=onefile)
    windowed_param = check_windowed(windowed_param=windowed)
    app_base_spec = [
        main_file_path,
        '--clean',
        '--name=WTDRP',
        '--icon',
        main_file_ico,
    ]
    if onefile_param:
        app_base_spec.append(onefile_param)
    if windowed_param:
        app_base_spec.append(windowed_param)
    logger.debug(f'Build params -> {app_base_spec}')
    return app_base_spec


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--path', type=str, help='Целевой файл сборки', required=True,
    )
    parser.add_argument(
        '--icon-path', type=str, help='Файл иконки', required=True,
    )
    parser.add_argument(
        '--onefile', action='store_true', help='Упаковка в один файл',
    )
    parser.add_argument(
        '--windowed', action='store_true', help='Запуск без консоли'
    )
    parser.add_argument(
        '--no-onefile',
        action='store_false',
        dest='onefile',
        help='Упаковка в несколько файлов',
    )
    parser.set_defaults(onefile=False)
    parser.add_argument(
        '--additional-files',
        nargs='*', help='Файлы для добавления в директорию', required=True,
    )

    args = parser.parse_args()
    return args


def clear_dist_dir() -> None:
    logger.info('Clearing dist')
    path_exist = os.path.exists('dist')
    if path_exist is True:
        shutil.rmtree('dist')
        logger.info('Dist cleared')


if __name__ == '__main__':
    logging.disable(logging.ERROR)
    logger.info('Start build')
    params = parse_args()
    logger.info(f'Start params -> {params}')
    clear_dist_dir()
    app_spec = build_app_spec(build_params=params)
    build_app(build_info=app_spec)
    copy_additional_files(files=params.additional_files)
    set_default_app_settings()
    set_default_vehicle_files()
    copy_browser_dir()
    copy_updater_service()
    zip_release()
    logger.info('Build complete')
