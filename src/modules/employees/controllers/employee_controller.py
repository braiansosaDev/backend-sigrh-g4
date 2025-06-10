from typing import Optional
from fastapi import APIRouter, status
from src.database.core import DatabaseSession
from src.modules.employees.services import employee_service
from src.auth.login_request import LoginRequest
from src.modules.employees.schemas.employee_models import (
    ChangePasswordRequest,
    CreateEmployee,
    EmployeeResponse,
    UpdateEmployee,
)

employee_router = APIRouter(prefix="/employees", tags=["Employees"])

@employee_router.post(
    "/active-count",
    status_code=status.HTTP_200_OK,
    summary="Cantidad de empleados activos",
)
async def count_active_employees(
    db: DatabaseSession,
):
    return {"active_count": employee_service.count_active_employees(db)}


"""Enpoint para buscar a un empleado por su ID.
Returns:
    EmployeeResponse: Devuelve los datos del empleado.
"""


@employee_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=list[EmployeeResponse],
)
async def get_all_employees(
    db: DatabaseSession,
    sector_id: Optional[int] = None
):
    return employee_service.get_all_employees(db, sector_id)


@employee_router.get(
    "/{employee_id}",
    status_code=status.HTTP_200_OK,
    response_model=EmployeeResponse,
)
async def get_employee_by_id(
    db: DatabaseSession,
    employee_id: int,
):
    return employee_service.get_employee(db, employee_id)


"""Enpoint para registrar un nuevo empleado.
Returns:
    EmployeeResponse: Devuelve los datos del empleado registrado.
"""


@employee_router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=EmployeeResponse,
)
async def register_employee(
    db: DatabaseSession,
    register_employee_request: CreateEmployee,
):
    return employee_service.create_employee(db, register_employee_request)


"""Endpoint para actualizar los datos de un empleado.
El empleado debe proporcionar su ID y los datos a actualizar.
El ID debe ser un número entero positivo.
El empleado debe estar autenticado para realizar esta operación.
El token de acceso se obtiene al iniciar sesión.
Returns:
    EmployeeResponse: Devuelve los datos del empleado actualizado.
"""


@employee_router.patch("/{employee_id}", status_code=status.HTTP_200_OK)
async def update_employee(
    db: DatabaseSession,
    employee_id: int,
    update_request: UpdateEmployee,
):
    return employee_service.update_employee(db, employee_id, update_request)


# TODO: Remplazar por el de abajo
@employee_router.post("/change_password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(
    db: DatabaseSession,
    model_request: ChangePasswordRequest
):
    return employee_service.change_password(
        db,
        model_request.employee_id,
        model_request.password
    )


# @employee_router.post("/change_password_token", status_code=status.HTTP_204_NO_CONTENT)
# async def change_password_token(
#     db: DatabaseSession,
#     token: TokenDependency,
#     employee_id: int,
#     password: str
# ):
#     return employee_service.change_password_token(
#         db,
#         token,
#         employee_id,
#         password
#     )



"""Endpoint para eliminar un empleado.
El empleado debe proporcionar su ID.
El ID debe ser un número entero positivo.
El empleado debe estar autenticado para realizar esta operación.
El token de acceso se obtiene al iniciar sesión.
Returns:
    CODE: 204
"""


@employee_router.delete("/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(
    db: DatabaseSession,
    employee_id: int,
):
    return employee_service.delete_employee(db, employee_id)
