from typing import Literal

from pydantic import BaseModel


class ApiSettingsData(BaseModel):

    api_ip: str
    api_port: int
    indicators_endpoint: str
    map_endpoint: str
    air_info_endpoint: str


class ApiSettings(BaseModel):

    api: ApiSettingsData


class PresenceSettingsData(BaseModel):

    show_indicators: bool
    lang: Literal['en', 'ru']
    logo_theme: Literal['main_red', 'main_white']


class PresenceSettings(BaseModel):

    presence: PresenceSettingsData
