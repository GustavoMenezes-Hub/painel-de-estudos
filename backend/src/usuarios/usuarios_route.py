from flask import Blueprint
from . import usuarios_controller as controller

usuarios_bp = Blueprint("usuarios", __name__)

usuarios_bp.route("/api/usuarios", methods=["GET"])(controller.get_all)
usuarios_bp.route("/api/usuarios", methods=["POST"])(controller.create)
usuarios_bp.route("/api/usuarios/me", methods=["GET"])(controller.me)
usuarios_bp.route("/api/usuarios/<int:id_usuario>", methods=["GET"])(controller.get_one)
usuarios_bp.route("/api/usuarios/<int:id_usuario>", methods=["PUT", "PATCH"])(controller.update)
usuarios_bp.route("/api/usuarios/<int:id_usuario>", methods=["DELETE"])(controller.delete)
