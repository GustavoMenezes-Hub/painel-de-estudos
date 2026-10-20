from . import materias_repository as repository
from src.config import USUARIO_PADRAO_ID
from src.api_errors import ApiError

def list_all():
    return repository.find_all()

def create(dados):
    nome = (dados.get("nome") or "").strip()
    if not nome:
        raise ValueError("o campo 'nome' é obrigatório")
    descricao = dados.get("descricao", "").strip()
    return repository.create(nome, descricao, USUARIO_PADRAO_ID)

def get_by_id(id_materias):
    materia = repository.find_by_id(id_materias)
    if materia is None:
        raise ApiError("Matéria não encontrada.", 404)
    return materia