from io import BytesIO
from spacy.language import Language
from spacy.tokens import Doc
from spacy.tokens.span import Span
from spacy.matcher import PhraseMatcher
from sqlmodel import select
from src.database.core import DatabaseSession
from src.modules.opportunity.models.job_opportunity_models import JobOpportunityModel
from src.modules.opportunity.schemas.job_opportunity_schemas import (
    JobOpportunityResponse,
)
from src.modules.opportunity.services import opportunity_service
from src.modules.postulation.models.postulation_models import Postulation
from src.modules.cv_matching import matcher_schema
from fastapi import status, HTTPException
from typing import List, Any
import pymupdf
import unicodedata
import string
import spacy
import base64
import logging
import re
import itertools
from datetime import datetime
from pypdf import PdfReader

logger = logging.getLogger("uvicorn.error")


def get_all_abilities(
    db: DatabaseSession, job_opportunity_id: int
) -> JobOpportunityResponse:
    return opportunity_service.get_opportunity_with_abilities(db, job_opportunity_id)


def extract_text_from_pdf(base64_pdf: str) -> str:
    texto: str = ""
    pdf_bytes = base64.b64decode(base64_pdf)

    try:
        logger.info("Extracting text with PyMuPDF...")
        with pymupdf.open("pdf", pdf_bytes) as doc_pymupdf:
            for pagina in doc_pymupdf:
                # Se debe ignorar porque pymupdf no soporta
                # adecuadamente los type hints:
                # https://github.com/pymupdf/PyMuPDF/issues/2883
                texto += str(pagina.get_text())  # type: ignore
    except Exception as e:
        logger.error("Unexpected exception occurred while extracting text with PyMuPDF")
        logger.error(e)

    try:
        logger.info("Extracting text with pypdf...")
        if texto.strip():
            texto += " "
        with PdfReader(BytesIO(pdf_bytes)) as doc_pypdf:
            for pagina in doc_pypdf.pages:
                texto += pagina.extract_text(extraction_mode="plain")
    except Exception as e:
        logger.error("Unexpected error occurred while extracting text with pypdf")
        logger.error(e)

    if not texto.strip():
        raise ValueError("Extracted text is empty!")
    logger.info(f"Extracted text:\n{texto}")
    return texto


def evaluate_candidates(
    db: DatabaseSession, job_opportunity_id: int
) -> List[matcher_schema.MatcherResponse]:
    job_opportunity = db.exec(
        select(JobOpportunityModel).where(JobOpportunityModel.id == job_opportunity_id)
    ).one()
    if not job_opportunity:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No existe la oferta laboral {job_opportunity_id}",
        )
    postulations = db.exec(
        select(Postulation).where(Postulation.job_opportunity_id == job_opportunity_id)
    ).all()
    if not postulations:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No hay postulaciones para la oferta laboral {job_opportunity_id}",
        )
    abilities = get_all_abilities(db, job_opportunity_id)
    model = load_spanish_model()

    desired_abilities = extract_desirable_abilities(abilities)
    required_abilities = extract_required_abilities(abilities)

    normalized_required_words = normalize_words(required_abilities)
    normalized_desired_words = normalize_words(desired_abilities)

    response: list[matcher_schema.MatcherResponse] = []

    for postulation in postulations:
        normalized_text = normalize(
            extract_text_from_pdf(postulation.cv_file.replace("\n", "").strip())
        )
        logger.info(f"Normalized PDF text:\n{normalized_text}")
        required_words_match = match_abilities(
            normalized_text,
            normalized_required_words,
            model,
            similarity_threshold=0.79,
            minimum_percentage=job_opportunity.required_skill_percentage,
        )
        desired_words_match = match_abilities(
            normalized_text,
            normalized_desired_words,
            model,
            similarity_threshold=0.79,
            minimum_percentage=job_opportunity.desirable_skill_percentage,
        )
        suitable = required_words_match["SUITABLE"] and desired_words_match["SUITABLE"]

        matcher = schema.MatcherResponse(
            postulation_id=postulation.id,
            name=postulation.name,
            surname=postulation.surname,
            suitable=suitable,
            required_words_found=required_words_match["WORDS_FOUND"],
            desired_words_found=desired_words_match["WORDS_FOUND"],
            required_words_not_found=required_words_match["WORDS_NOT_FOUND"],
            desired_words_not_found=desired_words_match["WORDS_NOT_FOUND"],
        )
        response.append(matcher)

        postulation.evaluated_at = datetime.now()
        postulation.suitable = suitable
        postulation.ability_match = {
            "required_words_found": required_words_match["WORDS_FOUND"],
            "desired_words_found": desired_words_match["WORDS_FOUND"],
            "required_words_not_found": required_words_match["WORDS_NOT_FOUND"],
            "desired_words_not_found": desired_words_match["WORDS_NOT_FOUND"],
        }

    db.commit()

    return response


def extract_desirable_abilities(abilities: JobOpportunityResponse):
    desired_abilities: list[str] = []
    for ability in abilities.desirable_abilities:
        desired_abilities.append(ability.name)
    return desired_abilities


def extract_required_abilities(abilities: JobOpportunityResponse):
    required_abilities: list[str] = []
    for ability in abilities.required_abilities:
        required_abilities.append(ability.name)
    return required_abilities


def normalize(text: str) -> str:
    """
    Convierte el texto a minúsculas, elimina acentos, signos de puntuación y caracteres especiales.
    """
    text = text.lower()
    text = text.replace("\n", " ")
    text = re.sub(r' +', ' ', text)
    text = unicodedata.normalize("NFD", text)
    text = "".join([c for c in text if unicodedata.category(c) in ["Ll", "Nd", "Zs", "Cc"]])
    translator = str.maketrans("", "", string.punctuation)
    text = text.translate(translator)
    return text


def normalize_words(words: list[str]) -> list[str]:
    normalized_words = [normalize(word) for word in words]
    return normalized_words


def match_phrase(tokens: Doc, ability: str, model: Language) -> bool:
    matcher = PhraseMatcher(model.vocab, attr="LOWER")
    matcher.add("TerminologyList", [model.make_doc(ability)])

    matches = matcher(tokens)
    matches_list: list[Span] = []
    if not matches:
        logger.info(f"Did not find {ability} with PhraseMatcher")
        return False

    for match_id, start, end in matches:
        span = tokens[start:end]
        matches_list.append(span)
        logger.info(f"Matched phrase: {span} (start: {start}, end: {end})")

    if len(matches_list) > 0:
        logger.info(f"Ability {ability} found with PhraseMatcher {len(matches_list)} times")
        return True
    else:
        return False


def match_abilities(text: str, abilities: list[str], model: Language, *, similarity_threshold: float, minimum_percentage: float):
    """
    Verifica si las habilidades se encuentran en `text`, usando el umbral de similaridad especificado.
    Devuelve las listas de palabras encontradas y no encontradas y el valor booleano Suitable en base
    al mínimo porcentaje requerido del total de habilidades.
    """

    if minimum_percentage < 0:
        raise ValueError("minimum_percentage must be a positive value or zero")

    logger.info(f"Finding required abilities {abilities} with threshold {similarity_threshold} and minimum percentage {minimum_percentage}")

    doc: Doc = model(text)
    tokens_text = [token.text for token in doc if token.text.strip()]
    doc = model(" ".join(tokens_text))
    logger.info(f"Tokens: {tokens_text}")



    result: dict[str, Any] = {
        "WORDS_FOUND": [],
        "WORDS_NOT_FOUND": [],
        "SUITABLE": False
    }

    for ability in abilities:
        logger.info(f"Matching ability {ability}")

        if ability in tokens_text:
            result["WORDS_FOUND"].append(ability)
            logger.info(f"Found ability {ability} in tokens")
        elif match_phrase(doc, ability, model):
            result["WORDS_FOUND"].append(ability)
        else:
            custom_lemmas = {
            "lic": "licenciatura",
            "tec": "tecnicatura",
            "ing": "ingenieria",
            "definicion": "definir",
            "capacitacion": "capacitar",
            "definiciones": "definir",
            "organizacion": "organizar",
            "organizaciones": "organizar",
            "resolucion": "resolver",
            "resoluciones": "resolver",
            "ejecucion": "ejecutar",
            "ejecuciones": "ejecutar",
            "educacion": "educar",
            "educaciones": "educar",
            "analisis": "analizar",
            "construccion": "construir",
            "construcciones": "construir",
            "produccion": "producir",
            "producciones": "producir",
            "evaluacion": "evaluar",
            "evaluaciones": "evaluar",
            "informacion": "informar",
            "revision": "revisar",
            "revisiones": "revisar",
            "desarrollo": "desarrollar",
            "desarrollos": "desarrollar",
            "programacion": "programar",
            "programaciones": "programar",
            "implementacion": "implementar",
            "implementaciones": "implementar",
            "diseno": "disenar",
            "disenos": "disenar",
            "configuracion": "configurar",
            "configuraciones": "configurar",
            "integracion": "integrar",
            "integraciones": "integrar",
            "mantenimiento": "mantener",
            "automatizacion": "automatizar",
            "automatizaciones": "automatizar",
            "optimizacion": "optimizar",
            "optimizaciones": "optimizar",
            "pruebas": "probar",
            "testing": "probar",
            "despliegue": "desplegar",
            "despliegues": "desplegar",
            "soporte": "soportar",
            "migracion": "migrar",
            "migraciones": "migrar",
            "documentacion": "documentar",
            "depuracion": "depurar",
            "refactorizacion": "refactorizar",
            "innovacion": "innovar",
            "actualizacion": "actualizar",
            "prueba": "probar",
            "integracioncontinua": "integrar",
            "desplieguecontinuo": "desplegar",
            "postgres": "sql",
            "postgresql": "sql",
            "mariadb": "sql",
            "mysql": "sql",
            "adm": "administrar",
            "administracion": "administrar",
            "administraciones": "administrar",
            "comunicacion": "comunicar",
            "comunicaciones": "comunicar",
            "liderazgo": "liderar",
            "gestion": "gestionar",
            "gestiones": "gestionar",
            "estrategia": "estrategizar",
            "estrategias": "estrategizar",
            "planificacion": "planificar",
            "planificaciones": "planificar",
            "innovaciones": "innovar",
            "experiencia": "experimentar",
            "coordinacion": "coordinar",
            "coordinaciones": "coordinar",
            "proyecto": "proyectar",
            "proyectos": "proyectar",
            "code": "codigo"
            }
            doc_norm: Doc = doc.copy()
            doc_norm_text = [custom_lemmas.get(token.lemma_, token.lemma_) for token in doc_norm if token.text.strip() and token.lemma_.strip() and not token.is_stop and token.pos_ != "ADP"]
            doc_norm = model(" ".join(doc_norm_text))
            logger.info(f"Norm tokens: {doc_norm_text}")

            ability_doc: Doc = model(ability)
            ability_doc_text = [custom_lemmas.get(token.lemma_, token.lemma_) for token in ability_doc if token.text.strip() and token.lemma_.strip() and not token.is_stop and token.pos_ != "ADP"]
            ability_doc = model(" ".join(ability_doc_text))

            if not ability_doc or len(ability_doc) == 0 or not all([token.has_vector for token in ability_doc]):
                result["WORDS_NOT_FOUND"].append(ability)
                logger.info(f"Skipping ability {ability} because it's empty or doesn't have a vector")
                continue

            token_groups: list[Span] = create_token_groups(doc_norm, len(ability_doc))
            similarities: dict[Span, float] = {}
            for token in token_groups:
                if not token.text.strip():
                    logger.info(f"Tried to evaluate similarity of empty token {token}")
                    continue
                elif not token.has_vector:
                    logger.info(f"Tried to evaluate similarity of token without vector: {token}")
                    continue
                sum = 0
                for token_i, ability_doc_i in zip(token, ability_doc):
                    sum += token_i.similarity(ability_doc_i)
                similarities[token] = sum / len(token)
            logger.info(f"Similarities: {similarities}")

            max_item = max(similarities.items(), key=lambda item: item[1])
            max_key = max_item[0]
            max_value = max_item[1]

            if similarities and max_value >= similarity_threshold:
                result["WORDS_FOUND"].append(ability)
                logger.info(f"Matched ability \"{ability}\" ({ability_doc_text}) with max similarity {max_value} to \"{max_key}\"")
            else:
                result["WORDS_NOT_FOUND"].append(ability)
                logger.info(f"Didn't match ability \"{ability}\" ({ability_doc_text}) with max similarity {max_value} to \"{max_key}\"")

    processed_abilities = result["WORDS_FOUND"] + result["WORDS_NOT_FOUND"]
    for ability in abilities:
        if ability not in processed_abilities:
            result["WORDS_NOT_FOUND"].append(ability)

    result["SUITABLE"] = (
        len(result["WORDS_FOUND"]) / len(abilities)
    ) >= minimum_percentage / 100
    return result


def create_token_groups(doc: Doc, word_amount: int) -> list[Span]:
    output_spans: list[Span] = []

    for i in range(len(doc) - word_amount + 1):
        token_group = doc[i : i + word_amount]
        output_spans.append(token_group)

        tokens_text = [token.text for token in token_group]

        if word_amount >= 10:
            logger.info(f"Skipping token group \"{tokens_text}\" permutations because word amount is too large ({word_amount})")
        elif word_amount > 1:
            perms = set(itertools.permutations(tokens_text))
            for perm in perms:
                if list(perm) == tokens_text:
                    continue
                new_doc = Doc(doc.vocab, words=list(perm))
                new_span = new_doc[0:len(new_doc)]
                output_spans.append(new_span)

    logger.info(
           f"Total token groups (including permutations): {len(output_spans)}. "
           f"Groups: {[span.text for span in output_spans]}"
       )
    return output_spans


def load_spanish_model():
    return spacy.load("es_core_news_lg")


def load_english_model():
    return spacy.load("en_core_web_lg")
