from datetime import date
from src.api_errors import ApiError
from . import entregas_repository as repository

def _titulo(dados):
    titulo = dados.get("titulo")
    if not isinstance(titulo, str) or not titulo.strip() or len(titulo.strip()) > 100:
        raise ApiError("titulo deve ter entre 1 e 100 caracteres")
    return titulo.strip()

def _data(dados):
    valor = dados.get("data_vencimento")
    if not isinstance(valor, str):
        raise ApiError("data_vencimento deve estar no formato AAAA-MM-DD")
    try:
        data = date.fromisoformat(valor)
    except ValueError:
        raise ApiError("data_vencimento inválida; use AAAA-MM-DD")
    if data.isoformat() != valor:
        raise ApiError("data_vencimento deve estar no formato AAAA-MM-DD")
    return valor

def _situacao(dados):
    valor = dados.get("situacao")
    if not isinstance(valor, str):
        raise ApiError("situacao deve ser pendente ou realizado")
    valor = valor.strip().lower()
    if valor not in ("pendente", "realizado"):
        raise ApiError("situacao deve ser pendente ou realizado")
    return valor

def _id_materia(dados, id_usuario):
    numero = dados.get("id_materias")
    if type(numero) is not int or numero <= 0:
        raise ApiError("id_materias deve ser um número inteiro positivo")
    if not repository.materia_do_usuario(numero, id_usuario):
        raise ApiError("Matéria não encontrada para este usuário", 404)
    return numero

def list_all(id_usuario):
    return repository.find_all(id_usuario)

def get_one(id_entrega, id_usuario):
    entrega = repository.find_by_id(id_entrega, id_usuario)
    if entrega is None:
        raise ApiError("Entrega não encontrada para este usuário", 404)
    return entrega

def cadastrar(dados, id_usuario):
    if not isinstance(dados, dict):
        raise ApiError("Envie um objeto JSON")
    titulo = _titulo(dados)
    data_vencimento = _data(dados)
    situacao = _situacao({"situacao": dados.get("situacao", "Pendente")})
    id_materia = _id_materia(dados, id_usuario)
    return repository.create(titulo, data_vencimento, situacao, id_materia)

def atualizar(id_entrega, id_usuario, dados):
    get_one(id_entrega, id_usuario)
    if not isinstance(dados, dict):
        raise ApiError("Envie um objeto JSON")
    campos = {}
    if "titulo" in dados:
        campos["titulo"] = _titulo(dados)
    if "data_vencimento" in dados:
        campos["data_vencimento"] = _data(dados)
    if "situacao" in dados:
        campos["situacao"] = _situacao(dados)
    if "id_materias" in dados:
        campos["id_materias"] = _id_materia(dados, id_usuario)
    if not campos:
        raise ApiError("Informe algum campo para atualizar")
    entrega_atualizada = repository.update(id_entrega, id_usuario, campos)

    if entrega_atualizada is None:
        raise ApiError("Entrega não encontrada para este usuário", 404)

    return entrega_atualizada

def excluir(id_entrega, id_usuario):
    get_one(id_entrega, id_usuario)

    if not repository.delete(id_entrega, id_usuario):
        raise ApiError("Entrega não encontrada para este usuário", 404)