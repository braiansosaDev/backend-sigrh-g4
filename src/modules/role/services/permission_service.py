from sqlmodel import select
from fastapi import HTTPException, status
from src.modules.role.models.role_models import Permission
from src.modules.role.schemas.permission_schemas import PermissionPublic
from src.database.core import DatabaseSession
from typing import Sequence


def get_all_permissions(db: DatabaseSession) -> Sequence[Permission]:
    return db.exec(select(Permission)).all()


def get_permission_by_id(db: DatabaseSession, permission_id: str) -> Permission | None:
    return db.exec(select(Permission).where(Permission.id == permission_id)).one_or_none()


def get_permission(db: DatabaseSession, permission_id: str) -> Permission:
    result = get_permission_by_id(db, permission_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El permiso con ID {permission_id} no existe.")
    return result


def validate_permission_list(db: DatabaseSession, permissions: list[PermissionPublic]) -> list[Permission]:
    """
    Valida que todos los permisos de la lista existan en la base de datos.
    """

    permission_list: list[Permission] = []

    for permission in permissions:
            db_permission = db.exec(
                select(Permission)
                .where(Permission.id == permission.id)
                .where(Permission.name == permission.name)
                .where(Permission.description == permission.description)
            ).one_or_none()
            if db_permission is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El siguiente permiso no existe: {permission.model_dump_json()}"
                )
            else:
                permission_list.append(db_permission)

    return permission_list
