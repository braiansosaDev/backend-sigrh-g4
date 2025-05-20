-- Cargar países
INSERT INTO country (id, name) VALUES
(1, 'Argentina'),
(2, 'Brasil'),
(3, 'Chile');

-- Cargar provincias/estados
INSERT INTO state (id, name, country_id) VALUES
(1, 'Buenos Aires', 1),
(2, 'Córdoba', 1),
(3, 'Santa Fe', 1),
(4, 'Rio de Janeiro', 2),
(5, 'Sao Paulo', 2),
(6, 'Valparaíso', 3),
(7, 'Santiago', 3);

-- Sectores
INSERT INTO sector (id, name) VALUES
(1, 'Desarrollo'),
(2, 'Recursos Humanos'),
(3, 'Administración'),
(4, 'Diseño'),
(5, 'Contabilidad'),
(6, 'Proyectos');

-- Cargar puestos
INSERT INTO job (id, name, sector_id) VALUES
(1, 'Desarrollador', 1),
(2, 'Analista de Recursos Humanos', 2),
(3, 'Contador', 5),
(4, 'Diseñador Gráfico', 4),
(5, 'Gerente de Proyectos', 6),
(6, 'Asistente Administrativo', 3);

-- Cargar habilidades
INSERT INTO ability (id, name, description) VALUES
(1, 'Java', 'Lenguaje de programación orientado a objetos'),
(2, 'Python', 'Lenguaje de programación interpretado'),
(3, 'SQL', 'Lenguaje de consulta estructurado'),
(4, 'Diseño Gráfico', 'Habilidad en diseño visual'),
(5, 'Gestión de Proyectos', 'Habilidad en planificación y ejecución de proyectos'),
(6, 'Comunicación', 'Habilidad para transmitir información efectivamente'),
(7, 'PostgreSQL', 'Motor de bases de datos relacionales'),
(8, 'MongoDB', 'Motor de bases de datos no relacionales');

-- Cargar empleados
-- INSERT INTO employee (
--     id, user_id, first_name, last_name, dni, type_dni, personal_email, active,
--     role, password, phone, salary, job_id, birth_date, hire_date, address_street,
--     address_city, address_cp, address_state_id, address_country_id
-- ) VALUES
-- (1, 'fbarra138', 'Franco', 'Barraza', '42194138', 'dni', 'franco@sigrh.com', False, 'dev', 'hash123', '+541123234343', 1000.00, 1, '1999-05-05', '2025-05-05', 'Mitre 123', 'Polvorines', '1613', 1, 1),
-- (2, 'nsoza258', 'Nilda', 'Sosa', '42194258', 'dni', 'nilda@sigrh.com', False, 'rrhh', 'hashabc', '+541122334455', 1500.00, 2, '1980-10-15', '2020-01-10', 'Belgrano 456', 'Tigre', '1648', 1, 1),
-- (3, 'jrodriguez369', 'Joaquín', 'Rodríguez', '42194369', 'dni', 'jrodri@sigrh.com', False, 'dev', 'hashxyz', '+541134567890', 1200.00, 3, '1995-03-20', '2022-06-15', 'Rivadavia 789', 'San Fernando', '1670', 1, 1);