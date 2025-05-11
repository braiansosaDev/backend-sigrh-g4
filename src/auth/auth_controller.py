from fastapi import HTTPException, status, APIRouter
from src.database.core import DatabaseSession
from src.auth import auth_service
from src.auth.login_request import LoginRequest
from src.auth.token import encode_token

"""Endopint para iniciar sesión como empleado.
El empleado debe proporcionar su ID y contraseña.
El ID debe ser un número entero positivo.
Returns:
EmployeeResponse: Devuelve el token de acceso.
"""
auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Username must be a number. Error: {e}",
        )
    token = encode_token(
        {
            "employee_id": employee.id,  # 👈 este es el dato clave
            "user_id": employee.user_id,
        }
    )

    return {"access_token": token}