from fastapi import APIRouter, status
from src.database.core import DatabaseSession
from src.modules.role.schemas.role_schemas import RolePublic, RoleCreate, RoleUpdate
from src.modules.role.services import role_service


role_router = APIRouter(prefix="/roles", tags=["Roles"])


@role_router.get("/", response_model=list[RolePublic])
async def get_all_roles(db: DatabaseSession):
    return role_service.get_all_roles(db)


@role_router.get("/{role_id}", response_model=RolePublic)
async def get_role(db: DatabaseSession, role_id: int):
    return role_service.get_role(db, role_id)


@role_router.put("/", status_code=status.HTTP_201_CREATED, response_model=RolePublic)
async def create_role(db: DatabaseSession, body: RoleCreate):
    return role_service.create_role(db, body)


@role_router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_role(db: DatabaseSession, role_id: int) -> None:
    return role_service.delete_role(db, role_id)


@role_router.patch("/{role_id}", response_model=RolePublic)
async def update_role(db: DatabaseSession, role_id: int, body: RoleUpdate):
    return role_service.update_role(db, role_id, body)
