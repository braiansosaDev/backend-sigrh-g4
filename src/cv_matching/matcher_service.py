from fastapi import HTTPException
#import fitz
from pypdf import PdfReader
from io import BytesIO
from spacy.language import Language
from spacy.tokens import Doc
from spacy.tokens.span import Span
from spacy.matcher import PhraseMatcher
from src.cv_matching import schema
from src.database.core import DatabaseSession
from src.modules.opportunity.schemas.job_opportunity_schemas import (
    JobOpportunityResponse,
)
from src.modules.opportunity.services import opportunity_service
from src.modules.postulation.models.postulation_models import Postulation
from typing import List, Any
import unicodedata
import string
import spacy
import base64
import logging
import re
from sqlalchemy import func
from sqlmodel import select


logger = logging.getLogger("uvicorn.error")

def get_all_postulations(
    db: DatabaseSession, job_opportunity_id: int
) -> List[schema.PostulationResponse]:
    postulations = db.exec(select(Postulation).where(Postulation.job_opportunity_id == job_opportunity_id)).all()

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
        #doc = fitz.open("pdf", pdf_bytes)
        #texto = ""
        #for pagina in doc:
        #    texto += pagina.get_text()
        #return texto
        doc = PdfReader(BytesIO(pdf_bytes))
        texto: str = ""
        for pagina in doc.pages:
            texto += pagina.extract_text()
        return texto
    except Exception as e:
        print(f"Error al procesar el PDF: {e}")
        return ""


def evaluate_candidates(
    db: DatabaseSession, job_opportunity_id: int
) -> List[schema.MatcherResponse]:
    postulations = db.exec(select(Postulation).where(Postulation.job_opportunity_id == job_opportunity_id))
    abilities = get_all_abilities(db, job_opportunity_id)
    model = load_spanish_model()

    desired_abilities = extract_desirable_abilities(abilities)
    required_abilities = extract_required_abilities(abilities)

    normalized_required_words = normalize_words(required_abilities)
    normalized_desired_words = normalize_words(desired_abilities)

    response = []

    for postulation in postulations:
        normalized_text = normalize(
            extract_text_from_pdf(postulation.cv_file.replace("\n", "").strip())
        )
        logger.info(f"Normalized PDF text:\n{normalized_text}")
        required_words_match = match_abilities(
            normalized_text, normalized_required_words, model, similarity_threshold=0.79, minimum_percentage=1.0
        )
        desired_words_match = match_abilities(
            normalized_text, normalized_desired_words, model, similarity_threshold=0.79, minimum_percentage=0.50
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
    text = text.replace("\n", " ")
    text = re.sub(r' +', ' ', text)
    text = unicodedata.normalize("NFD", text)
    text = "".join([c for c in text if unicodedata.category(c) in ["Ll", "Nd", "Zs", "Cc"]])
    translator = str.maketrans("", "", string.punctuation)
    text = text.translate(translator)
    return text


def normalize_words(words: list) -> list[str]:
    normalized_words = [normalize(word) for word in words]
    return normalized_words


def match_phrase(tokens: Doc, ability: str, model: Language) -> bool:
    matcher = PhraseMatcher(model.vocab, attr="LOWER")
    matcher.add("TerminologyList", [model.make_doc(ability)])

    matches = matcher(tokens)
    matches_list = []
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

    if minimum_percentage <= 0:
        raise ValueError("minimum_percentage must be a positive value")

    logger.info(f"Finding required abilities {abilities} with threshold {similarity_threshold} and minimum percentage {minimum_percentage}")

    doc: Doc = model(text)
    tokens_text = [token.text for token in doc if token.text.strip()]
    doc = model(" ".join(tokens_text))
    logger.info(f"Tokens: {tokens_text}")

    doc_norm: Doc = doc.copy()
    doc_norm_text = [token.lemma_ for token in doc_norm if token.text.strip() and token.lemma_.strip() and not token.is_stop and token.pos_ != "ADP"]
    doc_norm = model(" ".join(doc_norm_text))
    logger.info(f"Norm tokens: {doc_norm_text}")

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
            ability_doc: Doc = model(ability)
            ability_doc_text = [token.lemma_ for token in ability_doc if token.text.strip() and token.lemma_.strip() and not token.is_stop and token.pos_ != "ADP"]
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

    result["SUITABLE"] = (len(result["WORDS_FOUND"]) / len(abilities)) >= minimum_percentage
    return result


def create_token_groups(doc: Doc, word_amount: int) -> list[Span]:
    token_groups: list[Span] = []
    for i in range(len(doc) - word_amount + 1):
        token_group = doc[i : i + word_amount]
        token_groups.append(token_group)
    logger.info(f"Token groups ({len(token_groups)}): {[token_group.text for token_group in token_groups]}")
    return token_groups


def load_spanish_model():
    return spacy.load("es_core_news_lg")


def load_english_model():
    return spacy.load("en_core_web_lg")
