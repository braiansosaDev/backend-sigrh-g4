from fastapi import HTTPException, status, APIRouter
from sqlmodel import select
from src.database.core import DatabaseSession
from src.modules.auth import auth_service
from src.modules.auth.login_request import LoginRequest
from src.modules.auth.token import TokenDependency, encode_token
from src.modules.employees.models.employee import Employee
from sqlalchemy.orm import selectinload
from src.modules.employees.models.job import Job
from src.modules.employees.schemas.employee_models import MeResponse
from src.modules.role.models.role_models import Role
import logging

logger = logging.getLogger("uvicorn.error")

"""
Endopint para iniciar sesión como empleado.
El empleado debe proporcionar su ID y contraseña.
El ID debe ser un número entero positivo.
Returns:
EmployeeResponse: Devuelve el token de acceso.
"""
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


@auth_router.get("/me", status_code=status.HTTP_200_OK, response_model=MeResponse)
def get_my_data(db: DatabaseSession, payload: TokenDependency):
    employee_id = payload.get("employee_id")

    if not employee_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ID de empleado no encontrado en el token"
        )

    stmt = (
        select(Employee)
        .where(Employee.id == employee_id)
        .options(
            selectinload(Employee.job).selectinload(Job.sector),
            selectinload(Employee.state),
            selectinload(Employee.country),
            selectinload(Employee.role_entity).selectinload(Role.permissions),
        )
    )
    employee = db.exec(stmt).one_or_none()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Empleado no encontrado"
        )

    return employee


@auth_router.post("/login", status_code=status.HTTP_200_OK, response_model=dict)
async def auth_login(
    db: DatabaseSession,
    login_request: LoginRequest,
):
    try:
        employee = auth_service.auth_login(
            db, login_request.user_id, login_request.password
        )
    except ValueError as e:
        logger.error(f"Unexpected error while processing login:\n{e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    token = encode_token(
        {
            "employee_id": employee.id,  # 👈 este es el dato clave
            "user_id": employee.user_id,
        }
    )

    return {"access_token": token}
