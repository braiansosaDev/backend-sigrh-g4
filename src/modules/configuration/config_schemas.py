from pydantic import BaseModel, StringConstraints
from typing import Annotated

ColorHex = Annotated[str, StringConstraints(pattern=r"^#(?:[0-9a-fA-F]{3}){1,2}$")]


class ConfigBase(BaseModel):
    company_name: str
    primary_color: ColorHex
    secondary_color: ColorHex
    logo: bytes
    favicon: bytes
    email: str
    phone: str


class ConfigRequest(ConfigBase):
    pass


class ConfigResponse(ConfigBase):
    id: int
