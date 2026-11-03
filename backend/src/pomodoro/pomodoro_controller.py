from flask import g, request, jsonify
from src.db_helpers import registro_json
from src.pomodoro.pomodoro_service import PomodoroService

def get_all():
    id_materias = request.args.get("id_materias")
    linhas = PomodoroService.listar_pomodoros(id_materias, g.id_usuario)
    return jsonify([registro_json(linha) for linha in linhas]), 200

def get_one(id_pomodoro):
    linha = PomodoroService.buscar_pomodoro(id_pomodoro, g.id_usuario)
    return jsonify(registro_json(linha)), 200

def create():
    dados = request.get_json(silent=True)
    novo = PomodoroService.criar_pomodoro(dados, g.id_usuario)
    return jsonify(registro_json(novo)), 201

def update(id_pomodoro):
    dados = request.get_json(silent=True)
    atualizado = PomodoroService.atualizar_pomodoro(id_pomodoro, dados, g.id_usuario)
    return jsonify(registro_json(atualizado)), 200

def delete(id_pomodoro):
    PomodoroService.deletar_pomodoro(id_pomodoro, g.id_usuario)
    return jsonify({"mensagem": "Registro de Pomodoro removido com sucesso."}), 200