from pydantic import BaseModel, EmailStr
from typing import Optional


class ConfigBase(BaseModel):
    company_name: str
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    logo: Optional[str]
    favicon: Optional[str]
    email: EmailStr
    phone: str


class ConfigRequest(ConfigBase):
    pass


class ConfigResponse(ConfigBase):
    id: int
