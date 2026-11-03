from werkzeug.security import check_password_hash
from src.api_errors import ApiError
from src.usuarios import usuarios_repository as usuarios
from .security import gerar_token, DURACAO_TOKEN_SEGUNDOS

def entrar(dados):
    if not isinstance(dados, dict):
        raise ApiError("Envie um objeto JSON com email e senha")
    email = dados.get("email")
    senha = dados.get("senha")
    if not isinstance(email, str) or not isinstance(senha, str) or not email.strip() or not senha:
        raise ApiError("Email e senha são obrigatórios")
    usuario = usuarios.find_by_email(email.strip().lower())
    if not usuario or not usuario.get("senha_hash") or not check_password_hash(usuario["senha_hash"], senha):
        raise ApiError("Email ou senha inválidos", 401)
    return {
        "access_token": gerar_token(usuario["id_usuarios"]),
        "token_type": "Bearer",
        "expires_in": DURACAO_TOKEN_SEGUNDOS,
        "usuario": {
            "id_usuarios": usuario["id_usuarios"],
            "nome": usuario["nome"],
            "email": usuario["email"],
        },
    }