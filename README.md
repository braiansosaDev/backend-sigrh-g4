# SIGRH: Sistema de Gestión de RRHH con IA

Plataforma web pensada para automatizar y optimizar procesos clave de RRHH como reclutamiento, evaluación y administración del personal.

## Requisitos

Este proyecto requiere 
- Python 3.10 o superior.
- PostgreSQL 16 o superior.
- Ollama instalado
- Docker [**recomendado**]

## Instalación en máquina local

1. Clona el repositorio o descarga los archivos en tu máquina local.

    ```bash
    git clone <url-del-repositorio>
    cd <nombre-del-repositorio>
    ```

2. Recomendado: Crear un entorno virtual para descargar las librerías

    ```bash
    python -m venv .venv
    ```

    1. **Importante**: Si vas a abrir la terminal, cmd, PowerShell, etc. por fuera del editor de código seguramente tendrás que activar el entorno virtual.

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

3. Instala las dependencias

    ```bash
    pip install -r requirements.txt
    ```

4. Instalar PostgreSQL, configurar usuario/contraseña y crear base de datos `sigrh`.

5. Crear `.env` en la raiz del proyecto utilizando de copia `.env.example`. Se deben modificar los siguientes campos:
    - SECRET_KEY
        - Una key secreta.
    - DATABASE_URL
        - La URL de la base de datos `sigrh` que fue creada en el paso anterior.
    - MAIL_USERNAME
    - MAIL_PASSWORD

6. Descargar el modelo `gemma:2b` utilizando Ollama
    - Para esto hay que tener instalado Ollama. Ver instalación según OS en [La web oficial de Ollama](https://ollama.com/)
    - Una vez instalado Ollama, iniciar el servicio.    
        - Abrir una terminal, PowerShell, CMD, etc. Y ejecutar el siguiente comando:
        ```bash
        ollama serve
        ```
        **Importante**: Asegurarse que el comando `ollama` está registrado en la variable de entorno PATH. Si esto no es asi y existe algún error al realizar el comando, probablemente no reiniciaste tu máquina luego de la instalación.
    - Descargar el modelo `gemma:2b`
        - Abrir otra terminal, PowerShell, CMD, etc. Y ejecutar el siguiente comando:
        ```
        ollama run gemma:2b
        ```

7. Levantar el servidor. Por defecto se levanta en el puerto 8000. Para dejar de correr el servidor realizar CTRL+C

    ```bash
    uvicorn src.main:app --reload
    ```

8. La documentación de los endpoints se puede encontrar en:

- http://127.0.0.1:8000/redoc con ReDoc
- http://127.0.0.1:8000/docs#/ con Swagger

---

# Levantar en Docker
1. Tener Docker y Docker Compose instalados
2. Agregar `.env` utilizando copia de `.env.example`, modificar con host de postgres `db`, usuario `postgres` y password a elección
3. Poner password elegida en archivo  `.postgres-password` (está ignorado en git)
4. Si se modificó el código o dependencias volver a construir imagen:
```bash
docker-compose build backend
```
4. Ejecutar con
```bash
docker-compose up -d backend db
```
Se accede de la misma forma que si corre en local.

5. Ver logs con
```bash
docker-compose logs backend
docker-compose logs db
```

6. Parar con
```bash
docker-compose down
```

7. Eliminar datos de database (opcional)
```bash
docker volume rm postgres-data
```
