from pydantic import BaseModel, Field


class PermissionCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=100)


class PermissionPublic(PermissionCreate):
    id: str = Field(min_length=1, max_length=100)


class PermissionUpdate(BaseModel):
    name: str | None = Field(min_length=1, max_length=50, default=None)
    description: str | None = Field(min_length=1, max_length=100, default=None)
