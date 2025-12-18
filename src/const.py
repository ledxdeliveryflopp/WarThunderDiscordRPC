
class Lang:

    hangar: dict = {'en': 'In hangar', 'ru': 'В ангаре'}
    loading: dict = {'en': 'Loading...', 'ru': 'Загружается...'}
    details: dict = {'en': 'Plays on', 'ru': 'Играет на'}
    tas_speed: dict = {'en': 'TAS speed', 'ru': 'Скорость TAS'}
    ias_speed: dict = {'en': 'IAS speed', 'ru': 'Скорость IAS'}
    radio_altitude: dict = {'en': 'Radio altitude', 'ru': 'Радиовысота'}
    absolute_altitude: dict = {'en': 'Absolute altitude', 'ru': 'Абсолютная высота'}
    tank_speed: dict = {'en': 'Speed', 'ru': 'Скорость'}
    tank_crew: dict = {'en': 'Crew', 'ru': 'Экипаж'}


class Constants:

    game_name: str = 'War Thunder'
    presence_lang: Lang = Lang()


const = Constants()
