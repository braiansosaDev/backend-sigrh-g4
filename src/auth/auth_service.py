from fastapi import HTTPException, status
from src.modules.employees.models.employee import Employee
from src.database.core import DatabaseSession
from src.auth.crypt import verify_password
from src.modules.employees.services import utils

def auth_login(db: DatabaseSession, user_id: str, password: str) -> Employee:
    """
    Obtiene un empleado por sus credenciales.
        Args:
            db (Session): Sesión de la base de datos.
            id (str): User ID del empleado a buscar.
            password (str): Contraseña del empleado.
        Returns:
            Employee: Empleado encontrado.
    """
    employee = utils.get_employee_by_user_id(db, user_id)

    if not employee or not employee.active or not employee.password or not verify_password(password, employee.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    return employee