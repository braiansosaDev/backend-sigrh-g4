from typing import Sequence
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import select
from src.database.core import DatabaseSession
from src.modules.concept.models.models import Concept
from src.modules.concept.schemas.schemas import ConceptRequest
import logging


def get_concept_by_id(db: DatabaseSession, id: int) -> Concept:
    concept = db.exec(select(Concept).where(Concept.id == id)).first()
    if not concept:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Concept id was not found"
        )
    return concept


def get_concepts(db: DatabaseSession) -> Sequence[Concept]:
    return db.exec(select(Concept)).all()


def post_concept(db: DatabaseSession, request: ConceptRequest) -> Concept:
    try:
        db_concept = Concept(**request.model_dump())
        db.add(db_concept)
        db.commit()
        db.refresh(db_concept)
        return db_concept
    except IntegrityError as e:
        db.rollback()
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An unexpected error occurred",
        )


def patch_concept(
    db: DatabaseSession, concept_id: int, request: ConceptRequest
) -> Concept:
    try:
        db_concept = get_concept_by_id(db, concept_id)
        if not db_concept:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Concept not found"
            )
        for attr, value in request.model_dump(exclude_unset=True).items():
            if hasattr(db_concept, attr):
                setattr(db_concept, attr, value)

        db.add(db_concept)
        db.commit()
        return db_concept
    except IntegrityError as e:
        db.rollback()
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An unexpected error occurred",
        )


def delete_concept(db: DatabaseSession, concept_id: int):
    try:
        db_concept = get_concept_by_id(db, concept_id)
        if not db_concept:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Concept not found"
            )
        if db_concept.is_deletable is False:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Concept cannot be deleted",
            )
        db.delete(db_concept)
        db.commit()
    except IntegrityError as e:
        db.rollback()
        logging.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An unexpected error occurred",
        )
