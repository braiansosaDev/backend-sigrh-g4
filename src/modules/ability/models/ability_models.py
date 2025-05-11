from sqlmodel import SQLModel, Field


class AbilityBaseModel(SQLModel):
    """
    Contiene todos los atributos comunes
    de los modelos de Ability.
    """

    name: str = Field(max_length=50, unique=True)
    description: str | None = Field(max_length=100, default=None)


class AbilityIdModel(AbilityBaseModel):
    """
    Representa una Ability que se obtiene de la base de datos,
    y por lo tanto siempre tiene `id`.
    """

    id: int = Field(primary_key=True, index=True)


class AbilityModel(AbilityBaseModel, table=True):
    """
    Modelo de entidad Ability que se guarda en la base de datos.
    El `id` puede ser `None` porque es generado por la database.
    """

    __tablename__ = "ability"  # type: ignore
    id: int | None = Field(primary_key=True, index=True)
