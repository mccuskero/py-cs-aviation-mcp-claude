from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class Gate(BaseModel):
    model_config = ConfigDict(populate_by_name=True, alias_generator=to_camel)

    airport: str
    gate_number: str
    terminal: str
    status: str
    assigned_flight: str
    airline: str
    last_updated: str
