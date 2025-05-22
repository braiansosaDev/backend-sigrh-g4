from fastapi import HTTPException, status
from sqlmodel import select
from sqlalchemy.exc import IntegrityError
from src.database.core import DatabaseSession
from src.modules.role.models.role_models import Role, Permission
from src.modules.role.schemas.role_schemas import RoleCreate, RoleUpdate
from src.modules.role.services import permission_service
from typing import Sequence
import logging

logger = logging.getLogger("uvicorn.error")

def get_role_by_id(db: DatabaseSession, role_id: int) -> Role | None:
    return db.exec(
        select(Role).where(Role.id == role_id)
    ).one_or_none()


def get_role(db: DatabaseSession, role_id: int) -> Role:
    result = get_role_by_id(db, role_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"El role con id {role_id} no existe.")
    return result


def get_all_roles(db: DatabaseSession) -> Sequence[Role]:
    return db.exec(select(Role)).all()


def create_role(db: DatabaseSession, request: RoleCreate) -> Role:
    permissions: list[Permission] = permission_service.validate_permission_list(db, request.permissions)

    try:
        db_role = Role(**request.dict(exclude={"permissions"}))
        for permission in permissions:
            db_role.permissions.append(permission)
        db.add(db_role)
        db.commit()
        return db_role
    except IntegrityError as e:
        db.rollback()
        logger.error(f"An unexpected error occurred while creating role with request {request.model_dump_json()}")
        logger.error(e)
        raise


def delete_role(db: DatabaseSession, role_id: int) -> None:
    db_role = get_role(db, role_id)
    try:
        db.delete(db_role)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        logger.error(f"An unexpected error occurred while deleting role with ID {db_role.id}")
        logger.error(e)
        raise


def update_role(db: DatabaseSession, role_id: int, request: RoleUpdate) -> Role:
    db_role = get_role(db, role_id)
    if hasattr(request, "permissions"):
        db_role.permissions.clear()
        permissions: list = request.permissions # type: ignore
        permissions = permission_service.validate_permission_list(db, permissions)
        for permission in permissions:
            db_role.permissions.append(permission)

    for key, value in request.model_dump(exclude_unset=True, exclude={"permissions"}).items():
        if hasattr(db_role, key):
            setattr(db_role, key, value)

    try:
        db.add(db_role)
        db.commit()
        return db_role
    except IntegrityError as e:
        db.rollback()
        logger.error(f"An unexpected error occurred while updating role with ID {role_id} and data {request.model_dump_json()}")
        logger.error(e)
        raise
