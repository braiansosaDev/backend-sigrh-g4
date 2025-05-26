from fastapi import APIRouter
from src.modules.role.schemas.permission_schemas import PermissionPublic
from src.modules.role.services import permission_service
from src.database.core import DatabaseSession


permission_router = APIRouter(prefix="/permissions", tags=["Permissions"])


@permission_router.get("/", response_model=list[PermissionPublic])
async def get_all_permissions(db: DatabaseSession):
    return permission_service.get_all_permissions(db)


@permission_router.get("/{permission_id}", response_model=PermissionPublic)
async def get_permission(db: DatabaseSession, permission_id: str):
    return permission_service.get_permission(db, permission_id)
