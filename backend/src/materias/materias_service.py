from . import materias_repository as repository
from src.api_errors import ApiError

def list_all(id_usuario):
    return repository.find_all(id_usuario)

def _validar_dados(dados):
    if not isinstance(dados, dict):
        raise ApiError("Corpo da requisição inválido.", 400)
    nome = dados.get("nome")
    descricao = dados.get("descricao")
    if not isinstance(nome, str) or not nome.strip() or len(nome.strip()) > 100:
        raise ApiError("O campo 'nome' deve ter entre 1 e 100 caracteres.", 400)
    if descricao is not None and not isinstance(descricao, str):
        raise ApiError("O campo 'descricao' deve ser texto.", 400)
    descricao = descricao.strip() or None if descricao is not None else None
    return nome.strip(), descricao

def create(dados, id_usuario):
    nome, descricao = _validar_dados(dados)
    return repository.create(nome, descricao, id_usuario)

def update(id_materias, dados, id_usuario):
    nome, descricao = _validar_dados(dados)
    materia = repository.update(id_materias, nome, descricao, id_usuario)
    if materia is None:
        raise ApiError("Matéria não encontrada para este usuário.", 404)
    return materia

def get_by_id(id_materias, id_usuario):
    materia = repository.find_by_id(id_materias, id_usuario)
    if materia is None:
        raise ApiError("Matéria não encontrada para este usuário.", 404)
    return materia

def delete(id_materias, id_usuario):
    if not repository.delete(id_materias, id_usuario):
        raise ApiError("Matéria não encontrada para este usuário.", 404)