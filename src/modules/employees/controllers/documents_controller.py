from typing import List
from fastapi import APIRouter
from src.modules.employees.services import documents_service
from src.database.core import DatabaseSession
from src.modules.employees.schemas.documents_models import DocumentResponse, DocumentRequest

documents_router = APIRouter(prefix="/documents", tags=["Documents"])


@documents_router.get(
    "/{employee_id}", status_code=200, response_model=List[DocumentResponse]
)
async def get_documents_of_employee(
    db: DatabaseSession,
    employee_id: int,
):
    return documents_service.get_documents_of_employee(
        db=db,
        employee_id=employee_id,
    )


@documents_router.post(
    "/{employee_id}", status_code=201, response_model=DocumentResponse
)
async def create_document_of_employee(
    db: DatabaseSession,
    employee_id: int,
    document: DocumentRequest,
):
    return documents_service.create_document_of_employee(
        db=db,
        employee_id=employee_id,
        document=document,
    )


@documents_router.patch(
    "/{employee_id}/{document_id}", status_code=200, response_model=DocumentResponse
)
async def update_document_of_employee(
    db: DatabaseSession,
    employee_id: int,
    document_id: int,
    document: DocumentRequest,
):
    return documents_service.update_document_of_employee(
        db=db,
        employee_id=employee_id,
        document_id=document_id,
        document=document,
    )


@documents_router.delete("/{employee_id}/{document_id}", status_code=204)
async def delete_documents_of_employee(
    db: DatabaseSession,
    employee_id: int,
    document_id: int,
):
    return documents_service.delete_documents_of_employee(
        db=db,
        employee_id=employee_id,
        document_id=document_id,
    )
