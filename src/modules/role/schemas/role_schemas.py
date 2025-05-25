from pydantic import BaseModel, Field
from src.modules.role.schemas.permission_schemas import PermissionPublic


class RoleCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=100)
    permissions: list[PermissionPublic]


class RolePublic(RoleCreate):
    id: int = Field()


class RoleUpdate(BaseModel):
    name: str | None = Field(min_length=1, max_length=50, default=None)
    description: str | None = Field(min_length=1, max_length=100, default=None)
    permissions: list[PermissionPublic] | None = Field(default=None)
