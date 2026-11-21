from flask import jsonify, request
from psycopg2 import IntegrityError, OperationalError
from psycopg2.errors import CheckViolation, ForeignKeyViolation, UniqueViolation
from src.api_errors import ApiError
from werkzeug.exceptions import HTTPException, RequestEntityTooLarge

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

    @app.errorhandler(OperationalError)
    def tratar_indisponibilidade_banco(erro):
        app.logger.error("Falha operacional no PostgreSQL (SQLSTATE %s)", erro.pgcode)
        return jsonify({"erro": "Banco de dados temporariamente indisponível"}), 503

    @app.errorhandler(HTTPException)
    def tratar_erro_http(erro):
        if not request.path.startswith("/api/"):
            return erro
        resposta = erro.get_response()
        mensagem = ("O corpo da requisição deve ter até 1 MB (1.048.576 bytes)."
                    if isinstance(erro, RequestEntityTooLarge) else erro.description)
        resposta.set_data(app.json.dumps({"erro": mensagem}))
        resposta.content_type = "application/json"
        return resposta

    @app.errorhandler(500)
    def tratar_erro_interno(erro):
        app.logger.exception("Erro interno na aplicação")
        return jsonify({"erro": "Erro interno do servidor"}), 500
