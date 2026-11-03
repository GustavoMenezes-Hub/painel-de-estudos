from werkzeug.security import generate_password_hash
from src.api_errors import ApiError
from . import usuarios_repository as repository

def _texto(dados, campo, maximo=100):
    valor = dados.get(campo)
    if not isinstance(valor, str) or not valor.strip():
        raise ApiError(f"{campo} deve ser um texto não vazio")
    valor = valor.strip()
    if len(valor) > maximo:
        raise ApiError(f"{campo} não pode ultrapassar {maximo} caracteres")
    return valor

def _senha(dados):
    senha = dados.get("senha")
    if not isinstance(senha, str) or len(senha) < 8:
        raise ApiError("senha deve ter pelo menos 8 caracteres")
    return senha

def _email(dados):
    email = _texto(dados, "email").lower()
    if "@" not in email or "." not in email.split("@")[-1] or " " in email:
        raise ApiError("email inválido")
    return email

def list_all():
    return repository.find_all()

def get_one(id_usuario, id_logado):
    if id_usuario != id_logado:
        raise ApiError("Você só pode consultar seus próprios dados", 403)
    usuario = repository.find_by_id(id_usuario)
    if usuario is None:
        raise ApiError("Usuário não encontrado", 404)
    return usuario

def cadastrar(dados):
    if not isinstance(dados, dict):
        raise ApiError("Envie um objeto JSON")
    nome = _texto(dados, "nome")
    email = _email(dados)
    senha = _senha(dados)
    if repository.find_by_email(email):
        raise ApiError("Email já cadastrado", 409)
    return repository.create(nome, email, generate_password_hash(senha))

def atualizar(id_usuario, id_logado, dados):
    get_one(id_usuario, id_logado)
    if not isinstance(dados, dict):
        raise ApiError("Envie um objeto JSON")
    campos = {}
    if "nome" in dados:
        campos["nome"] = _texto(dados, "nome")
    if "email" in dados:
        novo_email = _email(dados)
        existente = repository.find_by_email(novo_email)
        if existente and existente["id_usuarios"] != id_usuario:
            raise ApiError("Email já cadastrado", 409)
        campos["email"] = novo_email
    if "senha" in dados:
        campos["senha_hash"] = generate_password_hash(_senha(dados))
    if not campos:
        raise ApiError("Informe nome, email ou senha para atualizar")
    usuario_atualizado = repository.update(id_usuario, campos)
    if usuario_atualizado is None:
        raise ApiError("Usuário não encontrado", 404)
    return usuario_atualizado

def excluir(id_usuario, id_logado):
    get_one(id_usuario, id_logado)
    if not repository.delete(id_usuario):
        raise ApiError("Usuário não encontrado", 404)