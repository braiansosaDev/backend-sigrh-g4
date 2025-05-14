import unicodedata
import string
import spacy


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
