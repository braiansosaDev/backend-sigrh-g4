from pydantic import (
    BaseModel,
    Field,
    AwareDatetime,
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
    PENDIENTE_DE_CARGA = auto()
    PENDIENTE_DE_VALIDACION = auto()
    APROBADO = auto()
    RECHAZADO = auto()


class LeaveRequestStatus(StrEnum):
    PENDIENTE = auto()
    APROBADO = auto()
    RECHAZADO = auto()


class LeaveCreate(BaseModel):
    start_date: date = Field()
    end_date: date = Field()
    leave_type_id: int = Field()
    reason: Optional[str] = Field(default=None)
    file: Optional[str] = Field(min_length=1, default=None)

    @model_validator(mode="after")
    def check_end_date(self) -> "LeaveCreate":
        if self.start_date > self.end_date:
            raise ValueError(
                "La fecha de inicio no puede ser posterior a la fecha de fin."
            )
        return self


class LeaveUpdate(BaseModel):
    document_status: Optional[LeaveDocumentStatus] = Field(default=None)
    request_status: Optional[LeaveRequestStatus] = Field(default=None)
    file: Optional[str] = Field(min_length=1, default=None)


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
    file: Optional[str] = Field(default=None)
    created_at: AwareDatetime = Field()
    updated_at: AwareDatetime = Field()

    @model_validator(mode="after")
    def check_end_date(self) -> "LeavePublic":
        if self.start_date > self.end_date:
            raise ValueError(
                "La fecha de inicio no puede ser posterior a la fecha de fin."
            )
        return self


class GetRequest(BaseModel):
    model_config = {"extra": "forbid"}

    document_statuses: Optional[list[LeaveDocumentStatus]] = None
    request_statuses: Optional[list[LeaveRequestStatus]] = None
    employee_ids: Optional[list[int]] = None
    sector_ids: Optional[list[int]] = None
    leave_type_ids: Optional[list[int]] = None
    from_start_date: Optional[date] = None
    until_start_date: Optional[date] = None

    @model_validator(mode="after")
    def validate_dates(self) -> "GetRequest":
        if self.from_start_date and self.until_start_date:
            if self.until_start_date < self.from_start_date:
                raise ValueError("La fecha 'hasta' no puede ser anterior que la fecha 'desde'.")
        return self


class ReportRequest(BaseModel):
    model_config = {"extra": "forbid"}

    from_start_date: Optional[date] = None
    until_start_date: Optional[date] = None
    sector_ids: Optional[list[int]] = None
    request_statuses: Optional[list[LeaveRequestStatus]] = None
    leave_type_ids: Optional[list[int]] = None

    @model_validator(mode="after")
    def validate_dates(self) -> "ReportRequest":
        if self.from_start_date and self.until_start_date:
            if self.until_start_date < self.from_start_date:
                raise ValueError("La fecha 'hasta' no puede ser anterior que la fecha 'desde'.")
        return self


class ReportResponse(BaseModel):
    model_config = {"extra": "forbid"}

    report: dict[int, tuple[str, int]]
