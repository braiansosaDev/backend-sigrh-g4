BEGIN;

-- IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE IMPORTANTE
--
-- Si agregás nuevas tablas agregá la llamada a setval
-- como en las demás (solo cambiar el nombre de la tabla)
-- para evitar que dé error de ID duplicada al agregar
-- nuevas filas.

-- Cargar países
INSERT INTO country (id, name) VALUES
(1, 'Argentina'),
(2, 'Brasil'),
(3, 'Chile')
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;
SELECT setval(pg_get_serial_sequence('country', 'id'), (SELECT MAX(id) FROM country));

-- Cargar provincias/estados
INSERT INTO state (id, name, country_id) VALUES
(1, 'Buenos Aires', 1),
(2, 'Córdoba', 1),
(3, 'Santa Fe', 1),
(4, 'Rio de Janeiro', 2),
(5, 'Sao Paulo', 2),
(6, 'Valparaíso', 3),
(7, 'Santiago', 3)
ON CONFLICT (id) DO UPDATE
SET name = EXCLUDED.name,
country_id = EXCLUDED.country_id;
SELECT setval(pg_get_serial_sequence('state', 'id'), (SELECT MAX(id) FROM state));

-- Sectores
INSERT INTO sector (id, name) VALUES
(1, 'Desarrollo'),
(2, 'Recursos Humanos'),
(3, 'Administración'),
(4, 'Diseño'),
(5, 'Contabilidad'),
(6, 'Proyectos')
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;
SELECT setval(pg_get_serial_sequence('sector', 'id'), (SELECT MAX(id) FROM sector));

-- Cargar puestos
INSERT INTO job (id, name, sector_id) VALUES
(1, 'Desarrollador', 1),
(2, 'Analista de Recursos Humanos', 2),
(3, 'Contador', 5),
(4, 'Diseñador Gráfico', 4),
(5, 'Gerente de Proyectos', 6),
(6, 'Asistente Administrativo', 3)
ON CONFLICT (id) DO UPDATE
SET name = EXCLUDED.name,
sector_id = EXCLUDED.sector_id;
SELECT setval(pg_get_serial_sequence('job', 'id'), (SELECT MAX(id) FROM job));

-- Cargar habilidades
INSERT INTO ability (id, name, description) VALUES
(1, 'Java', 'Lenguaje de programación orientado a objetos'),
(2, 'Python', 'Lenguaje de programación interpretado'),
(3, 'SQL', 'Lenguaje de consulta estructurado'),
(4, 'Diseño Gráfico', 'Habilidad en diseño visual'),
(5, 'Gestión de Proyectos', 'Habilidad en planificación y ejecución de proyectos'),
(6, 'Comunicación', 'Habilidad para transmitir información efectivamente'),
(7, 'PostgreSQL', 'Motor de bases de datos relacionales'),
(8, 'MongoDB', 'Motor de bases de datos no relacionales')
ON CONFLICT (id) DO UPDATE
SET name = EXCLUDED.name,
description = EXCLUDED.description;
SELECT setval(pg_get_serial_sequence('ability', 'id'), (SELECT MAX(id) FROM ability));

-- Cargar permisos
INSERT INTO permission (id, name, description) VALUES
(1, 'ABM Empleados', 'El usuario puede ingresar y accionar en ABM Empleados'),
(2, 'ABM Roles', 'El usuario puede operar con el ABM de roles'),
(3, 'ABM Postulaciones - Carga', 'El usuario puede Generar solicitudes en ABM postulaciones'),
(4, 'ABM Postulaciones - Aprobaciones', 'El usuario puede Generar autorizar en ABM
postulaciones'),
(5, 'Asignacion de Roles - Carga', 'El usuario puede Asignar Roles a los empleados'),
(6, 'ABM Turnos', 'El usuario puede Generar turnos de trabajo'),
(7, 'Gestion Nomina empleados - Cargas', 'El usuario puede operar sobre la nomina de
empleados'),
(8, 'Personalizacion del sistema', 'El usuario puede personalizar el sistema, logo, foto,
colores,ect'),
(9, 'Gestion de licencias - Carga', 'El usuario puede Gestionar las licencias de los empleados'),
(10, 'Gestion de licencias - Aprobaciones', 'El usuario puede Aprobar las solicitudes licencias de
los empleados'),
(11, 'Gestion Nomina empleados - Aprobaciones', 'El usuario puede aprobar operaciones sobre
la nomina de empleados'),
(12, 'Asignacion de Roles - Aprobaciones', 'El usuario puede Aprobar las asignaciones de
Roles a los empleados'),
(13, 'ABM Fichadas', 'El usuario puede acceder a la pestania de asistencia')
ON CONFLICT (id) DO UPDATE
SET name = EXCLUDED.name,
description = EXCLUDED.description;
SELECT setval(pg_get_serial_sequence('permission', 'id'), (SELECT MAX(id) FROM permission));

-- Cargar roles
INSERT INTO role (id, name, description) VALUES
(1, 'Analista RRHH', 'Analista de Recursos humanos'),
(2, 'Administrador Root', 'Usuario de Administrador ROOT IT'),
(3, 'Supervisor - RRHH', 'Supervisor del área de Recursos Humanos'),
(4, 'Empleado', 'Empleado de la empresa'),
(5, 'Supervisor - Empleados', 'Supervisor de los empleados'),
(6, 'Gerente RRHH', 'Gerente del área de Recursos Humanos'),
(7, 'Reclutador', 'Analista de RRHH que es Reclutador de talento'),
(8, 'Dev', 'Desarrollador del sistema')
ON CONFLICT (id) DO UPDATE
SET name = EXCLUDED.name,
description = EXCLUDED.description;
SELECT setval(pg_get_serial_sequence('role', 'id'), (SELECT MAX(id) FROM role));

-- Cargar permisos de roles
INSERT INTO role_permission (role_id, permission_id) VALUES
(1,1), (1,7), (1,5), (1,9), (1,5), (1, 10), (1, 13),
(2,8), (2,1), (2,2), (2,6), (2,5),
(3,1), (3,7), (3,11), (3,5), (3,12), (3,9), (3,10), (3,3), (3,4), (3, 13),
(4,9),
(5,11), (5,9),(5,10),
(6,1), (6,7), (6,11), (6,5), (6,12), (6,9), (6,10), (6,3), (6,4), (6, 13),
(7,3),
-- Nuevo rol: Developer
(8,1), (8,2), (8,3), (8,4), (8,5), (8,6), (8,7), (8,8), (8,9), (8,10), (8,11), (8,12), (8,13)
ON CONFLICT DO NOTHING;

-- Cargar shifts
INSERT INTO shift (id, description, type, working_hours, working_days) VALUES
  (1, 'turno mañana',      'matutino', 8, 5),
  (2, 'turno tarde',      'vespertino', 8, 5),
  (3, 'turno noche',       'nocturno',  8, 7)
ON CONFLICT (id) DO UPDATE SET
description = EXCLUDED.description,
type = EXCLUDED.type,
working_hours = EXCLUDED.working_hours,
working_days = EXCLUDED.working_days;
SELECT setval(pg_get_serial_sequence('shift', 'id'), (SELECT MAX(id) FROM shift));

-- Cargar tipos de licencia
INSERT INTO leave_type (id, type, justification_required) VALUES
(1, 'Licencia por maternidad', True),
(2, 'Licencia por paternidad', True),
(3, 'Licencia médica por enfermedad común', False),
(4, 'Licencia médica por accidente laboral', False),
(5, 'Licencia por enfermedad familiar grave', False),
(6, 'Licencia por duelo', False),
(7, 'Licencia por casamiento', True),
(8, 'Licencia sindical', True),
(9, 'Licencia por estudio o examen', True),
(10, 'Licencia por adopción', True),
(11, 'Licencia por donación de sangre', False),
(12, 'Licencia por fuerza mayor', False),
(13, 'Licencia por mudanza', True),
(14, 'Licencia por trámite personal urgente', False),
(15, 'Vacaciones', False),
(16, 'Licencia médica por enfermedad grave', True),
(17, 'Licencia con otros motivos', False)
ON CONFLICT (id) DO UPDATE SET
type = EXCLUDED.type,
justification_required = EXCLUDED.justification_required;
SELECT setval(pg_get_serial_sequence('leave_type', 'id'), (SELECT MAX(id) FROM leave_type));

-- Cargar empleado de prueba
-- Usuario: bsosa672
-- Contraseña: 1234
INSERT INTO public.employee
(id, user_id, first_name, last_name, dni, type_dni, personal_email, active, role_id, password, phone, salary, job_id, birth_date, hire_date, address_street, address_city, address_cp, address_state_id, address_country_id, shift_id)
VALUES(1, 'bsosa672', 'Braian', 'Sosa', '43022672', 'du', 'braianorlandososa@gmail.com', true, 2, '$2b$12$hTsvK48LWxRA3Cet8bHIi..SdpxgWyMyQMlfsZd24WGRcshuTXcGK', '+2131125277960', 1, 1, '2000-10-20', '2025-05-06', 'asdadsad', '123123', 'string1231231', 1, 1, 3)
ON CONFLICT (id) DO NOTHING;
SELECT setval(pg_get_serial_sequence('employee', 'id'), (SELECT MAX(id) FROM employee));

COMMIT;
