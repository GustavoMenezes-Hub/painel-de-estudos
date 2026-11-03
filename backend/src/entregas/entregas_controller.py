from flask import g, jsonify, request
from . import entregas_service as service

def get_all():
    return jsonify(service.list_all(g.id_usuario))

def get_one(id_entrega):
    return jsonify(service.get_one(id_entrega, g.id_usuario))

def create():
    return jsonify(service.cadastrar(request.get_json(silent=True), g.id_usuario)), 201

def update(id_entrega):
    return jsonify(service.atualizar(id_entrega, g.id_usuario, request.get_json(silent=True)))

def delete(id_entrega):
    service.excluir(id_entrega, g.id_usuario)
    return "", 204