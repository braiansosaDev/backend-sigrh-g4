# SIGRH+ Backend

Backend del Sistema Integral de Gestion de Recursos Humanos con IA (SIGRH+). Este repositorio concentra la API de negocio para reclutamiento, administracion de personal, asistencia, nomina, licencias y control de acceso por roles, con modulos de apoyo basados en inteligencia artificial.

## Contexto del producto

SIGRH+ busca automatizar y optimizar procesos clave de RRHH con una plataforma integral que combine gestion operativa y capacidades asistidas por IA.

- Nombre del producto: `SIGRH+`
- Objetivo: automatizar reclutamiento, evaluacion y administracion de personal con apoyo de IA
- Periodo de desarrollo informado en la presentacion: del `21 de abril de 2025` al `23 de junio de 2025`
- Metodologia de trabajo: `Scrum`, organizado en 5 sprints

### Resumen de hitos

- Sprint 0: relevamiento funcional, definicion de alcance y armado del backlog
- Sprint 1: maquetado inicial de las pantallas y validacion de flujos base
- Sprint 2: login, gestion de empleados, postulaciones y procesamiento de CVs
- Sprint 3: asistencia con reconocimiento facial, sueldos y roles
- Sprint 4: licencias, validaciones y pruebas finales
- Sprint 5: reporteria

La presentacion tambien menciona seguimiento por avance, calidad y eficiencia. En este repositorio se observan claramente los modulos de operacion de RRHH y los componentes de IA; la reporteria no aparece como un modulo dedicado en el backend inspeccionado.

## Stack verificado

Las tecnologias y librerias verificadas en el repositorio son:

- `Python`
- `FastAPI`
- `SQLModel` y `SQLAlchemy`
- `PostgreSQL`
- `Docker` y `docker-compose`
- `spaCy`
- `scikit-learn`
- `PyMuPDF` y `pypdf`

## Funcionalidades principales

El backend expone una API organizada por dominios de negocio. A partir de `src/main.py` y los controladores inspeccionados se verifican estas capacidades:

### Autenticacion, acceso y perfil

- inicio de sesion mediante `/auth/login`
- generacion de token para consumo del frontend
- consulta del usuario autenticado con `/auth/me`
- carga del perfil del empleado junto con cargo, sector, pais, provincia, rol y permisos

### Gestion de empleados

- alta de empleados con `/employees/register`
- listado general con posibilidad de filtrar por sector
- consulta de empleado por ID
- actualizacion de datos personales y laborales
- baja logica o eliminacion por ID
- cambio de password
- conteo de empleados activos para dashboard

### Estructura organizacional y datos maestros

- administracion de puestos de trabajo
- administracion de sectores
- catalogos de paises y provincias/estados
- asociacion de empleado con cargo, sector, ubicacion y turno
- gestion de habilidades y conceptos usados por otros procesos

### Reclutamiento y seleccion

- alta, listado, actualizacion y eliminacion de convocatorias laborales
- conteo de convocatorias activas para tablero
- asociacion de convocatorias con habilidades requeridas
- carga de postulaciones para una convocatoria
- validacion de si una convocatoria sigue aceptando postulaciones
- consulta individual o masiva de postulaciones por convocatoria
- actualizacion de estados de postulacion

### IA para matching de CVs

- evaluacion de candidatos contra una convocatoria mediante `/matcher/{job_opportunity_id}`
- procesamiento de CVs para comparar postulantes con habilidades o requerimientos de la vacante
- soporte en Python con `spaCy` y librerias de analisis para asistir el filtrado inicial

### Reconocimiento facial y fichadas

- registro inicial del rostro de un empleado
- actualizacion del registro facial
- verificacion de rostro antes de asociarlo o reutilizarlo
- fichada de ingreso y egreso por reconocimiento facial
- integracion con eventos de asistencia para registrar presencia real

### Asistencia, turnos y horas

- gestion de turnos
- alta, consulta, edicion y eliminacion de eventos de fichada
- consulta de fichadas por empleado y fecha
- resumen diario de asistencia por empleado activo
- registro y administracion de horas trabajadas

### Nomina

- consulta de horas por rango de fechas y empleado
- calculo de horas para proceso de nomina
- obtencion de registros pendientes de validacion
- soporte para estados de liquidacion y observaciones operativas desde el frontend

### Licencias

- listado de licencias con filtros por estado documental, estado de solicitud, empleado o sector
- consulta de tipos de licencia
- consulta puntual de una licencia
- alta de solicitudes de licencia autenticadas por token
- actualizacion de licencias existentes

### Roles y permisos

- listado y consulta de roles
- alta, edicion y baja de roles
- consulta de permisos disponibles
- asociacion de permisos al rol del empleado para controlar modulos del frontend

## Estructura general

El proyecto sigue una organizacion modular por dominio:

- `src/main.py`: punto de entrada de FastAPI
- `src/database/`: configuracion de persistencia y scripts SQL
- `src/auth/`: autenticacion y tokens
- `src/modules/`: dominios funcionales del sistema
- `src/cv_matching/`: logica de matching de CVs

## Puesta en marcha local

### Requisitos

- `Python 3.10` o superior
- `PostgreSQL` si se quiere correr con base de datos real

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd backend-sigrh-g4
```

### 2. Crear y activar un entorno virtual

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\Activate.ps1
```

Linux/macOS:

```bash
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Descargar modelos de spaCy

```bash
python -m spacy download es_core_news_lg
python -m spacy download en_core_web_lg
```

### 5. Configurar variables de entorno

Crear un archivo `.env` a partir de `.env.example`.

Variables operativas verificadas:

- `SECRET_KEY`
- `ALGORITHM`
- `DATABASE_URL`
- `TEST_DATABASE_URL`
- `USE_TEST_DATABASE`

Configuracion observada en el codigo:

- si `USE_TEST_DATABASE` no esta definido, se utiliza `DATABASE_URL`
- si `USE_TEST_DATABASE=true`, se utiliza `TEST_DATABASE_URL`
- para pruebas o desarrollo liviano puede usarse `sqlite`
- para un entorno cercano a produccion se espera `PostgreSQL`

Ejemplo base incluido en `.env.example`:

```env
SECRET_KEY=1234
ALGORITHM=HS256
DATABASE_URL=postgresql://user:password@localhost:5432/sigrh
TEST_DATABASE_URL=sqlite:///src/database/sigrh.db
```

### 6. Preparar la base de datos

El README historico del proyecto indica crear una base `sigrh` en PostgreSQL. Ademas, el repositorio incluye scripts SQL de apoyo en:

- `src/database/esquema_sigrh.sql`
- `src/database/data_entry.sql`
- `src/database/data/`

### 7. Levantar la API

```bash
uvicorn src.main:app --reload
```

Documentacion interactiva disponible por defecto en:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## Ejecucion con Docker

El repositorio incluye `docker-compose.yaml` con al menos estos servicios:

- `backend`: API FastAPI publicada en `8000`
- `db`: PostgreSQL publicado localmente como `8003:5432`
- `dev`: contenedor de desarrollo adicional

### Pasos sugeridos

1. Crear `.env` desde `.env.example`
2. Configurar `DATABASE_URL` para apuntar al host `db`
3. Definir la password de PostgreSQL en `.postgres-password`
4. Construir la imagen si hubo cambios en codigo o dependencias

```bash
docker-compose build backend
```

5. Levantar backend y base de datos

```bash
docker-compose up -d backend db
```

6. Ver logs

```bash
docker-compose logs backend
docker-compose logs db
```

7. Detener servicios

```bash
docker-compose down
```

8. Eliminar el volumen de datos de PostgreSQL si hace falta reiniciar el estado

```bash
docker volume rm postgres-data
```

## Superficies publicas documentadas

Sin modificar contratos ni APIs, este README resume los principales grupos de endpoints observables:

- `/auth`
- `/employees`
- `/documents`
- `/work-history`
- `/countries`
- `/states`
- `/sectors`
- `/jobs`
- `/opportunities`
- `/postulations`
- `/matcher`
- `/face_recognition`
- `/clock_events`
- `/employee_hours`
- `/shift`
- `/payroll`
- `/leaves`
- `/roles`
- `/permissions`
- `/abilities`
- `/concept`

La definicion detallada de request y response puede consultarse en Swagger y ReDoc al ejecutar la API.

## Consideraciones actuales

- `src/main.py` y `src/database/core.py` referencian un modulo de `configuration`
- en el arbol de archivos inspeccionado no aparecio la carpeta `src/modules/configuration`
- por eso no se documenta la configuracion del sistema como funcionalidad confirmada de este backend, sino como una inconsistencia o pendiente a validar
- la reporteria figura como hito de cierre en la presentacion, pero no aparece aqui como un modulo backend claramente identificado
