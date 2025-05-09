from pydantic import BaseModel, Field, field_validator
import logging


logger = logging.getLogger("uvicorn.error")

def validate_name(name):
    if name is None:
        raise ValueError("El nombre no puede ser None")
    if type(name) is not str:
        raise TypeError(f"El nombre no es una string, es {type(name)}.")
    if not name.strip():
        raise ValueError("El nombre no puede estar vacío.")
    if len(name) > 100:
        raise ValueError("El nombre no puede tener más de 100 caracteres.")
    return name


def validate_description(description):
    if type(description) is not str:
        return description
    if len(description) > 100:
        raise ValueError("La descripción no puede tener más de 100 caracteres.")
    return description


class AbilityUpdate(BaseModel):
    """
    Utilizado para actualizar las Ability
    """

    name: str | None = Field(min_length=1, max_length=100, default=None)
    description: str | None = Field(max_length=100, default=None)

    @field_validator("name", mode="before")
    @classmethod
    def name_validator(cls, name) -> str:
        return validate_name(name)

    @field_validator("description", mode="before")
    @classmethod
    def description_validator(cls, description) -> str | None:
        return validate_description(description)


class AbilityRequest(BaseModel):
    """
    Utilizado para crear las Ability.
    """

    name: str = Field(min_length=1, max_length=100)
    description: str | None = Field(max_length=100, default=None)

    @field_validator("name", mode="before")
    @classmethod
    def name_validator(cls, name) -> str:
        return validate_name(name)

    @field_validator("description", mode="before")
    @classmethod
    def description_validator(cls, description) -> str | None:
        return validate_description(description)


class AbilityPublic(AbilityRequest):
    """
    Modelo de Ability ya creada que se puede usar
    tanto en requests como responses
    """
    id: int = Field()
