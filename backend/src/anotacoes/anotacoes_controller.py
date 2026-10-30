from flask import g, request, jsonify
from src.db_helpers import registro_json
from src.anotacoes.anotacoes_service import AnotacoesService

def get_all():
    id_materias = request.args.get("id_materias")
    linhas = AnotacoesService.listar_anotacoes(id_materias, g.id_usuario)
    return jsonify([registro_json(linha) for linha in linhas]), 200

def get_one(id_anotacoes):
    linha = AnotacoesService.buscar_anotacao(id_anotacoes, g.id_usuario)
    return jsonify(registro_json(linha)), 200

def create():
    dados = request.get_json(silent=True)
    nova_anotacao = AnotacoesService.criar_anotacao(dados, g.id_usuario)
    return jsonify(registro_json(nova_anotacao)), 201

def update(id_anotacoes):
    dados = request.get_json(silent=True)
    anotacao_atualizada = AnotacoesService.atualizar_anotacao(id_anotacoes, dados, g.id_usuario)
    return jsonify(registro_json(anotacao_atualizada)), 200

def delete(id_anotacoes):
    AnotacoesService.deletar_anotacao(id_anotacoes, g.id_usuario)
    return jsonify({"mensagem": "Anotação removida com sucesso."}), 200