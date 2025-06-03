from typing import Optional, Sequence
from fastapi import HTTPException, status
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from src.database.core import DatabaseSession
from src.modules.auth.token import TokenDependency
from src.modules.leave.schemas.leave_schemas import (
    LeaveDocumentStatus,
    LeaveRequestStatus,
    LeaveCreate,
    LeaveUpdate,
)
from src.modules.leave.models.leave_models import Leave, LeaveType
import logging

logger = logging.getLogger("uvicorn.error")


def get_leave_or_none(session: DatabaseSession, leave_id: int) -> Leave | None:
    return session.exec(select(Leave).where(Leave.id == leave_id)).one_or_none()


def get_leave(session: DatabaseSession, leave_id: int) -> Leave:
    leave = get_leave_or_none(session, leave_id)
    if leave is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No existe la solicitud de licencia con ID {leave_id}.",
        )
    return leave


def get_leaves(
    session: DatabaseSession,
    document_status: Optional[LeaveDocumentStatus],
    request_status: Optional[LeaveRequestStatus],
    employee_id: Optional[int],
) -> Sequence[Leave]:
    stmt = select(Leave)
    if document_status is not None:
        stmt = stmt.where(Leave.document_status == document_status)
    if request_status is not None:
        stmt = stmt.where(Leave.request_status == request_status)
    if employee_id is not None:
        stmt = stmt.where(Leave.employee_id == employee_id)
    return session.exec(stmt).all()


def create_leave(
    session: DatabaseSession, token: TokenDependency, request: LeaveCreate
) -> Leave:
    employee_id = token.get("employee_id")
    if not employee_id:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se encuentra el ID de empleado en el token.",
        )

    leave_type = session.exec(
        select(LeaveType).where(LeaveType.id == request.leave_type_id)
    ).one_or_none()

    if leave_type is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El tipo de licencia con ID {request.leave_type_id} no existe.",
        )

    db_leave = Leave(
        employee_id=employee_id,
        start_date=request.start_date,
        end_date=request.end_date,
        leave_type_id=request.leave_type_id,
        reason=request.reason,
        request_status=LeaveRequestStatus.PENDIENTE,
        document_status=(
            LeaveDocumentStatus.VALIDACION
            if leave_type.justification_required
            else LeaveDocumentStatus.NO_REQUERIDO
        ),
    )

    try:
        session.add(db_leave)
        session.commit()
        session.refresh(db_leave)
        return db_leave
    except IntegrityError as e:
        session.rollback()
        logger.error(
            f"Unexpected IntegrityError occurred while creating leave with data {request.model_dump_json()}"
        )
        logger.error(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def update_leave(session: DatabaseSession, leave_id: int, request: LeaveUpdate):
    db_leave: Leave = get_leave(session, leave_id)

    for attr, value in request.model_dump(exclude_unset=True).items():
        setattr(db_leave, attr, value)

    if db_leave.start_date > db_leave.end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La fecha de inicio no puede ser posterior a la fecha de fin.",
        )

    try:
        session.add(db_leave)
        session.commit()
        session.refresh(db_leave)
        return db_leave
    except IntegrityError as e:
        logger.error(
            f"Unexpected IntegrityError occurred while updating Leave with data {request.model_dump_json()}"
        )
        raise e


def get_leave_types(session: DatabaseSession) -> Sequence[LeaveType]:
    return session.exec(select(LeaveType)).all()


def get_leave_type_or_none(
    session: DatabaseSession, leave_type_id: int
) -> LeaveType | None:
    return session.exec(
        select(LeaveType).where(LeaveType.id == leave_type_id)
    ).one_or_none()


def get_leave_type(session: DatabaseSession, leave_type_id: int) -> LeaveType:
    result = get_leave_type_or_none(session, leave_type_id)
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El tipo de licencia con ID {leave_type_id} no existe.",
        )
    return result
