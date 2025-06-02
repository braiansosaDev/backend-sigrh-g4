from sqlmodel import SQLModel, Field, Relationship


class RolePermission(SQLModel, table=True):
    __tablename__: str = "role_permission" # type: ignore

    role_id: int = Field(foreign_key="role.id", primary_key=True, index=True, ondelete="CASCADE")
    permission_id: int = Field(foreign_key="permission.id", primary_key=True, index=True, ondelete="CASCADE")


class Permission(SQLModel, table=True):
    __tablename__: str = "permission" # type: ignore

    id: int | None = Field(primary_key=True, index=True, default=None)
    name: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=100)
    roles: list["Role"] = Relationship(back_populates="permissions", link_model=RolePermission)


class Role(SQLModel, table=True):
    __tablename__: str = "role" # type: ignore

    id: int | None = Field(primary_key=True, index=True, default=None)
    name: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1, max_length=100)
    permissions: list[Permission] = Relationship(back_populates="roles", link_model=RolePermission)
