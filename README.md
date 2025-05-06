# Sistema de Gestión de RRHH con IA

Plataforma web pensada para automatizar y optimizar procesos clave de RRHH como reclutamiento, evaluación y adinistración del personal.

## Requisitos

Este proyecto requiere Python 3.10 o superior. Las dependencias necesarias se pueden instalar utilizando el archivo `requirements.txt`.

## Instalación

1. Clona el repositorio o descarga los archivos en tu máquina local.

   ```bash
   git clone <url-del-repositorio>
   cd <nombre-del-repositorio>

2. Instala las dependencias

   ```bash
   pip install -r requirements.txt

3. Instalar postgreSQL y configurar usuario/contraseña y crear BBDD sigrh. Opcionalmente se puede instalar DBEAVER (recomendado) sino desde la SQL Shell se puede trabajar.

4. Agregar .env utilizando de copia .env.example, modificar segun datos de inicio de sesión y bbdd de maquina local.

5. Levantar el servidor por defecto en el puerto 8000

- ``uvicorn src.main:app --reload``

6. La documentación de los endpoints se puede encontrar en: 

- http://127.0.0.1:8000/redoc con ReDoc
- http://127.0.0.1:8000/docs#/ con Swagger

7. Para ejecutar la funcionalidad de análisis de CV realizar los siguientes pasos:

- Instalar spacy con ``pip install spacy``
- Instalar los modelos nlp de spacy:
   - python -m spacy download es_core_news_lg
   - python -m spacy download en_core_web_lg
- Ya se puede ejecutar el archivo src/cv_matching/main ingresando la descripcion de un currículum y la lista de palabras clave a buscar.