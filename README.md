# SIGRH: Sistema de Gestión de RRHH con IA

Plataforma web pensada para automatizar y optimizar procesos clave de RRHH como reclutamiento, evaluación y administración del personal.

## Requisitos

Se recomienda utilizar Python 3.12, no utilizar Python 3.13 porque es incompatible con una de las dependencias.

## Instalación en máquina local

Se recomienda utilizar Python 3.12.10 o la última versión menor disponible. No utilizar Python 3.13 o superior porque es incompatible con una de las dependencias.

1. Clona el repositorio o descarga los archivos en tu máquina local.

    ```bash
    git clone <url-del-repositorio>
    cd <nombre-del-repositorio>
    ```

2. Recomendado: Crear un entorno virtual

    ```bash
    python -m venv .venv
    ```

    1. **Importante (desarrolladores)**: Si vas a abrir la terminal, cmd, PowerShell, etc. por fuera del editor de código seguramente tendrás que activar el entorno virtual.

        ### Windows (PowerShell):

        Habilitar scripts de internet firmados digitalmente:
        ```powershell
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
        ```
        Ejecutar cada vez que abras la terminal:
        ```powershell
        .venv\Scripts\Activate.ps1
        ```
        ---

        ### Linux/macOS:
        Ejecutar cada vez que abras la terminal:
        ```bash
        source .venv/bin/activate
        ```

3. Instalar las dependencias (incluyendo modelos de spacy)
    ```bash
    pip install -r requirements.txt
    ```

4. Instalar PostgreSQL, configurar usuario/contraseña y crear base de datos `sigrh` con el comando:
    ```sql
    CREATE DATABASE sigrh WITH ENCODING 'UTF8'
    ```
    Opcionalmente se puede instalar [DBeaver](https://dbeaver.io/download/) (recomendado) para crear y conectarse a la base de datos.

5. Instalar otros servicios
    - Instalar [Mailpit](https://mailpit.axllent.org/) si se desea simular un servicio de correo o bien configurar los datos de SMTP con un servidor real en el siguiente paso.
    - Instalar [ollama](https://ollama.com/download) y correr el modelo `gemma:2b` para que funcione el chatbot.

6. Agregar `.env` utilizando de copia `.env.example`. :
    - Crear key segura y ponerla en `SECRET_KEY` (opcional para seguridad).

    Los datos por defecto son para levantar el backend en Docker, si no se desea usar Docker hay que modificar las siguientes variables si corresponden a su situación:

    - Cambiar en los datos de PostgreSQL. Cambiar valor de `POSTGRES_USER` por el usuario, cambiar valor de `POSTGRES_PASSWORD` por la contraseña, cambiar valor de `POSTGRES_HOST` por el host (seguramente `localhost`) y `5432` por el puerto (si se cambió del default).
    - Cambiar los datos de SMTP a los valores correspondientes a su servidor. Se puede cambiar `MAIL_USERNAME` por el usuario, `MAIL_PASSWORD` por la contraseña, `MAIL_FROM` por la dirección de correo electrónico correspondiente al sistema, `MAIL_PORT` por el puerto de SMTP, `MAIL_SERVER` por el host del servidor SMTP y `MAIL_SSL_TLS` para configurar conexión cifrada.
    - Cambiar `OLLAMA_HOST` por el host de ollama correspondiente y `OLLAMA_PORT` por el puerto de ollama correspondiente.

7. **Obligatorio:** Ejecutar en la base de datos `sigrh` el archivo SQL `data_entry_system.sql` que está en la carpeta `database/data/` con DBeaver o de alguna otra forma, si no se hace el sistema no tendrá los datos por defecto para trabajar y **no funcionará**.


8. Levantar el servidor por defecto en el puerto 8000

    ```bash
    uvicorn src.main:app --reload
    ```

9. La documentación de los endpoints se puede encontrar en:

- http://127.0.0.1:8000/redoc con ReDoc
- http://127.0.0.1:8000/docs con Swagger (recomendado)

---

# Levantar en Docker
1. Tener Docker y Docker Compose instalados
2. Agregar `.env` utilizando copia de `.env.example`, modificar `SECRET_KEY` con una key segura (opcional para seguridad), `POSTGRES_HOST` con host de postgres `db`, `POSTGRES_USER` con usuario `postgres` y `POSTGRES_PASSWORD` con password a elección, `POSTGRES_PORT` con puerto de postgres si es diferente al default.

3. Si se modificó el código o dependencias volver a construir imagen:
    ```bash
    docker-compose build backend
    ```
4. Ejecutar con
    ```bash
    docker-compose up -d backend db ollama mailpit
    ```

    Se accede al backend en http://localhost:8000.

    Se accede a la interfaz web de Mailpit con http://localhost:8005.

5. **Obligatorio:** Ejecutar en la base de datos `sigrh` el archivo SQL `data_entry_system.sql` que está en la carpeta `database/data/` con DBeaver o de alguna otra forma, si no se hace el sistema no tendrá los datos por defecto para trabajar y **no funcionará**.


6. Ver logs con los siguientes comandos, agregar modificador `-f` antes del nombre del servicio si se desea seguir el log en tiempo real:
    ```bash
    docker-compose logs backend
    docker-compose logs db
    docker-compose logs ollama
    docker-compose logs mailpit
    ```

7. Parar con
    ```bash
    docker-compose down
    ```

8. Eliminar datos de contenedores (opcional, para resetear)
    ```bash
    docker volume rm backend-sigrh-g4_postgres-data backend-sigrh-g4_mailpit-data backend-sigrh-g4_ollama-data
    ```
