from flask import Response, g, request, jsonify
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
 
 
def upload_imagem(id_anotacoes):
    """
    Envia a imagem de uma anotação (por exemplo, a foto do caderno).
 
    ---
    tags:
      - Anotações
    security:
      - Bearer: []
    consumes:
      - multipart/form-data
    parameters:
      - in: path
        name: id_anotacoes
        type: integer
        required: true
        description: Identificador da anotação.
      - in: formData
        name: arquivo
        type: file
        required: true
        description: Imagem PNG, JPEG ou WEBP de até 5 MB.
    responses:
      201:
        description: Imagem salva.
        schema:
          type: object
          properties:
            mensagem:
              type: string
              example: Imagem enviada com sucesso.
      400:
        description: Arquivo ausente, vazio ou em formato não suportado.
      401:
        description: Não autenticado.
      404:
        description: Anotação não encontrada para este usuário.
      413:
        description: Imagem maior que o limite permitido.
    """
    arquivo = request.files.get("arquivo")
    AnotacoesService.enviar_imagem(id_anotacoes, arquivo, g.id_usuario)
    return jsonify({"mensagem": "Imagem enviada com sucesso."}), 201
 
 
def get_imagem(id_anotacoes):
    """
    Baixa a imagem de uma anotação.
 
    ---
    tags:
      - Anotações
    security:
      - Bearer: []
    produces:
      - image/png
      - image/jpeg
      - image/webp
    parameters:
      - in: path
        name: id_anotacoes
        type: integer
        required: true
        description: Identificador da anotação.
    responses:
      200:
        description: Arquivo de imagem.
        schema:
          type: file
      401:
        description: Não autenticado.
      404:
        description: Anotação ou imagem não encontrada para este usuário.
    """
    linha = AnotacoesService.obter_imagem(id_anotacoes, g.id_usuario)
    return Response(
        bytes(linha["imagem"]),
        mimetype=linha["imagem_tipo"],
        headers={
            "Content-Disposition": f'inline; filename="{linha["imagem_nome"]}"',
            "X-Content-Type-Options": "nosniff",
        },
    )