from pydantic import (
    BaseModel,
    Field,
    AwareDatetime,
    FutureDate,
    model_validator,
)
from datetime import date
from typing import Optional
from enum import StrEnum, auto


class LeaveTypePublic(BaseModel):
    id: int = Field()
    type: str = Field()
    justification_required: bool = Field(default=False)


class LeaveDocumentStatus(StrEnum):
    NO_REQUERIDO = auto()
    VALIDACION = auto()
    APROBADO = auto()
    RECHAZADO = auto()


class LeaveRequestStatus(StrEnum):
    PENDIENTE = auto()
    APROBADO = auto()
    RECHAZADO = auto()


class LeaveCreate(BaseModel):
    start_date: FutureDate = Field()
    end_date: FutureDate = Field()
    leave_type_id: int = Field()
    reason: Optional[str] = Field(default=None)

    @model_validator(mode="after")
    def check_end_date(self) -> "LeaveCreate":
        if self.start_date > self.end_date:
            raise ValueError(
                "La fecha de inicio no puede ser posterior a la fecha de fin."
            )
        return self


class LeaveUpdate(BaseModel):
    start_date: Optional[date] = Field(default=None)
    end_date: Optional[date] = Field(default=None)
    leave_type_id: Optional[int] = Field(default=None)
    reason: Optional[str] = Field(default=None)
    document_status: Optional[str] = Field(default=None)
    request_status: Optional[str] = Field(default=None)

    @model_validator(mode="after")
    def check_dates(self) -> "LeaveUpdate":
        if (
            self.start_date is not None
            and self.end_date is not None
            and self.start_date > self.end_date
        ):
            raise ValueError(
                "La fecha de inicio no puede ser posterior a la fecha de fin."
            )
        return self


class LeavePublic(BaseModel):
    id: int = Field()
    employee_id: int = Field()
    request_date: date = Field()
    start_date: date = Field()
    end_date: date = Field()
    leave_type_id: int = Field()
    reason: Optional[str] = Field(default=None)
    document_status: LeaveDocumentStatus = Field()
    request_status: LeaveRequestStatus = Field()
    created_at: AwareDatetime = Field()
    updated_at: AwareDatetime = Field()

    @model_validator(mode="after")
    def check_end_date(self) -> "LeavePublic":
        if self.start_date > self.end_date:
            raise ValueError(
                "La fecha de inicio no puede ser posterior a la fecha de fin."
            )
        return self
