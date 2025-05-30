from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from typing import Optional
from sqlalchemy import LargeBinary


class Configuration(SQLModel, table=True):
    __tablename__ = "configuration"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    company_name: str
    primary_color: str
    secondary_color: str
    logo: bytes = Field(
        sa_column=Field(default=None, sa_column_kwargs={"type_": LargeBinary})
    )
    favicon: bytes = Field(
        sa_column=Field(default=None, sa_column_kwargs={"type_": LargeBinary})
    )
    email: EmailStr
    phone: str
