from datetime import date
from pydantic import BaseModel, model_validator


class WorkHistoryResponse(BaseModel):
    """
    Modelo de respuesta para el historial laboral.
    Este modelo se utiliza para serializar los datos del historial laboral al enviarlos como respuesta a una solicitud.
    """

    id: int
    employee_id: int
    job_id: int
    from_date: date
    to_date: date
    company_name: str
    notes: str


class WorkHistoryRequest(BaseModel):
    """
    Modelo de creación para el historial laboral.
    Este modelo se utiliza para validar los datos de entrada al crear un nuevo historial laboral en la base de datos.
    """
    job_id: int
    from_date: date
    to_date: date
    company_name: str
    notes: str

    @model_validator(mode="before")
    @classmethod
    def validate_dates(cls, values):
        from_date = values.get("from_date")
        to_date = values.get("to_date")
        if from_date and to_date and from_date >= to_date:
            raise ValueError("from_date must be before to_date")
        return values