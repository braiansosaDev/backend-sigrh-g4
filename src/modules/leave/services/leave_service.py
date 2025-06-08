from typing import Optional, Sequence, cast, Any
from fastapi import HTTPException, status
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from src.database.core import DatabaseSession
from src.modules.auth.token import TokenDependency
from src.modules.employees.models.employee import Employee
from src.modules.employees.models.job import Job
from src.modules.leave.schemas.leave_schemas import (
    LeaveDocumentStatus,
    LeaveRequestStatus,
    LeaveCreate,
    LeaveUpdate,
)
from src.modules.leave.models.leave_models import Leave, LeaveType
from src.modules.employees.services import employee_service, sector_service
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
    sector_id: Optional[int],
) -> Sequence[Leave]:
    stmt = select(Leave).order_by(cast(Any, Leave.id))
    if document_status is not None:
        stmt = stmt.where(Leave.document_status == document_status)
    if request_status is not None:
        stmt = stmt.where(Leave.request_status == request_status)
    if employee_id is not None:
        stmt = stmt.where(Leave.employee_id == employee_id)
    if sector_id is not None:
        # Para dar error si no existe el sector
        sector_service.get_sector_by_id(session, sector_id)

        stmt = stmt.join(
            Employee, cast(Any, Leave.employee_id == Employee.id)
        ).join(
            Job, cast(Any, Employee.job_id == Job.id)
        ).where(Job.sector_id == sector_id)
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

    if leave_type.justification_required and not request.file:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El tipo de licencia '{leave_type.type}' requiere archivo de justificación obligatorio.",
        )

    db_leave = Leave(
        employee_id=employee_id,
        start_date=request.start_date,
        end_date=request.end_date,
        leave_type_id=request.leave_type_id,
        reason=request.reason,
        request_status=LeaveRequestStatus.PENDIENTE,
        document_status=(
            LeaveDocumentStatus.PENDIENTE_DE_VALIDACION
            if request.file
            else LeaveDocumentStatus.PENDIENTE_DE_CARGA
        ),
        file=request.file,
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


def update_leave(
    session: DatabaseSession,
    token: TokenDependency,
    leave_id: int,
    request: LeaveUpdate,
):
    db_leave: Leave = get_leave(session, leave_id)

    leave_author_employee = employee_service.get_employee(session, db_leave.employee_id)
    request_employee_id = token.get("employee_id")

    if db_leave.request_status in {LeaveRequestStatus.APROBADO, LeaveRequestStatus.RECHAZADO}:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="La solicitud ya está cerrada y no se puede editar."
        )

    if request_employee_id == leave_author_employee.id:
        if not set(request.dict(exclude_unset=True).keys()).issubset({'file'}):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No podés cambiar estados de tu propia solicitud."
            )

        if db_leave.document_status in {LeaveDocumentStatus.APROBADO, LeaveDocumentStatus.RECHAZADO}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="La documentación ya fue evaluada y no se puede editar."
            )

        if request.file is not None and request.file.strip():

            db_leave.file = request.file

            if db_leave.document_status == LeaveDocumentStatus.PENDIENTE_DE_CARGA:
                db_leave.document_status = LeaveDocumentStatus.PENDIENTE_DE_VALIDACION

        elif db_leave.leave_type.justification_required:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El tipo de licencia '{db_leave.leave_type.type}' requiere archivo de justificación obligatorio.",
            )

        try:
            session.add(db_leave)
            session.commit()
            session.refresh(db_leave)
            return db_leave
        except IntegrityError:
            session.rollback()
            logger.error(
                f"An unexpected error ocurred while updating Leave with ID {leave_id} and data {request.model_dump_json()}"
            )
            raise

    if request_employee_id is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No se encuentra el employee_id en el token.",
        )

    request_employee = employee_service.get_employee(session, request_employee_id)

    # TODO: Cambiar el ID del permiso por un enum sincronizado al data entry
    if (not request_employee.role
        or 10 not in list(map(lambda permission: permission.id, request_employee.role.permissions))
        or not set(request.dict(exclude_unset=True).keys()).issubset({'request_status', 'document_status'})
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tenés permiso para realizar esta acción o editar algunos campos."
        )

    if request.document_status is not None:
        db_leave.document_status = request.document_status

    if request.request_status is not None:
        db_leave.request_status = request.request_status
        if request.request_status is LeaveRequestStatus.APROBADO:
            db_leave.document_status = LeaveDocumentStatus.APROBADO

    try:
        session.add(db_leave)
        session.commit()
        session.refresh(db_leave)
        return db_leave
    except IntegrityError as e:
        logger.error(
            f"Unexpected IntegrityError occurred while updating Leave with ID {leave_id} and data {request.model_dump_json()}"
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
