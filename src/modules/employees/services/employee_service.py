from typing import List
from fastapi import HTTPException, status
from src.modules.employees.models.employee import Employee
from src.modules.employees.models.work_history import WorkHistory
from src.modules.employees.models.documents import Document
from src.modules.employees.schemas.employee_models import (
    CreateEmployee,
    EmployeeResponse,
    UpdateEmployee,
)
from src.database.core import DatabaseSession
from sqlalchemy.exc import IntegrityError
from src.auth.crypt import get_password_hash
from src.modules.employees.services import utils


def count_active_employees(db: DatabaseSession) -> int:
    result = utils.count_active_employees(db)
    return result


def get_all_employees(db: DatabaseSession) -> List[EmployeeResponse]:
    employees = utils.get_all_employees(db)

    if employees is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found."
        )
    return employees


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
        # Convertir documentos
        documents = (
            [Document(**doc.model_dump()) for doc in employee_request.documents]
            if employee_request.documents
            else []
        )

        # Convertir historial laboral
        work_histories = (
            [
                WorkHistory(**history.model_dump())
                for history in employee_request.work_histories
            ]
            if employee_request.work_histories
            else []
        )

        hashed_password = (
            get_password_hash(employee_request.password)
            if employee_request.password
            else None
        )

        db_employee = Employee(
            user_id=utils.create_user_id(db, employee_request),
            first_name=employee_request.first_name,
            last_name=employee_request.last_name,
            dni=employee_request.dni,
            type_dni=employee_request.type_dni,
            personal_email=employee_request.personal_email,
            active=employee_request.active,
            role=employee_request.role,
            password=hashed_password,
            phone=employee_request.phone,
            salary=employee_request.salary,
            job_id=employee_request.job_id,
            birth_date=employee_request.birth_date,
            hire_date=employee_request.hire_date,
            photo=employee_request.photo,
            address_street=employee_request.address_street,
            address_city=employee_request.address_city,
            address_cp=employee_request.address_cp,
            address_state_id=employee_request.address_state_id,
            address_country_id=employee_request.address_country_id,
            work_histories=work_histories,
            documents=documents,
            shift_id=employee_request.shift_id,
        )
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    except IntegrityError as e:
        db.rollback()
        # Podés refinar el mensaje si querés analizar `str(e.orig)`
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ya existe un empleado con datos únicos duplicados (DNI, email, user_id, etc).",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )


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
    employee = utils.get_employee_by_id_simple(db, employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found."
        )

    try:
        update_data = update_request.model_dump(exclude_unset=True)

        # Si se actualiza la contraseña, se rehashea
        if "password" in update_data:
            update_data["password"] = get_password_hash(update_data["password"])

        for attr, value in update_data.items():
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
            detail="Error de validación: Usuario, DNI, Mail o Telefono ya está siendo utilizado",
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
