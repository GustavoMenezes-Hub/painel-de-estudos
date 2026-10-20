from flask import jsonify, request
from . import auth_service as service

def login():
    resposta = service.entrar(request.get_json(silent=True))
    return jsonify(resposta), 200