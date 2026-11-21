import os
from dotenv import load_dotenv
from flask import Flask, request
from flasgger import Swagger
from werkzeug.exceptions import RequestEntityTooLarge

load_dotenv()

from src.error_handlers import registrar_error_handlers
from src.materias.materias_route import materias_bp
from src.usuarios.usuarios_route import usuarios_bp
from src.entregas.entregas_route import entregas_bp
from src.auth.auth_route import auth_bp
from src.auth.security import verificar_autenticacao
from src.api_errors import ApiError
from src.contrato_api import especificacao
from src.validacao import IdDaRota, id_postgres
from src.anotacoes.anotacoes_route import anotacoes_bp
from src.pomodoro.pomodoro_route import pomodoro_bp

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024
app.url_map.converters["int"] = IdDaRota

Swagger(app, template=especificacao())

chave = os.environ.get("SECRET_KEY")
if not chave:
    raise RuntimeError("Configure SECRET_KEY no arquivo .env local antes de iniciar o Flask")
app.config["SECRET_KEY"] = chave

app.register_blueprint(materias_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(entregas_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(anotacoes_bp)
app.register_blueprint(pomodoro_bp)

registrar_error_handlers(app)

def validar_tamanho_json():
    if not request.is_json:
        return
    limite = app.config["MAX_CONTENT_LENGTH"]
    tamanho = request.content_length
    if tamanho is None and request.environ.get("wsgi.input_terminated"):
        # Sem Content-Length, um byte extra distingue um corpo exato de um maior.
        # get_data mantém o corpo em cache para o get_json do controller.
        request.max_content_length = limite + 1
        tamanho = len(request.get_data())
    if tamanho is not None and tamanho > limite:
        raise RequestEntityTooLarge()

@app.before_request
def proteger_api():
    rotas_publicas = {
        ("POST", "/api/login"),
        ("POST", "/api/usuarios"),
    }

    if request.url_rule and request.path.startswith("/api/") and request.method != "OPTIONS":
        validar_tamanho_json()
        if (request.method, request.path) not in rotas_publicas:
            erro = verificar_autenticacao()
            if erro is not None:
                return erro
            for campo, valor in (request.view_args or {}).items():
                if not id_postgres(valor):
                    raise ApiError(f"{campo} deve ser inteiro positivo de até 2147483647.")

if __name__ == "__main__":
    app.run(port=3000, debug=os.environ.get("FLASK_DEBUG") == "1")
