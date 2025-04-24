from app import db

#Creo las tablas necesarias. En este caso, solo candidato
class Candidato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    anios_experiencia = db.Column(db.Integer, nullable=False)
    nivel_educativo = db.Column(db.String(50), nullable=False)
    habilidades = db.Column(db.String(150), nullable=False)
    idiomas = db.Column(db.String(100), nullable=False)
    expectativa_salarial = db.Column(db.Float, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    es_apto = db.Column(db.Boolean, nullable=True) #Inicializo la columna en null para que sea determinada por el metodo de ml

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "anios_experiencia": self.anios_experiencia,
            "nivel_educativo": self.nivel_educativo,
            "habilidades": self.habilidades,
            "idiomas": self.idiomas,
            "expectativa_salarial": self.expectativa_salarial,
            "email": self.email,
            "es_apto": self.es_apto
        }
