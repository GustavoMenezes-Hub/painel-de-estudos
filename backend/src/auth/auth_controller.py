
from flask import jsonify, request
from . import auth_service as service


def login():
    """
    Realiza a autenticação do usuário.

    ---
    tags:
      - Autenticação

    consumes:
      - application/json

    produces:
      - application/json

    parameters:
      - in: body
        name: credenciais
        required: true
        schema:
          type: object
          required:
            - email
            - senha
          properties:
            email:
              type: string
              example: usuario@email.com
            senha:
              type: string
              example: "123456"

    responses:
      200:
        description: Login realizado com sucesso.
        schema:
          type: object
          properties:
            access_token:
              type: string
              description: Token de autenticação.
              example: token_gerado
            token_type:
              type: string
              example: Bearer
            expires_in:
              type: integer
              example: 86400
            usuario:
              type: object
              properties:
                id_usuarios:
                  type: integer
                  example: 1
                nome:
                  type: string
                  example: Gustavo
                email:
                  type: string
                  example: gustavo@email.com

      400:
        description: Dados inválidos ou ausentes.
        schema:
          type: object
          properties:
            erro:
              type: string
              example: Email e senha são obrigatórios.

      401:
        description: Email ou senha inválidos.
        schema:
          type: object
          properties:
            erro:
              type: string
              example: Email ou senha inválidos.

    """
    resposta = service.entrar(request.get_json(silent=True))
    return jsonify(resposta), 200


   