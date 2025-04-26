from typing import Annotated
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

employee_router = APIRouter(prefix="/employees", tags=["Employees"])


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
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )


@employee_router.post("/login", status_code=status.HTTP_200_OK, response_model=dict)
async def login_employee(
    db: DatabaseSession,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    try:
        employee = service.get_employee_by_credentials(
            db, int(form_data.username), form_data.password
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


@employee_router.patch(
    "/{employee_id}", status_code=status.HTTP_200_OK, response_model=EmployeeResponse
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
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )


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
