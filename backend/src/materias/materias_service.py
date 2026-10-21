from . import materias_repository as repository
from src.config import USUARIO_PADRAO_ID
from src.api_errors import ApiError

def list_all():
    return repository.find_all()

def _validar_dados(dados):
    if not dados:
        raise ApiError("Corpo da requisição inválido.", 400)
    nome = (dados.get("nome") or "").strip()
    if not nome:
        raise ApiError("O campo 'nome' é obrigatório.", 400)
    descricao = (dados.get("descricao") or "").strip() or None
    return nome, descricao

def create(dados):
    nome, descricao = _validar_dados(dados)
    return repository.create(nome, descricao, USUARIO_PADRAO_ID)

def update(id_materias, dados):
    nome, descricao = _validar_dados(dados)
    materia = repository.update(id_materias, nome, descricao)
    if materia is None:
        raise ApiError("Matéria não encontrada.", 404)
    return materia

def get_by_id(id_materias):
    materia = repository.find_by_id(id_materias)
    if materia is None:
        raise ApiError("Matéria não encontrada.", 404)
    return materia