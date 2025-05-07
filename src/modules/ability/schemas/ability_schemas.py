from sqlmodel import SQLModel, Field


class AbilityBase(SQLModel):
    name: str = Field(max_length=50, unique=True, index=True)
    description: str = Field(max_length=100)


class AbilityPublic(AbilityBase):
    id: int = Field(primary_key=True, index=True)
