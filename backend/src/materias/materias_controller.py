from flask import jsonify, request
from src.api_errors import ApiError
from . import materias_service as service

def get_all():
    materias = service.list_all()
    materias_dicts = [materia.to_dict() for materia in materias]
    return jsonify(materias_dicts)

def create():
    dados = request.get_json(silent=True)
    try:
        materia = service.create(dados)
    except ApiError as erro:
        return jsonify({"error": {"message": erro.mensagem}}), erro.status
    return jsonify(materia.to_dict()), 201


def update(id_materias):
    dados = request.get_json(silent=True)
    try:
        materia = service.update(id_materias, dados)
    except ApiError as erro:
        return jsonify({"error": {"message": erro.mensagem}}), erro.status
    return jsonify(materia.to_dict()), 200

def get_by_id(id_materias):
    try:
        materia = service.get_by_id(id_materias)
    except ApiError as erro:
        return jsonify({"error": {"message": erro.mensagem}}), erro.status
    return jsonify(materia.to_dict())
