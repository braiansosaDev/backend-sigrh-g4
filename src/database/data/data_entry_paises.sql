-- Insertar países
INSERT INTO public.country (name) VALUES
('Argentina'),
('Brasil'),
('Estados Unidos'),
('México'),
('España');

-- Insertar provincias/estados

-- Argentina
INSERT INTO public.state (name, country_id) VALUES
('Buenos Aires', 1),
('Córdoba', 1),
('Santa Fe', 1),
('Mendoza', 1),
('Tucumán', 1);

-- Brasil
INSERT INTO public.state (name, country_id) VALUES
('São Paulo', 2),
('Rio de Janeiro', 2),
('Bahia', 2),
('Minas Gerais', 2),
('Paraná', 2);

-- Estados Unidos
INSERT INTO public.state (name, country_id) VALUES
('California', 3),
('Texas', 3),
('Florida', 3),
('New York', 3),
('Illinois', 3);

-- México
INSERT INTO public.state (name, country_id) VALUES
('Ciudad de México', 4),
('Jalisco', 4),
('Nuevo León', 4),
('Puebla', 4),
('Guanajuato', 4);

-- España
INSERT INTO public.state (name, country_id) VALUES
('Madrid', 5),
('Cataluña', 5),
('Andalucía', 5),
('Galicia', 5),
('País Vasco', 5);
