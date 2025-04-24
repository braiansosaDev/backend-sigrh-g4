import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.utils import resample

file_path = "./data/candidatos.xlsx"
df = pd.read_excel(file_path)

#No agregamos expectativa salarial hasta corregir imperfecciones
df = df.drop(columns=['id_candidato', 'nombre', 'expectativa_salarial'])

nivel_educativo_mapping = {'secundario': 0, 'terciario': 1, 'universitario': 2}
df['nivel_educativo'] = df['nivel_educativo'].map(nivel_educativo_mapping)

#separamos las habilidades
habilidades = df['habilidades'].str.get_dummies(sep=', ')
idiomas = df['idiomas'].str.get_dummies(sep=', ')
df = pd.concat([df.drop(columns=['habilidades', 'idiomas']), habilidades, idiomas], axis=1)

# separamos los aptos y no aptos
df_aptos = df[df['es_apto'] == 1]
df_no_aptos = df[df['es_apto'] == 0]

# Hacer oversampling de los "Aptos" si hay menos registros
df_aptos_upsampled = resample(df_aptos, 
                              replace=True,
                              n_samples=len(df_no_aptos), 
                              random_state=42)
df_balanced = pd.concat([df_no_aptos, df_aptos_upsampled])

X = df_balanced.drop(columns=['es_apto'])  
y = df_balanced['es_apto']  # Etiqueta (0 = No Apto, 1 = Apto)

scaler = StandardScaler()
X = scaler.fit_transform(X)

# dividimos en conjuntos de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# entrenamiento de modelo
modelo = DecisionTreeClassifier(random_state=42)
modelo.fit(X_train, y_train)

# evaluacion de modelo
y_pred = modelo.predict(X_test)
precision = accuracy_score(y_test, y_pred)
reporte = classification_report(y_test, y_pred)

print(f'🔹 Precisión del modelo: {precision:.2f}')
print("🔹 Reporte de clasificación:\n", reporte)

#prediccion candidato X
nuevo_candidato_df = pd.DataFrame({
    'anios_de_experiencia': [5],
    'nivel_educativo': [nivel_educativo_mapping['universitario']], 
    **{col: [1 if col in ['Python', 'Java'] else 0] for col in habilidades.columns},  
    **{col: [1 if col in ['Inglés'] else 0] for col in idiomas.columns}  
})

# normalizar el nuevo candidato (sin la columna 'expectativa_salarial')
nuevo_candidato_df = scaler.transform(nuevo_candidato_df)

# Hacer la predicción
prediccion = modelo.predict(nuevo_candidato_df)
resultado = 'Apto 🟢' if prediccion[0] == 1 else 'No Apto 🔴'

print(f'🔹 Candidato con 5 años de experiencia, habilidades en Python y Java: {resultado}')

