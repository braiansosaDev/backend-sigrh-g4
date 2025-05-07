import matcher

text = """
La inteligencia artificial está transformando la forma en que las empresas operan.
Gracias al aprendizaje automático, los sistemas pueden identificar patrones complejos
y tomar decisiones en tiempo real. Además, la automatización reduce los costos
y mejora la eficiencia en múltiples industrias.
"""

required_words = [
    "inteligencia",
    "artificial",
    "aprendizaje",
    "automatización",
    "decisiones",
]

desired_words = ["eficiencia", "industria", "algoritmo", "aprendizaje"]

normalized_required_words = matcher.normalize_words(required_words)
normalized_desired_words = matcher.normalize_words(desired_words)
normalized_text = matcher.normalize(text)
model = matcher.load_spanish_model()


required_words_match = matcher.find_required_words(
    normalized_text, normalized_required_words, model
)
desired_words_match = matcher.find_desired_words(
    normalized_text, normalized_desired_words, model
)

print(
    f"RESULTADO FINAL: {required_words_match['SUITABLE'] and desired_words_match['SUITABLE']}",
    f"\nPALABRAS REQUERIDAS NO ENCONTRADAS: {required_words_match['WORDS_NOT_FOUND']}",
    f"\nPALABRAS DESEADAS ENCONTRADAS: {desired_words_match['WORDS_FOUND']}",
    f"\nPALABRAS DESEADAS NO ENCONTRADAS: {desired_words_match['WORDS_NOT_FOUND']}",
)
