from flask import g, jsonify, request
from src.api_errors import ApiError
from . import materias_service as service

def get_all():
    materias = service.list_all(g.id_usuario)
    materias_dicts = [materia.to_dict() for materia in materias]
    return jsonify(materias_dicts)

def create():
    dados = request.get_json(silent=True)
    materia = service.create(dados, g.id_usuario)
    return jsonify(materia.to_dict()), 201

def update(id_materias):
    dados = request.get_json(silent=True)
    materia = service.update(id_materias, dados, g.id_usuario)
    return jsonify(materia.to_dict()), 200

def get_by_id(id_materias):
    materia = service.get_by_id(id_materias, g.id_usuario)
    return jsonify(materia.to_dict())

def delete(id_materias):
    service.delete(id_materias, g.id_usuario)
    return "", 204