from fastapi import HTTPException
import fitz
from src.cv_matching import schema
from src.database.core import DatabaseSession
from src.modules.opportunity.schemas.job_opportunity_schemas import (
    JobOpportunityResponse,
)
from src.modules.opportunity.services import opportunity_service
from src.modules.postulation.models.postulation_models import Postulation
from typing import List
import unicodedata
import string
import spacy
import base64
from sqlalchemy import func


def get_all_postulations(
    db: DatabaseSession, job_opportunity_id: int
) -> List[schema.PostulationResponse]:
    postulations = (
        db.query(Postulation)
        .filter(Postulation.job_opportunity_id == job_opportunity_id)
        .all()
    )

    if not postulations:
        raise HTTPException(status_code=404, detail="Postulation not found")

    formatted_postulations = []
    for postulation in postulations:
        postulation_dict = postulation.dict()
        try:
            # Decodifica base64 a bytes, luego a utf-8
            postulation_dict["cv_file"] = base64.b64decode(postulation.cv_file).decode(
                "utf-8"
            )
        except Exception:
            postulation_dict["cv_file"] = ""
        formatted_postulations.append(postulation_dict)

    return formatted_postulations


def get_all_abilities(
    db: DatabaseSession, job_opportunity_id: int
) -> JobOpportunityResponse:
    return opportunity_service.get_opportunity_with_abilities(db, job_opportunity_id)


def extract_text_from_pdf(base64_pdf: str):
    try:
        pdf_bytes = base64.b64decode(base64_pdf)
        doc = fitz.open("pdf", pdf_bytes)
        texto = ""
        for pagina in doc:
            texto += pagina.get_text()
        return texto
    except Exception as e:
        print(f"Error al procesar el PDF: {e}")
        return ""


def evaluate_candidates(
    db: DatabaseSession, job_opportunity_id: int
) -> List[schema.MatcherResponse]:
    postulations = (
        db.query(Postulation)
        .filter(Postulation.job_opportunity_id == job_opportunity_id)
        .all()
    )
    abilities = get_all_abilities(db, job_opportunity_id)
    model = load_spanish_model()

    desired_abilities = extract_desirable_abilities(abilities)
    required_abilities = extract_required_abilities(abilities)

    normalized_required_words = normalize_words(required_abilities)
    normalized_desired_words = normalize_words(desired_abilities)

    response = []

    for postulation in postulations:
        normalized_text = normalize(extract_text_from_pdf(postulation.cv_file))
        required_words_match = find_required_words(
            normalized_text, normalized_required_words, model
        )
        desired_words_match = find_desired_words(
            normalized_text, normalized_desired_words, model
        )

        ability_match = (
            required_words_match["WORDS_FOUND"] + desired_words_match["WORDS_FOUND"]
        )
        suitable = required_words_match["SUITABLE"] and desired_words_match["SUITABLE"]

        matcher = schema.MatcherResponse(
            postulation_id=postulation.id,
            name=postulation.name,
            surname=postulation.surname,
            suitable=suitable,
            ability_match=ability_match,
        )
        response.append(matcher)

        postulation.evaluated_at = func.now()
        postulation.suitable = suitable
        postulation.ability_match = {
            "required_words": required_words_match["WORDS_FOUND"],
            "desired_words": desired_words_match["WORDS_FOUND"],
        }
        postulation.status = "ACEPTADA" if suitable else "NO_ACEPTADA"

    db.commit()

    return response


def extract_desirable_abilities(abilities):
    desired_abilities = []
    for ability in abilities.desirable_abilities:
        desired_abilities.append(ability.name)
    return desired_abilities


def extract_required_abilities(abilities):
    required_abilities = []
    for ability in abilities.required_abilities:
        required_abilities.append(ability.name)
    return required_abilities


def normalize(text: str) -> str:
    """
    Convierte el texto a minúsculas, elimina acentos, signos de puntuación y caracteres especiales.
    """
    text = text.lower()
    text = unicodedata.normalize("NFD", text)
    text = "".join([c for c in text if unicodedata.category(c) != "Mn"])
    translator = str.maketrans("", "", string.punctuation)
    text = text.translate(translator)
    return text


def normalize_words(words: list) -> list[str]:
    normalized_words = [normalize(word) for word in words]
    return normalized_words


def find_required_words(text: str, words: list, model, threshold: float = 0.79) -> dict:
    """
    Verifica si todas las palabras de 'words' se encuentran en 'text'.
    Primero se busca una coincidencia literal y, si no se encuentra,
    se recurre a una coincidencia semántica usando spaCy.

    Parámetros:
        texto: el texto donde buscar.
        lista_palabras: lista de palabras a buscar.
        modelo: modelo spaCy (por ejemplo, es_core_news_lg o en_core_web_lg).
        umbral: valor mínimo de similitud para considerar una coincidencia semántica.

    Retorna:
        Un diccionario con las palabras encontradas, la palabra no encontrada (si existe) y un boolean.
        True si todas las palabras se encontraron (literal o semánticamente),
        False en caso contrario.
    """
    doc = model(text)
    tokens_text = [token.text for token in doc]
    result = {"WORDS_FOUND": [], "WORDS_NOT_FOUND": [], "SUITABLE": False}

    for word in words:
        if word in tokens_text:
            result["WORDS_FOUND"].append(word)
            continue
        else:
            word_doc = model(word)
            if len(word_doc) == 0 or not word_doc[0].has_vector:
                return False

            similarities = [
                token.similarity(word_doc[0]) for token in doc if token.has_vector
            ]
            if similarities and max(similarities) >= threshold:
                result["WORDS_FOUND"].append(word)
                continue
            else:
                result["WORDS_NOT_FOUND"].append(word)
                result["SUITABLE"] = False
                return result

    result["SUITABLE"] = True
    return result


def find_desired_words(
    text: str,
    words: list,
    model,
    threshold: float = 0.79,
    minimal_porcentage: float = 0.50,
) -> dict:
    """
    Verifica cuántas palabras de 'words' aparecen en 'text'.
    Retorna un diccionario con las palabras y un booleano.
    """
    doc = model(text)
    tokens_texto = [t.text for t in doc]
    result = {"WORDS_FOUND": [], "WORDS_NOT_FOUND": [], "SUITABLE": False}

    for word in words:
        if word in tokens_texto:
            result["WORDS_FOUND"].append(word)
            continue

        word_doc = model(word)
        if not word_doc or not word_doc[0].has_vector:
            continue

        max_sim = max(
            (t.similarity(word_doc[0]) for t in doc if t.has_vector), default=0.0
        )
        if max_sim >= threshold:
            result["WORDS_FOUND"].append(word)

    for word in words:
        if word not in result["WORDS_FOUND"]:
            result["WORDS_NOT_FOUND"].append(word)

    result["SUITABLE"] = (len(result["WORDS_FOUND"]) / len(words)) > minimal_porcentage
    return result


def load_spanish_model():
    return spacy.load("es_core_news_lg")


def load_english_model():
    return spacy.load("en_core_web_lg")
