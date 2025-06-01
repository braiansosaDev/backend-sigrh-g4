from pydantic import BaseModel, EmailStr
from typing import Optional


class ConfigBase(BaseModel):
    company_name: str
    primary_color: Optional[str]
    secondary_color: Optional[str]
    logo: str
    favicon: str
    email: EmailStr
    phone: str


class ConfigRequest(ConfigBase):
    pass


class ConfigResponse(ConfigBase):
    id: int
