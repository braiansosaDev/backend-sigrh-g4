import unicodedata
import string
import spacy


def normalize(text: str) -> str:
    """
    Convierte el texto a minúsculas, elimina acentos, signos de puntuación y caracteres especiales.
    """
    # Convertir a minúsculas
    text = text.lower()
    # Eliminar tildes: descomponer y filtrar caracteres
    text = unicodedata.normalize("NFD", text)
    text = "".join([c for c in text if unicodedata.category(c) != "Mn"])
    # Eliminar signos de puntuación y caracteres especiales
    translator = str.maketrans("", "", string.punctuation)
    text = text.translate(translator)
    # Se pueden eliminar espacios extras o nuevos caracteres si se desea
    return text


def find_words(text: str, words: list, model, threshold: float = 0.6) -> bool:
    """
    Verifica si todas las palabras de 'lista_palabras' se encuentran en 'texto'.
    Primero se busca una coincidencia literal y, si no se encuentra,
    se recurre a una coincidencia semántica usando spaCy.

    Parámetros:
        texto: el texto donde buscar.
        lista_palabras: lista de palabras a buscar.
        modelo: modelo spaCy (por ejemplo, es_core_news_lg o en_core_web_lg).
        umbral: valor mínimo de similitud para considerar una coincidencia semántica.

    Retorna:
        True si todas las palabras se encontraron (literal o semánticamente),
        False en caso contrario.
    """
    # Normalizar texto y palabras
    normalized_text = normalize(text)
    normalized_words = [normalize(word) for word in words]

    # Procesamos el texto con el modelo de spaCy
    doc = model(normalized_text)

    # Convertir el documento en una lista de tokens (o palabras) para comparar literalmente.
    tokens_text = [token.text for token in doc]

    # Para cada palabra de la lista, se verifica la coincidencia
    for word in normalized_words:
        # Coincidencia literal
        if word in tokens_text:
            continue  # Se encontró la palabra literalmente
        else:
            # Coincidencia semántica:
            # Procesamos la palabra con el modelo para obtener su vector
            word_doc = model(word)
            # Se asume que la palabra consiste en un solo token
            if len(word_doc) == 0 or not word_doc[0].has_vector:
                # Si la palabra no tiene representación vectorial,
                # no podemos comparar semánticamente
                return False

            # Comparar la similitud de la palabra con cada token del texto
            similarities = [
                token.similarity(word_doc[0]) for token in doc if token.has_vector
            ]
            # Se verifica si alguna similitud supera el umbral
            if similarities and max(similarities) >= threshold:
                continue
            else:
                return False  # No se encontró coincidencia (literal ni semántica)
    return True


def load_spanish_model():
    return spacy.load("es_core_news_lg")


def load_english_model():
    return spacy.load("en_core_web_lg")
