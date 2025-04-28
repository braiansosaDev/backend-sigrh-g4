from datetime import date
from sqlmodel import SQLModel


class WorkHistoryResponse(SQLModel):
    """
    Modelo de respuesta para el historial laboral.
    Este modelo se utiliza para serializar los datos del historial laboral al enviarlos como respuesta a una solicitud.
    """

    id: int
    employee_id: int
    job_title: str
    from_date: date
    to_date: date
    company_name: str
    notes: str


class WorkHistoryRequest(SQLModel):
    """
    Modelo de creación para el historial laboral.
    Este modelo se utiliza para validar los datos de entrada al crear un nuevo historial laboral en la base de datos.
    """

    job_title: str
    from_date: date
    to_date: date
    company_name: str
    notes: str
