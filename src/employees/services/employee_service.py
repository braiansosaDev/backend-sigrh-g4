from fastapi import HTTPException, status
from src.schemas.entities import Employee
from src.schemas.employee_models import CreateEmployee
from src.database.core import DatabaseSession
from sqlalchemy.exc import IntegrityError
from src.auth.crypt import get_password_hash, verify_password
from src.employees.services import utils


def get_employee(db: DatabaseSession, employee_id: int):
    employee = utils.get_employee_by_id(db, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found."
        )

    return employee


def create_employee(db: DatabaseSession, employee_request: CreateEmployee) -> Employee:
    """
    Registra un nuevo empleado en la base de datos.
    Args:
        db (Session): Sesión de la base de datos.
        employee_request (CreateEmployee): Datos del empleado a registrar.
    Returns:
        Employee: Empleado registrado.
    """
    try:
        db_employee = Employee(
            dni=employee_request.dni,
            email=employee_request.email,
            phone=employee_request.phone,
            full_name=employee_request.full_name,
            password=get_password_hash(employee_request.password),
            department=employee_request.department,
            job_title=employee_request.job_title,
            address=employee_request.address,
            nationality=employee_request.nationality,
            hire_date=employee_request.hire_date,
            birth_date=employee_request.birth_date,
            salary=employee_request.salary,
            photo=employee_request.photo,
            facial_register=employee_request.facial_register,
        )
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee with this DNI, phone or email already exists.",
        )


def login_employee(db: DatabaseSession, id: int, password: str) -> Employee:
    """
    Obtiene un empleado por sus credenciales.
        Args:
            db (Session): Sesión de la base de datos.
            id (int): ID del empleado a buscar.
            password (str): Contraseña del empleado.
        Returns:
            Employee: Empleado encontrado.
    """
    employee = utils.get_employee_by_id(db, id)

    if not employee or not verify_password(password, employee.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid credentials",
        )
    return employee


def update_employee(
    db: DatabaseSession,
    employee_id: int,
    update_request: CreateEmployee,
) -> Employee:
    """
    Actualiza los datos de un empleado en la base de datos.
    Args:
        db (Session): Sesión de la base de datos.
        employee_id (int): ID del empleado a actualizar.
        update_request (CreateEmployee): Datos a actualizar.
    Returns:
        Employee: Empleado actualizado.
    """
    employee = utils.get_employee_by_id(db, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found."
        )

    try:
        for attr, value in update_request.model_dump(exclude_unset=True).items():
            if hasattr(employee, attr):
                setattr(employee, attr, value)

        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee with this DNI, phone or email already exists.",
        )


def delete_employee(db: DatabaseSession, employee_id: int) -> None:
    """
    Elimina un empleado de la base de datos.
    Args:
        db (Session): Sesión de la base de datos.
        employee_id (int): ID del empleado a eliminar.
    Returns:
        None
    """
    employee = utils.get_employee_by_id(db, employee_id)
    work_history = utils.get_work_history_of_employee(db, employee_id)
    documents = utils.get_documents_of_employee(db, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found."
        )

    for document in documents:
        db.delete(document)
        db.commit()

    for history in work_history:
        db.delete(history)
        db.commit()

    db.delete(employee)
    db.commit()
