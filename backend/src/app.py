import os
from dotenv import load_dotenv
from flask import Flask, request

load_dotenv()

from src.error_handlers import registrar_error_handlers
from src.materias.materias_route import materias_bp
from src.usuarios.usuarios_route import usuarios_bp
from src.entregas.entregas_route import entregas_bp
from src.auth.auth_route import auth_bp
from src.auth.security import verificar_autenticacao
from src.anotacoes.anotacoes_route import anotacoes_bp
from src.pomodoro.pomodoro_route import pomodoro_bp

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

app.register_blueprint(materias_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(entregas_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(anotacoes_bp)
app.register_blueprint(pomodoro_bp)

registrar_error_handlers(app)

@app.before_request
def proteger_api():
    rotas_publicas = {
        ("POST", "/api/login"),
        ("POST", "/api/usuarios"),
        ("GET", "/api/materias"),
        ("POST", "/api/materias"),
    }

    if request.path.startswith("/api/") and request.method != "OPTIONS":
        if (request.method, request.path) not in rotas_publicas:
            return verificar_autenticacao()

if __name__ == "__main__":
    app.run(port=3000, debug=True)
