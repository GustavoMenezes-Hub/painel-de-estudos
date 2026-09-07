from flask import Flask
from src.materias.materias_route import materias_bp

app = Flask(__name__)
app.register_blueprint(materias_bp)

if __name__ == "__main__":
    app.run(port=3000, debug=True)