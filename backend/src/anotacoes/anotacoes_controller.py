from flask import request, jsonify
from src.db_helpers import registro_json
from src.anotacoes.anotacoes_service import AnotacoesService

def get_all():
    id_materias = request.args.get("id_materias")
    linhas = AnotacoesService.listar_anotacoes(id_materias)
    return jsonify([registro_json(linha) for linha in linhas]), 200

def get_one(id_anotacoes):
    linha = AnotacoesService.buscar_anotacao(id_anotacoes)
    return jsonify(registro_json(linha)), 200

def create():
    dados = request.get_json() or {}
    nova_anotacao = AnotacoesService.criar_anotacao(dados)
    return jsonify(registro_json(nova_anotacao)), 201

def update(id_anotacoes):
    dados = request.get_json() or {}
    anotacao_atualizada = AnotacoesService.atualizar_anotacao(id_anotacoes, dados)
    return jsonify(registro_json(anotacao_atualizada)), 200

def delete(id_anotacoes):
    AnotacoesService.deletar_anotacao(id_anotacoes)
    return jsonify({"mensagem": "Anotação removida com sucesso."}), 200