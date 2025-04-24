from flask import Blueprint, request, jsonify
from app.models import db, Candidato
from app.clasificacion_candidatos_model import es_apto

bp = Blueprint('main', __name__)

#Metodo para validar id
def es_id_valido(id):
    if id < 1:
        return False

    candidato = Candidato.query.get(id)
    if not candidato:
        return False
    
    return True

#Crea un objeto candidato con los datos pasados por json en el formulario
@bp.route('/candidatos', methods=['POST'])
def agregar_candidato():
    datos = request.json
    nuevo_candidato = Candidato(
        nombre=datos['nombre'],
        anios_experiencia=datos['anios_experiencia'],
        nivel_educativo=datos['nivel_educativo'],
        habilidades=datos['habilidades'],
        idiomas=datos['idiomas'],
        expectativa_salarial=datos['expectativa_salarial'],
        email=datos['email']
    )
    db.session.add(nuevo_candidato)
    db.session.commit()
    return jsonify({"mensaje": "Candidato agregado"}), 201

#Consulta la tabla Candidato 
@bp.route('/candidatos', methods=['GET'])
def obtener_candidatos():
    candidatos = Candidato.query.all()
    return jsonify([c.to_dict() for c in candidatos])

#Metodo para actualizar candidatos
@bp.route('/candidatos/<int:id>', methods=['PUT'])
def actualizar_candidato(id):
    if not es_id_valido(id):
        return jsonify({"error": "El ID ingresado no es válido o no existe"}), 400

    datos = request.json
    candidato = Candidato.query.get(id)

    candidato.nombre = datos.get('nombre', candidato.nombre)
    candidato.anios_experiencia = datos.get('anios_experiencia', candidato.anios_experiencia)
    candidato.nivel_educativo = datos.get('nivel_educativo', candidato.nivel_educativo)
    candidato.habilidades = datos.get('habilidades', candidato.habilidades)
    candidato.idiomas = datos.get('idiomas', candidato.idiomas)
    candidato.expectativa_salarial = datos.get('expectativa_salarial', candidato.expectativa_salarial)
    candidato.email = datos.get('email', candidato.email)

    db.session.commit()
    return jsonify({"mensaje": f"Candidato con ID {id} actualizado correctamente"}), 200

#Filtra candidato por su id
@bp.route('/candidatos/<int:id>', methods=['GET'])
def obtener_candidato(id):
    if not es_id_valido(id):
        return jsonify({"error": "El ID ingresado no es válido o no existe"}), 400

    candidato = Candidato.query.get(id)
    return jsonify(candidato.to_dict())

#Elimina un candidato por id si es que existe
@bp.route('/candidatos/<int:id>', methods=['DELETE'])
def eliminar_candidato(id):
    if not es_id_valido(id):
        return jsonify({"error": "El ID ingresado no es válido o no existe"}), 400

    candidato = Candidato.query.get(id)
    db.session.delete(candidato)
    db.session.commit()
    return jsonify({"mensaje": f"Candidato con ID {id} eliminado correctamente"}), 200

#Evalúa candidato por id y modificar la tabla
@bp.route('/candidatos/<int:id>/evaluar', methods=['GET'])
def evaluar_candidato(id):
    if not es_id_valido(id):
        return jsonify({"error": "El ID ingresado no es válido o no existe"}), 400

    candidato = Candidato.query.get(id)
    candidato_dict = candidato.to_dict()
    resultado = es_apto(candidato_dict)

    candidato.es_apto = resultado
    db.session.commit()

    return jsonify({"es_apto": resultado}), 200

#Evalúa la tabla completa de candidatos y la modifica
@bp.route('/candidatos/evaluar-candidatos', methods=['POST'])
def evaluar_candidatos():
    candidatos = Candidato.query.all()

    if not candidatos:
        return jsonify({"mensaje": "No hay candidatos para evaluar"}), 404

    resultados = []

    for candidato in candidatos:
        candidato_dict = candidato.to_dict()
        resultado = es_apto(candidato_dict)
        candidato.es_apto = resultado
        resultados.append({
            "id": candidato.id,
            "nombre": candidato.nombre,
            "es_apto": resultado
        })

    db.session.commit()

    return jsonify({
        "mensaje": f"{len(resultados)} candidatos evaluados correctamente",}), 200

#Filtra los candidatos aptos de la tabla candidatos
@bp.route('/candidatos/aptos', methods=['GET'])
def obtener_candidatos_aptos():
    candidatos_aptos = Candidato.query.filter_by(es_apto=True).all()

    if not candidatos_aptos:
        return jsonify({"mensaje": "No hay candidatos aptos"}), 404

    return jsonify([c.to_dict() for c in candidatos_aptos]), 200





