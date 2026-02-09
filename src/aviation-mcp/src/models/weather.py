from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class AirportWeather(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    airport: str
    condition: str
    temperature_f: float
    temperature_c: float
    wind_speed: str
    visibility: str
    humidity: int
    last_updated: str
