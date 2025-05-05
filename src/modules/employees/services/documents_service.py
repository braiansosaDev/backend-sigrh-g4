from src.database.core import DatabaseSession
from src.modules.employees.schemas.documents_models import DocumentRequest
from src.modules.employees.models.documents import Document
from src.modules.employees.services import utils
from fastapi import HTTPException, status


def get_documents_of_employee(db: DatabaseSession, employee_id: int):
    employee = utils.get_employee_by_id(db, employee_id)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found."
        )
    return utils.get_documents_of_employee(db, employee_id)


def create_document_of_employee(
    db: DatabaseSession,
    employee_id: int,
    document: DocumentRequest,
) -> Document:
    employee = utils.get_employee_by_id(db, employee_id)
    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found."
        )
    doc = Document(
        employee_id=employee_id,
        name=document.name,
        extension=document.extension,
        creation_date=document.creation_date,
        file=document.file,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def update_document_of_employee(
    db: DatabaseSession,
    employee_id: int,
    document_id: int,
    document: DocumentRequest,
) -> Document:
    employee = utils.get_employee_by_id(db, employee_id)
    doc = utils.get_document(db, document_id, employee_id)

    if employee is None or doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee or document not found.",
        )
    for attr, value in document.model_dump(exclude_unset=True).items():
        if hasattr(doc, attr):
            setattr(doc, attr, value)

    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def delete_documents_of_employee(
    db: DatabaseSession,
    employee_id: int,
    document_id: int,
) -> None:
    employee = utils.get_employee_by_id(db, employee_id)
    doc = utils.get_document(db, document_id, employee_id)

    if employee is None or doc is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee or document not found.",
        )
    db.delete(doc)
    db.commit()
