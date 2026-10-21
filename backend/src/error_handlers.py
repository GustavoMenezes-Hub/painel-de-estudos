from flask import jsonify
from psycopg2 import IntegrityError
from psycopg2.errors import CheckViolation, UniqueViolation
from src.api_errors import ApiError

def registrar_error_handlers(app):

    @app.errorhandler(ApiError)
    def tratar_api_error(erro):
        return jsonify({"erro": erro.mensagem}), erro.status

    @app.errorhandler(IntegrityError)
    def tratar_erro_banco(erro):
        if isinstance(erro, UniqueViolation):
            return jsonify({"erro": "Registro duplicado"}), 409

        if isinstance(erro, CheckViolation):
            return jsonify({"erro": "Dados violam uma regra do banco"}), 400

        return jsonify({"erro": "Conflito com dados existentes"}), 409

    @app.errorhandler(500)
    def tratar_erro_interno(erro):
        return jsonify({"erro": "Erro interno do servidor"}), 500