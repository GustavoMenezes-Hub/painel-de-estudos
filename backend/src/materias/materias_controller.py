
from flask import g, jsonify, request
from . import materias_service as service


def get_all():
    """
    Lista as matérias do usuário autenticado.

    ---
    tags:
      - Matérias
    security:
      - Bearer: []

    responses:
      200:
        description: Lista de matérias retornada.
        schema:
          type: array
          items:
            type: object
            properties:
              id_materias:
                type: integer
                example: 1
              nome:
                type: string
                example: Introdução à Administração
              descricao:
                type: string
                example: Fundamentos de administração
              id_usuarios:
                type: integer
                example: 1
              data_criacao:
                type: string
                example: "Fri, 30 Oct 2026 12:11:43 GMT"
      401:
        description: Token ausente, inválido ou expirado.
    """
    materias = service.list_all(g.id_usuario)
    materias_dicts = [materia.to_dict() for materia in materias]
    return jsonify(materias_dicts)


def create():
    """
    Cadastra uma nova matéria.

    ---
    tags:
      - Matérias
    security:
      - Bearer: []

    parameters:
      - in: body
        name: materia
        required: true
        schema:
          type: object
          required:
            - nome
          properties:
            nome:
              type: string
              minLength: 1
              maxLength: 100
              example: Banco de Dados
            descricao:
              type: string
              example: Estudo de SQL e modelo relacional

    responses:
      201:
        description: Matéria cadastrada.
        schema:
          type: object
          properties:
            id_materias:
              type: integer
              example: 1
            nome:
              type: string
              example: Banco de Dados
            descricao:
              type: string
              example: Estudo de SQL
            id_usuarios:
              type: integer
              example: 1
            data_criacao:
              type: string
              example: "Fri, 30 Oct 2026 12:11:43 GMT"
      400:
        description: Dados inválidos.
      401:
        description: Não autenticado.
    """
    dados = request.get_json(silent=True)
    materia = service.create(dados, g.id_usuario)
    return jsonify(materia.to_dict()), 201


def update(id_materias):
    """
    Atualiza uma matéria existente.

    ---
    tags:
      - Matérias
    security:
      - Bearer: []

    parameters:
      - in: path
        name: id_materias
        type: integer
        required: true
        description: Identificador da matéria.
      - in: body
        name: materia
        required: true
        schema:
          type: object
          required:
            - nome
          properties:
            nome:
              type: string
              minLength: 1
              maxLength: 100
              example: Programação
            descricao:
              type: string
              example: Estudos de Python e Flask

    responses:
      200:
        description: Matéria atualizada.
        schema:
          type: object
          properties:
            id_materias:
              type: integer
              example: 1
            nome:
              type: string
              example: Programação
            descricao:
              type: string
              example: Estudos de Python e Flask
            id_usuarios:
              type: integer
              example: 1
            data_criacao:
              type: string
              example: "Fri, 30 Oct 2026 12:11:43 GMT"
      400:
        description: Dados inválidos.
      401:
        description: Não autenticado.
      404:
        description: Matéria não encontrada.
    """
    dados = request.get_json(silent=True)
    materia = service.update(id_materias, dados, g.id_usuario)
    return jsonify(materia.to_dict()), 200


def get_by_id(id_materias):
    """
    Busca uma matéria pelo identificador.

    ---
    tags:
      - Matérias
    security:
      - Bearer: []

    parameters:
      - in: path
        name: id_materias
        type: integer
        required: true
        description: Identificador da matéria.

    responses:
      200:
        description: Matéria encontrada.
        schema:
          type: object
          properties:
            id_materias:
              type: integer
              example: 1
            nome:
              type: string
              example: Introdução à Administração
            descricao:
              type: string
              example: Fundamentos de administração
            id_usuarios:
              type: integer
              example: 1
            data_criacao:
              type: string
              example: "Fri, 30 Oct 2026 12:11:43 GMT"
      401:
        description: Não autenticado.
      404:
        description: Matéria não encontrada.
    """
    materia = service.get_by_id(id_materias, g.id_usuario)
    return jsonify(materia.to_dict())


def delete(id_materias):
    """
    Exclui uma matéria.

    ---
    tags:
      - Matérias
    security:
      - Bearer: []

    parameters:
      - in: path
        name: id_materias
        type: integer
        required: true
        description: Identificador da matéria.

    responses:
      204:
        description: Matéria excluída com sucesso.
      401:
        description: Não autenticado.
      404:
        description: Matéria não encontrada.
    """
    service.delete(id_materias, g.id_usuario)
    return "", 204
