from src.modules.ability.schemas.ability_schemas import AbilityBase
from sqlmodel import Field


class Ability(AbilityBase, table=True):
    __tablename__ = "ability"  # type: ignore

    id: int | None = Field(primary_key=True, index=True)
