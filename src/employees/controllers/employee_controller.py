from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.database.core import DatabaseSession
from src.employees import service
from src.employees.token import encode_token, TokenDependency
from src.employees.employee_models import (
    CreateEmployee,
    EmployeeResponse,
    UpdateEmployee,
)
from src.schemas.login_request import LoginRequest

employee_router = APIRouter(prefix="/employees", tags=["Employees"])

"""Enpoint para buscar a un empleado por su ID. 
Returns:
    EmployeeResponse: Devuelve los datos del empleado.
"""

@employee_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[EmployeeResponse],
)
async def get_all_employees(
    db: DatabaseSession,
):
    try:
        return service.get_all_employees(db)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )

@employee_router.get(
    "/{employee_id}",
    status_code=status.HTTP_200_OK,
    response_model=EmployeeResponse,
)
async def get_employee_by_id(
    db: DatabaseSession,
    employee_id: int,
):
    try:
        return service.get_employee_by_id(db, employee_id)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )


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
    try:
        return service.register_employee(db, register_employee_request)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error: {str(e)}",
        )


"""Endopint para iniciar sesión como empleado.
El empleado debe proporcionar su ID y contraseña.
El ID debe ser un número entero positivo.
Returns:
EmployeeResponse: Devuelve el token de acceso.
"""


@employee_router.post("/login", status_code=status.HTTP_200_OK, response_model=dict)
async def login_employee(
    db: DatabaseSession,
    login_request: LoginRequest,
):
    try:
        employee = service.get_employee_by_credentials(
            db, int(login_request.username), login_request.password
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid username format. Username must be a number.",
        )
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
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
    "/{employee_id}", status_code=status.HTTP_200_OK
)
async def update_employee(
    db: DatabaseSession,
    employee_id: int,
    update_request: UpdateEmployee,
    token: TokenDependency,
):
    try:
        return service.update_employee(db, employee_id, update_request)
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )


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
    try:
        return service.delete_employee(db, employee_id)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )
