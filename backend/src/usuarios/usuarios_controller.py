from flask import g, jsonify, request
from . import usuarios_service as service

def get_all():
    return jsonify(service.list_all())

def get_one(id_usuario):
    return jsonify(service.get_one(id_usuario, g.id_usuario))

def me():
    return jsonify(service.get_one(g.id_usuario, g.id_usuario))

def create():
    return jsonify(service.cadastrar(request.get_json(silent=True))), 201

def update(id_usuario):
    return jsonify(service.atualizar(id_usuario, g.id_usuario, request.get_json(silent=True)))

def delete(id_usuario):
    service.excluir(id_usuario, g.id_usuario)
    return "", 204
