
class Git:

    GITHUB_API: str = 'https://api.github.com/repos/'
    GITHUB_OWNER: str = 'ledxdeliveryflopp'
    GITHUB_REPO: str = 'WarThunderDiscordRPC'
    GITHUB_PATH: str = '/releases/latest'

    latest_url = f'{GITHUB_API}{GITHUB_OWNER}/{GITHUB_REPO}{GITHUB_PATH}'


class Lang:

    hangar: dict = {'en': 'In hangar', 'ru': 'В ангаре'}
    loading: dict = {'en': 'Loading...', 'ru': 'Загружается...'}
    details: dict = {'en': 'Plays on', 'ru': 'Играет на'}
    tas_speed: dict = {'en': 'TAS speed', 'ru': 'Скорость TAS'}
    ias_speed: dict = {'en': 'IAS speed', 'ru': 'Скорость IAS'}
    radio_altitude: dict = {'en': 'Radio altitude', 'ru': 'Радиовысота'}
    absolute_altitude: dict = {
        'en': 'Absolute altitude', 'ru': 'Абсолютная высота',
    }
    tank_speed: dict = {'en': 'Speed', 'ru': 'Скорость'}
    tank_crew: dict = {'en': 'Crew', 'ru': 'Экипаж'}
    update_header: dict = {
        'en': 'WTDRP - version checker',
        'ru': 'WTDRP - информация об обновлениях',
    }
    update_message: dict = {
        'en': 'New app version available: ', 'ru': 'Доступна новая версия: ',
    }
    app_start_notify: dict = {
        'en': 'App started, version: ', 'ru': 'Приложение запущено, версия: ',
    }
    update_button: dict = {'en': 'Update', 'ru': 'Обновить'}
    skip_update_button: dict = {'en': 'Skip update', 'ru': 'Пропустить'}
    updater_dont_found: dict = {
        'en': 'updater.exe dont found', 'ru': 'updater.exe не найден',
    }
    close_tray: dict = {
        'en': 'Close app', 'ru': 'Закрыть приложение',
    }


class Constants:

    APP_VERSION = '2.11.0'
    game_name: str = 'War Thunder'
    presence_lang: Lang = Lang()
    github: Git = Git()


const = Constants()
