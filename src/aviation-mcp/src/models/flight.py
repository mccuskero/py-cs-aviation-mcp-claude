from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class Flight(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    airport: str
    flight_number: str
    airline: str
    origin: str
    destination: str
    departure_time: str
    arrival_time: str
    status: str
    gate: str
    terminal: str
