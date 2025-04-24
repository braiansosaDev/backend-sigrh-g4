import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils import resample

# Cargar datos
file_path = "./data/candidatos.xlsx"
df = pd.read_excel(file_path)

# Eliminar columnas no relevantes para el modelo
df = df.drop(columns=['id_candidato', 'nombre'])

# mapeos y normalizaciones
nivel_educativo_mapping = {'secundario': 0, 'terciario': 1, 'universitario': 2}
df['nivel_educativo'] = df['nivel_educativo'].map(nivel_educativo_mapping)
df['habilidades'] = df['habilidades'].str.lower().str.strip().str.replace(r'\s*,\s*', ', ', regex=True)
df['idiomas'] = df['idiomas'].str.lower().str.strip().str.replace(r'\s*,\s*', ', ', regex=True)

habilidades = df['habilidades'].str.get_dummies(sep=', ')
idiomas = df['idiomas'].str.get_dummies(sep=', ')
df = pd.concat([df.drop(columns=['habilidades', 'idiomas']), habilidades, idiomas], axis=1)

# Separar y balancear clases
df_aptos = df[df['es_apto'] == 1]
df_no_aptos = df[df['es_apto'] == 0]
df_aptos_upsampled = resample(df_aptos, replace=True, n_samples=len(df_no_aptos), random_state=42)
df_balanced = pd.concat([df_no_aptos, df_aptos_upsampled])

# Features y etiqueta
X = df_balanced.drop(columns=['es_apto'])
y = df_balanced['es_apto']

# Guardar las columnas usadas por el modelo (clave para predicciones futuras)
columnas_modelo = X.columns.tolist()

# Normalización
scaler = StandardScaler()
X = scaler.fit_transform(X)

# División de datos
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Entrenamiento del modelo y evaluacion
modelo = DecisionTreeClassifier(random_state=42)
modelo.fit(X_train, y_train)
y_pred = modelo.predict(X_test)
precision = accuracy_score(y_test, y_pred)
reporte = classification_report(y_test, y_pred)


def es_apto(candidato: dict):
    # Crear DataFrame con una sola fila a partir del dict
    df_candidato = pd.DataFrame([{
        'anios_experiencia': candidato['anios_experiencia'],
        'nivel_educativo': nivel_educativo_mapping[candidato['nivel_educativo'].lower()],
        'expectativa_salarial': candidato['expectativa_salarial'],
        **{h.lower(): 1 if h.lower() in [hab.lower() for hab in candidato['habilidades']] else 0 for h in habilidades.columns},
        **{i.lower(): 1 if i.lower() in [idi.lower() for idi in candidato['idiomas']] else 0 for i in idiomas.columns}
    }])
    # Aseguramos que tenga las columnas en el mismo orden y estructura
    for col in columnas_modelo:
        if col not in df_candidato.columns:
            df_candidato[col] = 0
    df_candidato = df_candidato[columnas_modelo]
    # Normalizar y predecir
    df_candidato_scaled = scaler.transform(df_candidato)
    prediccion = modelo.predict(df_candidato_scaled)

    if prediccion[0] == 1:
        return True
    return False

nuevo = {
    'anios_experiencia': 2,
    'nivel_educativo': 'secundario',
    'expectativa_salarial': 4100000,
    'habilidades': ['Python', 'Java'],
    'idiomas': ['Inglés']
}

print("Resultado:", es_apto(nuevo))
