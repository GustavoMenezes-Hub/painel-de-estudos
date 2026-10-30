from flask import jsonify, request
from psycopg2 import IntegrityError
from psycopg2.errors import CheckViolation, ForeignKeyViolation, UniqueViolation
from src.api_errors import ApiError
from werkzeug.exceptions import HTTPException

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
        if isinstance(erro, ForeignKeyViolation):
            return jsonify({"erro": "Operação bloqueada por registros relacionados"}), 409
        return jsonify({"erro": "Conflito com dados existentes"}), 409

    @app.errorhandler(HTTPException)
    def tratar_erro_http(erro):
        if not request.path.startswith("/api/"):
            return erro
        return jsonify({"erro": erro.description}), erro.code

    @app.errorhandler(500)
    def tratar_erro_interno(erro):
        app.logger.exception("Erro interno na aplicação")
        return jsonify({"erro": "Erro interno do servidor"}), 500