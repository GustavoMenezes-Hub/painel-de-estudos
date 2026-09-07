from flask import jsonify
from . import materias_service as service

def get_all():
    materias = service.list_all()
    return jsonify(materias)
