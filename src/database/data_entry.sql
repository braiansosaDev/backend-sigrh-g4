-- Script de inserción de datos de ejemplo para PostgreSQL

BEGIN;

-- Cargar países
INSERT INTO country (id, name) VALUES
(1, 'Argentina'),
(2, 'Brasil'),
(3, 'Chile')
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;


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


-- Sectores
INSERT INTO sector (id, name) VALUES
(1, 'Desarrollo'),
(2, 'Recursos Humanos'),
(3, 'Administración'),
(4, 'Diseño'),
(5, 'Contabilidad'),
(6, 'Proyectos')
ON CONFLICT (id) DO UPDATE SET name = EXCLUDED.name;


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


-- Cargar permisos
INSERT INTO permission (id, name, description) VALUES
(1, 'ABM Empleados', 'El usuario puede ingresar y accionar en ABM Empleados'),
(2, 'ABM Roles', 'El usuario puede operar con el ABM de roles'),
(3, 'ABM Postulaciones - Carga', 'El usuario puede Generar solicitudes en ABM postulaciones'),
(4, 'ABM Postulaciones - Aprobaciones', 'El usuario puede Generar autorizar en ABM postulaciones'),
(5, 'Asignacion de Roles - Carga', 'El usuario puede Asignar Roles a los empleados'),
(6, 'ABM Turnos', 'El usuario puede Generar turnos de trabajo'),
(7, 'Gestion Nomina empleados - Cargas', 'El usuario puede operar sobre la nomina de empleados'),
(8, 'Personalizacion del sistema', 'El usuario puede personalizar el sistema, logo, foto, colores,ect'),
(9, 'Gestion de licencias - Carga', 'El usuario puede Gestionar las licencias de los empleados'),
(10, 'Gestion de licencias - Aprobaciones', 'El usuario puede Aprobar las solicitudes licencias de los empleados'),
(11, 'Gestion Nomina empleados - Aprobaciones', 'El usuario puede aprobar operaciones sobre la nomina de empleados'),
(12, 'Asignacion de Roles - Aprobaciones', 'El usuario puede Aprobar las asignaciones de  Roles a los empleados')
ON CONFLICT (id) DO UPDATE 
SET name = EXCLUDED.name,
    description = EXCLUDED.description;


-- Cargar roles
INSERT INTO role (id, name, description) VALUES
(1, 'Analista RRHH', 'Analista de Recursos humanos'),
(2, 'Administrador Root', 'Usuario de Administrador ROOT IT'),
(3, 'Supervisor - RRHH', 'Supervisor del área de Recursos Humanos'),
(4, 'Empleado', 'Empleado de la empresa'),
(5, 'Supervisor - Empleados', 'Supervisor de los empleados'),
(6, 'Gerente RRHH', 'Gerente del área de Recursos Humanos'),
(7, 'Reclutador', 'Analista de RRHH que es Reclutador de talento')
ON CONFLICT (id) DO UPDATE 
SET name = EXCLUDED.name,
    description = EXCLUDED.description;

-- Cargar roles por permiso
INSERT INTO role_permission (role_id, permission_id) VALUES
(1,1), (1,7), (1,5), (1,9),
(2,8), (2,1), (2,2), (2,6),
(3,1), (3,7), (3,11), (3,5), (3,12), (3,9), (3,10), (3,3), (3,4),
(4,9),
(5,7), (5,11), (5,9), (5,10),
(6,1), (6,7), (6,11), (6,5), (6,12), (6,9), (6,10), (6,3), (6,4),
(7,4)
ON CONFLICT DO NOTHING;

INSERT INTO public.shift (description, type, working_hours, working_days) VALUES
  ('Turno mañana',      'Matutino', 8, 5),
  ('Turno tarde',      'Vespertino', 8, 5),
  ('Turno noche',       'Nocturno',  8, 6);

COMMIT;
