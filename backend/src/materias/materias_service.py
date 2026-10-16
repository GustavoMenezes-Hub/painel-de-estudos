from . import materias_repository as repository
from src.config import USUARIO_PADRAO_ID

def list_all():
    return repository.find_all()

def create(dados):
    nome = (dados.get("nome") or "").strip()
    if not nome:
        raise ValueError("o campo 'nome' é obrigatório")
    descricao = dados.get("descricao", "").strip()
    return repository.create(nome, descricao, USUARIO_PADRAO_ID)