import matcher

text = """
EDUCACIÓN
EXPERIENCIA LABORAL
BRAIAN ORLANDO SOSA
DESARROLLADOR WEB
SOBRE MÍ
Soy un estudiante de la carrera de
Lic. en Sistemas y autodidacta
apasionado por la tecnología en
general y las soluciones que pueden
brindar en todos los rubros y
sectores.
HABILIDADES PRINCIPALES
Patrones de diseño (SOLID, MVC,
Strategy, etc.), arquitecturas basadas
en web.
Desarrollo Web (TypeScript,
JavaScript ES6, HTML5, CSS3,
Python)
Software para integración e
industria 4.0 (Python, MQTT)
Frameworks/Librerias: Tailwind CSS,
Node.js, NestJS, React.js (Next.js)
PostgreSQL, PL/PGSQL, ACID.
Git, GitHub, GitLab, GitHub Actions
Microsoft Azure, CI/CD pipelines
IDIOMAS
Inglés B1
DATOS DE CONTACTO
Celular: (+54) 011 2527-7961
Email: braianorlandososa@gmail.com
Fecha de nacimiento: 20 oct. 2000
Domicilio: Buenos Aires, Argentina.
Disponibilidad horaria: Full Time
LinkedIn: linkedin.com/in/braianorlando-sosa/
GitHub:
github.com/braiansosaDevbsosaDev
IT-Support
Supervisión y mantenimiento de sistemas
informáticos.
Mantenimiento de redes y servicios. Planeamiento
e implementación de software de proveedores.
Automatización de procesos con Google Apps
Script y Python.
Assist North S.A | Febrero 2021 - Agosto
2023
Automation - Google Apps Script
Desarrollo de formularios web personalizados para
homogenización de datos. (Bootstrap,Vue, GAS).
Proyección, desarrollo y testeo de sistemas en
conjunto. (Google Apps Script).
Automatización de procesos con Google Apps
Script (RPA).
TwoBits (México) | Noviembre 2022 - Febrero
2023
Universidad Nacional de General Sarmiento
Actualmente cursando el tercer año de la licenciatura y
tecnicatura en informatica.
Porcentaje de aprobación 70% (Tecnicatura).
Lic. en Sistemas - Tec. Univ. en Informática |
Febrero 2020 - Actualidad
Iters
Desarrollo Web FullStack con MySQL, Express, React,
Node.JS
Código de validación: 3285-1221-1421-3451
(iters.com.ar/verify/)
MERN FullStack - Desarrollo Web | Diciembre 2022
- Marzo 2023
Desarrollador Full Stack
Ingeniería y especificación de software para
productos internos de gestión empresarial (core) y
productos comercializables basados en web
enfocados a la automatización industrial y la
industria 4.0.
Desarrollo web full stack (Backend/Frontend).
Especialista en Backend y bases de datos.
Analista de infraestructura Cloud y CI/CD.
Especializado en Microsoft Azure.
GÖTTERT S.A | Septiembre 2023 - Act.
"""

words = [
    "FullStack",
    "React",
    "Node js",
    "SQL",
    "Microsoft Azure",
    "CI/CD",
    "TypeScript",
    "Python",
    "Industria 4.0",
    "Git",
    "Patrones de diseño",
]

result = matcher.find_words(text, words, model=matcher.load_spanish_model())

print(result)
