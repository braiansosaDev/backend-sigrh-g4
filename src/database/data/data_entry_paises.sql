-- Insertar países
INSERT INTO public.country (name) VALUES
('Argentina'),
('Brasil'),
('Estados Unidos'),
('México'),
('España');

-- Insertar provincias/estados

-- Provincias de Argentina
INSERT INTO public.state (name, country_id) VALUES
('Buenos Aires', 1),
('Catamarca', 1),
('Chaco', 1),
('Chubut', 1),
('Córdoba', 1),
('Corrientes', 1),
('Entre Ríos', 1),
('Formosa', 1),
('Jujuy', 1),
('La Pampa', 1),
('La Rioja', 1),
('Mendoza', 1),
('Misiones', 1),
('Neuquén', 1),
('Río Negro', 1),
('Salta', 1),
('San Juan', 1),
('San Luis', 1),
('Santa Cruz', 1),
('Santa Fe', 1),
('Santiago del Estero', 1),
('Tierra del Fuego', 1),
('Tucumán', 1),
('Ciudad Autónoma de Buenos Aires', 1);

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
