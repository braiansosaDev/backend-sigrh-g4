from fastapi import HTTPException, status
from src.employees.token import TokenDependency
from .employee_models import CreateEmployee
from sqlmodel import Session, select
from src.schemas.entities import Employee
from src.database.core import DatabaseSession
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def register_employee(db: Session, employee_request: CreateEmployee) -> Employee:
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
    try:
        employee = db.exec(
            select(Employee).where(Employee.id == employee_id)
        ).one_or_none()
        if not employee:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found.",
            )
        return employee
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee with the provided ID does not exist.",
        )


def get_employee_by_credentials(
    db: DatabaseSession, id: int, password: str
) -> Employee:
    try:
        employee = get_employee_by_id(db, id)

        if not employee or not verify_password(password, employee.password):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invalid credentials",
            )
        return employee
    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee with the provided ID does not exist.",
        )


def update_employee(
    db: DatabaseSession,
    employee_id: int,
    update_request: CreateEmployee,
) -> Employee:
    try:
        employee = get_employee_by_id(db, employee_id)

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
                detail="Employee with the provided phone already exists.",
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {str(e)}",
            )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error retrieving employee: {str(e)}",
        )


def delete_employee(db: DatabaseSession, employee_id: int) -> None:
    pass
