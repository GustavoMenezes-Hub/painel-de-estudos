from flask import current_app, g, jsonify, request
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from src.usuarios import usuarios_repository

DURACAO_TOKEN_SEGUNDOS = 24 * 60 * 60

def _assinador():
    return URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"],
        salt="painel-estudos-autenticacao-v1",
    )

def gerar_token(id_usuario, versao):
    return _assinador().dumps({"id_usuarios": id_usuario, "versao": versao})

def verificar_autenticacao():
    autorizacao = request.headers.get("Authorization", "")
    esquema, separador, token = autorizacao.partition(" ")
    if esquema.lower() != "bearer" or not separador or not token.strip():
        return jsonify({"erro": "Token Bearer obrigatório"}), 401
    try:
        conteudo = _assinador().loads(token.strip(), max_age=DURACAO_TOKEN_SEGUNDOS)
        id_usuario = conteudo.get("id_usuarios")
        if not isinstance(id_usuario, int) or isinstance(id_usuario, bool):
            raise ValueError("ID inválido")
    except (BadSignature, SignatureExpired, ValueError, AttributeError, TypeError):
        return jsonify({"erro": "Token inválido ou expirado"}), 401
    versao = usuarios_repository.versao_token(id_usuario)
    if versao is None or versao != conteudo.get("versao"):
        return jsonify({"erro": "Token inválido ou expirado"}), 401
    g.id_usuario = id_usuario
    return None