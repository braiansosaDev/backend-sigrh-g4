import matcher

text = """
EDUCACIÓN\r\nEXPERIENCIA LABORAL\r\nBRAIAN ORLANDO SOSA\r\nDESARROLLADOR WEB\r\nSOBRE MÍ\r\nSoy un estudiante de la carrera de\r\nLic. en Sistemas y autodidacta\r\napasionado por la tecnología en\r\ngeneral y las soluciones que pueden\r\nbrindar en todos los rubros y\r\nsectores.\r\nHABILIDADES PRINCIPALES\r\nPatrones de diseño (SOLID, MVC,\r\nStrategy, etc.), arquitecturas basadas\r\nen web.\r\nDesarrollo Web (TypeScript,\r\nJavaScript ES6, HTML5, CSS3,\r\nPython)\r\nSoftware para integración e\r\nindustria 4.0 (Python, MQTT)\r\nFrameworks/Librerias: Tailwind CSS,\r\nNode.js, NestJS, React.js (Next.js)\r\nPostgreSQL, PL/PGSQL, ACID.\r\nGit, GitHub, GitLab, GitHub Actions\r\nMicrosoft Azure, CI/CD pipelines\r\nIDIOMAS\r\nInglés B1\r\nDATOS DE CONTACTO\r\nCelular: (+54) 011 2527-7961\r\nEmail: braianorlandososa@gmail.com\r\nFecha de nacimiento: 20 oct. 2000\r\nDomicilio: Buenos Aires, Argentina.\r\nDisponibilidad horaria: Full Time\r\nLinkedIn: linkedin.com/in/braianorlando-sosa/\r\nGitHub:\r\ngithub.com/braiansosaDevbsosaDev\r\nIT-Support\r\nSupervisión y mantenimiento de sistemas\r\ninformáticos.\r\nMantenimiento de redes y servicios. Planeamiento\r\ne implementación de software de proveedores.\r\nAutomatización de procesos con Google Apps\r\nScript y Python.\r\nAssist North S.A | Febrero 2021 - Agosto\r\n2023\r\nAutomation - Google Apps Script\r\nDesarrollo de formularios web personalizados para\r\nhomogenización de datos. (Bootstrap,Vue, GAS).\r\nProyección, desarrollo y testeo de sistemas en\r\nconjunto. (Google Apps Script).\r\nAutomatización de procesos con Google Apps\r\nScript (RPA).\r\nTwoBits (México) | Noviembre 2022 - Febrero\r\n2023\r\nUniversidad Nacional de General Sarmiento\r\nActualmente cursando el tercer año de la licenciatura y\r\ntecnicatura en informatica.\r\nPorcentaje de aprobación 70% (Tecnicatura).\r\nLic. en Sistemas - Tec. Univ. en Informática |\r\nFebrero 2020 - Actualidad\r\nIters\r\nDesarrollo Web FullStack con MySQL, Express, React,\r\nNode.JS\r\nCódigo de validación: 3285-1221-1421-3451\r\n(iters.com.ar/verify/)\r\nMERN FullStack - Desarrollo Web | Diciembre 2022\r\n- Marzo 2023\r\nDesarrollador Full Stack\r\nIngeniería y especificación de software para\r\nproductos internos de gestión empresarial (core) y\r\nproductos comercializables basados en web\r\nenfocados a la automatización industrial y la\r\nindustria 4.0.\r\nDesarrollo web full stack (Backend/Frontend).\r\nEspecialista en Backend y bases de datos.\r\nAnalista de infraestructura Cloud y CI/CD.\r\nEspecializado en Microsoft Azure.\r\nGÖTTERT S.A | Septiembre 2023 - Act.
"""

required_words = ["java"]

desired_words = ["comunicacion"]

normalized_required_words = matcher.normalize_words(required_words)
normalized_desired_words = matcher.normalize_words(desired_words)
normalized_text = matcher.normalize(text)
model = matcher.load_spanish_model()


required_words_match = matcher.find_required_words(
    normalized_text, normalized_required_words, model
)
desired_words_match = matcher.find_desired_words(
    normalized_text, normalized_desired_words, model
)

print(
    f"RESULTADO FINAL: {required_words_match['SUITABLE'] and desired_words_match['SUITABLE']}",
    f"\nPALABRAS REQUERIDAS NO ENCONTRADAS: {required_words_match['WORDS_NOT_FOUND']}",
    f"\nPALABRAS DESEADAS ENCONTRADAS: {desired_words_match['WORDS_FOUND']}",
    f"\nPALABRAS DESEADAS NO ENCONTRADAS: {desired_words_match['WORDS_NOT_FOUND']}",
)
