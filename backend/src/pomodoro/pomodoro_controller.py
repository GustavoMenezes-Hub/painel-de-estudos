from flask import request, jsonify
from src.db_helpers import registro_json
from src.pomodoro.pomodoro_service import PomodoroService

def get_all():
    id_materias = request.args.get("id_materias")
    linhas = PomodoroService.listar_pomodoros(id_materias)
    return jsonify([registro_json(linha) for linha in linhas]), 200

def get_one(id_pomodoro):
    linha = PomodoroService.buscar_pomodoro(id_pomodoro)
    return jsonify(registro_json(linha)), 200

def create():
    dados = request.get_json() or {}
    novo = PomodoroService.criar_pomodoro(dados)
    return jsonify(registro_json(novo)), 201

def update(id_pomodoro):
    dados = request.get_json() or {}
    atualizado = PomodoroService.atualizar_pomodoro(id_pomodoro, dados)
    return jsonify(registro_json(atualizado)), 200

def delete(id_pomodoro):
    PomodoroService.deletar_pomodoro(id_pomodoro)
    return jsonify({"mensagem": "Registro de Pomodoro removido com sucesso."}), 200