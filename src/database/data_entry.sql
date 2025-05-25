-- Script de inserción de datos de ejemplo para PostgreSQL

-- BEGIN;

-- 1) PAISES Y ESTADOS
INSERT INTO public.country (name) VALUES
  ('Argentina'),
  ('Brasil');

INSERT INTO public.state (name, country_id) VALUES
  ('Córdoba', 1),
  ('Buenos Aires', 1),
  ('São Paulo', 2);

-- 2) SECTORES Y PUESTOS
INSERT INTO public.sector (name) VALUES
  ('Tecnología'),
  ('Recursos Humanos');

INSERT INTO public.job (name, sector_id) VALUES
  ('Desarrollador Backend', 1),
  ('Analista RRHH', 2);

-- 3) TURNOS
INSERT INTO public.shift (description, type, working_hours, working_days) VALUES
  ('Turno mañana',      'Diurno', 8, 5),
  ('Turno noche',       'Nocturno',  8, 7);

-- 4) EMPLEADO
-- INSERT INTO public.employee (
--   user_id, first_name, last_name, dni, type_dni,
--   personal_email, active, role, password, phone,
--   salary, job_id, birth_date, hire_date,
--   address_street, address_city, address_cp, address_state_id, address_country_id
-- ) VALUES (
--   'juan.perez', 'Juan', 'Pérez', '30.123.456', 'DNI',
--   'juan.perez@empresa.com', TRUE, 'Developer', 'secret123', '+5493512345678',
--   150.00, 1, '1985-04-15', '2024-01-02',
--   'Av. Colón 123', 'Córdoba', '5000', 1, 1
-- );

-- 5) EVENTOS DE RELOJ (CLOCK EVENTS)
-- Juan Pérez entra y sale durante dos días:
-- INSERT INTO public.clock_events (employee_id, event_date, event_type, source, device_id) VALUES
--   -- Día 1
--   (1, '2025-05-01 08:15:00', 'IN',  'App móvil', 'DEV-A1'),
--   (1, '2025-05-01 12:30:00', 'OUT', 'App móvil', 'DEV-A1'),
--   (1, '2025-05-01 13:45:00', 'IN',  'App móvil', 'DEV-A1'),
--   (1, '2025-05-01 18:05:00', 'OUT', 'App móvil', 'DEV-A1'),
--   -- Día 2
--   (1, '2025-05-02 08:05:00', 'IN',  'Terminal',  'TER-01'),
--   (1, '2025-05-02 12:00:00', 'OUT', 'Terminal',  'TER-01'),
--   (1, '2025-05-02 13:00:00', 'IN',  'Terminal',  'TER-01'),
--   (1, '2025-05-02 17:55:00', 'OUT', 'Terminal',  'TER-01');

-- 6) EMPLEADO_HOURS (Cálculo diario de salario)
-- Supongamos que el turno asignado es 1 (Turno mañana):
-- INSERT INTO public.employee_hours (
--   employee_id, concept_id, shift_id, check_count, work_date,
--   register_type, first_check_in, last_check_out, time_worked,
--   daily_salary, pay, notes
-- ) VALUES
--   (1, NULL, 1, 4, '2025-05-01', 'PRESENCIA', '08:15:00', '18:05:00', '09:35:00', 150.00 * 9.5833, FALSE, ''),
--   (1, NULL, 1, 4, '2025-05-02', 'PRESENCIA', '08:05:00', '17:55:00', '08:50:00', 150.00 * 8.8333, FALSE, '');

-- COMMIT;
