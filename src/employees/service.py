from fastapi import HTTPException, status
from src.employees.token import TokenDependency
from .employee_models import CreateEmployee
from sqlmodel import Session, select
from src.schemas.entities import Employee
from src.database.core import DatabaseSession
from sqlalchemy.exc import IntegrityError


def register_employee(db: Session, employee_request: CreateEmployee) -> Employee:
    db_employee = Employee(
        dni=employee_request.dni,
        email=employee_request.email,
        phone=employee_request.phone,
        full_name=employee_request.full_name,
        password=employee_request.password,  # GUARDAR LA PASS HASHEADA
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
    try:
        db.add(db_employee)
        db.commit()
        db.refresh(db_employee)
        return db_employee
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee with the provided phone, email, or DNI already exists.",
        )


def get_employee_by_id(db: DatabaseSession, employee_id: int) -> Employee:
    employee = db.exec(select(Employee).where(Employee.id == employee_id)).one_or_none()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )
    return employee


def get_employee_by_credentials(
    db: DatabaseSession, id: str, password: str
) -> Employee:
    print(f"ID: {id}, Password: {password}")

    employee = db.exec(
        select(Employee).where(
            (Employee.id == int(id)) & (Employee.password == password)
        )
    ).one_or_none()

    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found.",
        )
    return employee


def update_employee(
    db: DatabaseSession,
    employee_id: int,
    update_request: CreateEmployee,
    token: TokenDependency,
) -> Employee:
    try:
        employee = get_employee_by_id(db, employee_id)
        for attr, value in update_request.model_dump(exclude_unset=True).items():
            if hasattr(employee, attr):
                setattr(employee, attr, value)
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee with the provided phonealready exists.",
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred.",
        )


def delete_employee(db: DatabaseSession, employee_id: int) -> None:
    pass
