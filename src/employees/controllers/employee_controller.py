from typing import Annotated
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from src.database.core import DatabaseSession
from src.employees.services import employee_service
from src.auth.token import encode_token, TokenDependency
from src.schemas.employee_models import (
    CreateEmployee,
    EmployeeResponse,
    UpdateEmployee,
)

employee_router = APIRouter(prefix="/employees", tags=["Employees"])

"""Enpoint para buscar a un empleado por su ID. 
Returns:
    EmployeeResponse: Devuelve los datos del empleado.
"""


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


"""Endopint para iniciar sesión como empleado.
El empleado debe proporcionar su ID y contraseña.
El ID debe ser un número entero positivo.
Returns:
EmployeeResponse: Devuelve el token de acceso.
"""


@employee_router.post("/login", status_code=status.HTTP_200_OK, response_model=dict)
async def login_employee(
    db: DatabaseSession,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    employee = employee_service.login_employee(
        db, int(form_data.username), form_data.password
    )

    token = encode_token(
        {
            "username": employee.id,
            "password": employee.password,
        }
    )
    return {"access_token": token}


"""Endpoint para actualizar los datos de un empleado.
El empleado debe proporcionar su ID y los datos a actualizar.
El ID debe ser un número entero positivo.
El empleado debe estar autenticado para realizar esta operación.
El token de acceso se obtiene al iniciar sesión.
Returns:
    EmployeeResponse: Devuelve los datos del empleado actualizado.
"""


@employee_router.patch(
    "/{employee_id}", status_code=status.HTTP_200_OK, response_model=EmployeeResponse
)
async def update_employee(
    db: DatabaseSession,
    employee_id: int,
    update_request: UpdateEmployee,
    token: TokenDependency,
):
    return employee_service.update_employee(db, employee_id, update_request)


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
    token: TokenDependency,
):
    return employee_service.delete_employee(db, employee_id)
