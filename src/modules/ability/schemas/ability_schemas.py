from pydantic import BaseModel, Field, field_validator
import logging


logger = logging.getLogger("uvicorn.error")


class AbilityRequest(BaseModel):
    """
    Utilizado para crear las Ability.
    """

    name: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=500)

    @field_validator("name", mode="before")
    @classmethod
    def empty_validator(cls, name):
        if type(name) is not str:
            raise TypeError("El nombre no es una string.")
        if not name.strip():
            raise ValueError("El nombre no puede estar vacío.")
        elif len(name) > 100:
            raise ValueError("El nombre no puede tener más de 100 caracteres.")
        return name

    @field_validator("description", mode="before")
    @classmethod
    def name_validator(cls, description):
        if type(description) is not str:
            raise TypeError("La descripción no es una string.")
        if not description.strip():
            raise ValueError("La descripción no puede estar vacía.")
        if len(description) > 500:
            raise ValueError("La descripción no puede tener más de 500 caracteres.")
        return description


class AbilityPublic(AbilityRequest):
    """
    Modelo de Ability ya creada que se puede usar
    tanto en requests como responses
    """
    id: int = Field()
