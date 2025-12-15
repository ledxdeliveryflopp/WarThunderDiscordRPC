from typing import Literal, Optional

from pydantic import BaseModel, Field


class MainInfoSchemas(BaseModel):

    army_type: Literal['dummy_plane', 'air', 'tank'] = Field(alias='army')
    vehicle_tech_name: str = Field(alias='type')
    speed: Optional[float] = None
    crew_total: Optional[float] = None
    crew_current: Optional[float] = None
    radio_altitude: Optional[float] = None
    valid: bool


class MapInfoSchemas(BaseModel):

    valid: bool


class AircraftInfoSchemas(BaseModel):

    valid: bool
    tas_speed: int = Field(alias='TAS, km/h')
    ias_speed: int = Field(alias='IAS, km/h')
    mah_speed: float = Field(alias='M')
