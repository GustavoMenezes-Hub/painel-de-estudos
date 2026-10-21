from flask import Blueprint
from . import materias_controller as controller

materias_bp = Blueprint("materias", __name__)
materias_bp.route("/api/materias", methods=["GET"])(controller.get_all)
materias_bp.route("/api/materias", methods=["POST"])(controller.create)
materias_bp.route("/api/materias/<int:id_materias>", methods=["GET"])(controller.get_by_id)
materias_bp.route("/api/materias/<int:id_materias>", methods=["PUT"])(controller.update)
materias_bp.route("/api/materias/<int:id_materias>", methods=["DELETE"])(controller.delete)