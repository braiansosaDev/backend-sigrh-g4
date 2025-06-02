from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from typing import Optional


class Configuration(SQLModel, table=True):
    __tablename__ = "configuration"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    company_name: str
    primary_color: Optional[str]
    secondary_color: Optional[str]
    logo: Optional[str]  # Guardar en Base64
    favicon: Optional[str]  # Guardar en Base64
    email: EmailStr
    phone: str
