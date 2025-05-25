-- Script de inserción de datos de ejemplo para PostgreSQL

-- BEGIN;

-- 1. Paises
-- INSERT INTO country (id, name) VALUES
--   (1, 'Argentina'),
--   (2, 'Chile');

-- -- 2. Provincias / Estados
-- INSERT INTO state (id, country_id, name) VALUES
--   (1, 1, 'Buenos Aires'),
--   (2, 1, 'Córdoba'),
--   (3, 2, 'Región Metropolitana');

-- -- 3. Sectores
-- INSERT INTO sector (id, name) VALUES
--   (1, 'Tecnología'),
--   (2, 'Finanzas');

-- -- 4. Puestos (job)
-- INSERT INTO job (id, sector_id, name) VALUES
--   (1, 1, 'Desarrollador Backend'),
--   (2, 1, 'Desarrollador Frontend'),
--   (3, 2, 'Analista Financiero');

-- 5. Empleados
-- INSERT INTO employee (
--   id, job_id, address_state_id, address_country_id, user_id,
--   first_name, last_name, dni, type_dni, personal_email,
--   password, phone, address_street, address_city, address_cp,
--   salary, active, birth_date, hire_date, photo, facial_register
-- ) VALUES
--   (1, 1, 1, 1, 'emp001', 'María', 'Gómez', '12345678', 'DNI', 'maria.gomez@example.com',
--    'hashed_pwd1', '+5491112345678', 'Calle Falsa 123', 'Buenos Aires', '1000',
--    150000, TRUE, '1988-05-10 00:00:00', '2022-01-15 09:00:00', NULL, NULL),
--   (2, 2, 2, 1, 'emp002', 'Juan', 'Pérez', '87654321', 'DNI', 'juan.perez@example.com',
--    'hashed_pwd2', '+5493518765432', 'Av. Siempre Viva 742', 'Córdoba', '5000',
--    130000, TRUE, '1990-11-20 00:00:00', '2023-06-01 08:30:00', NULL, NULL);

-- 6. Habilidades (ability)
INSERT INTO ability (id, name, description) VALUES
  (1, 'Python', 'Programación backend'),
  (2, 'JavaScript', 'Programación frontend'),
  (3, 'SQL', 'Gestión de bases de datos relacionales'),
  (4, 'Trabajo en equipo', 'Habilidad blanda de colaboración');

-- 7. Ofertas de trabajo (job_opportunity)
INSERT INTO job_opportunity (
  id, owner_employee_id, state_id, budget, budget_currency_id,
  status, work_mode, title, description, created_at, updated_at
) VALUES
  (1, 1, 1, 120000, 'USD', 'ACTIVO', 'REMOTO',
   'Backend Developer Senior', 'Desarrollo de APIs REST en Python y PostgreSQL.',
   '2025-05-01 10:00:00', '2025-05-01 10:00:00'),
  (2, 2, 2, 90000, 'USD', 'ACTIVO', 'HIBRIDO',
   'Frontend Developer', 'Maquetación y dinámicas con React.js.',
   '2025-04-20 09:30:00', '2025-04-20 09:30:00');

-- 8. Habilidades por oferta (job_opportunity_ability)
INSERT INTO job_opportunity_ability (job_opportunity_id, ability_id, ability_type) VALUES
  (1, 1, 'REQUERIDA'),
  (1, 3, 'REQUERIDA'),
  (1, 4, 'DESEADA'),
  (2, 2, 'REQUERIDA'),
  (2, 3, 'REQUERIDA');

-- 9. Documentos (document)
-- INSERT INTO document (id, employee_id, name, extension, creation_date, file, active) VALUES
--   (1, 1, 'Certificado Python', 'pdf', '2023-03-10 14:00:00', NULL, TRUE),
--   (2, 2, 'Portafolio Frontend', 'pdf', '2024-01-05 11:15:00', NULL, TRUE);

-- 10. Historial laboral (work_history)
-- INSERT INTO work_history (id, employee_id, job_id, from_date, to_date, company_name, notes) VALUES
--   (1, 1, 3, '2018-07-01 00:00:00', '2022-01-14 23:59:59', 'Finanzas SA', 'Analista de datos financieros'),
--   (2, 2, 1, '2019-09-01 00:00:00', '2023-05-31 23:59:59', 'Tech Solutions', 'Desarrollador frontend');

-- 11. Conceptos de horas (concept)
INSERT INTO concept (id, arca_concept_id, description) VALUES
  (1, 100, 'Horas normales'),
  (2, 101, 'Horas extras');

-- 12. Turnos (shift)
INSERT INTO shift (id, description, type) VALUES
  (1, 'Mañana', 'diurno'),
  (2, 'Tarde', 'vespertino');

-- 13. Registro de horas trabajadas (employee_hours)
INSERT INTO employee_hours (
  id, employee_id, concept_id, shift_id, weekday, date,
  register_type, first_check_in, last_check_out, check_count,
  amount, hours, pay, notes
) VALUES
  (1, 1, 1, 1, 3, '2025-05-12', 'ingreso', '08:00:00', '17:00:00', 2,
   8.0, '09:00:00', TRUE, 'Día habitual'),
  (2, 2, 2, 2, 2, '2025-05-13', 'ingreso', '10:00:00', '19:00:00', 2,
   9.0, '09:00:00', TRUE, 'Hora extra incluida');

-- 14. Eventos de reloj (clock_events)
INSERT INTO clock_events (id, employee_id, event_date, event_type, source, device_id) VALUES
  (1, 1, '2025-05-12 08:00:00', 'IN', 'app', 'dev123'),
  (2, 2, '2025-05-13 10:00:00', 'OUT', 'biométrico', 'dev321');

-- 15. Postulaciones (postulation)
INSERT INTO postulation (
  id, job_opportunity_id, address_country_id, address_state_id,
  name, surname, email, phone_number, cv_file,
  status, suitable, ability_match, evaluated_at, created_at, updated_at
) VALUES
  (1, 1, 1, 1, 'Ana', 'López', 'ana.lopez@example.com', '+549116001234',
   'ana_lopez_cv.pdf', 'PENDIENTE', FALSE,
   '{"Python": 0.80, "SQL": 0.70, "Trabajo en equipo": 0.95}',
   NULL, '2025-05-15 13:45:00', '2025-05-15 13:45:00'),
  (2, 2, 1, 2, 'Luis', 'Martínez', 'luis.martinez@example.com', '+549115005678',
   'luis_martinez_cv.pdf', 'ACEPTADA', TRUE,
   '{"JavaScript": 0.85, "SQL": 0.75}',
   '2025-05-16 11:20:00', '2025-05-14 09:00:00', '2025-05-16 11:20:00');

-- COMMIT;
