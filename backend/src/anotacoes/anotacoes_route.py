from flask import Blueprint
from . import anotacoes_controller as controller

anotacoes_bp = Blueprint("anotacoes", __name__)

anotacoes_bp.route("/api/anotacoes", methods=["GET"])(controller.get_all)
anotacoes_bp.route("/api/anotacoes", methods=["POST"])(controller.create)
anotacoes_bp.route("/api/anotacoes/<int:id_anotacoes>", methods=["GET"])(controller.get_one)
anotacoes_bp.route("/api/anotacoes/<int:id_anotacoes>", methods=["PUT", "PATCH"])(controller.update)
anotacoes_bp.route("/api/anotacoes/<int:id_anotacoes>", methods=["DELETE"])(controller.delete)