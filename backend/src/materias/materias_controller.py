from flask import jsonify
from . import materias_service as service

def get_all():
    materias = service.list_all()
    materias_dicts = [materia.to_dict() for materia in materias]
    return jsonify(materias_dicts)
