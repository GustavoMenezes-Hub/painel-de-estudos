from flask import Blueprint
from . import entregas_controller as controller

entregas_bp = Blueprint("entregas", __name__)
entregas_bp.route("/api/entregas", methods=["GET"])(controller.get_all)
entregas_bp.route("/api/entregas", methods=["POST"])(controller.create)
entregas_bp.route("/api/entregas/<int:id_entrega>", methods=["GET"])(controller.get_one)
entregas_bp.route("/api/entregas/<int:id_entrega>", methods=["PUT", "PATCH"])(controller.update)
entregas_bp.route("/api/entregas/<int:id_entrega>", methods=["DELETE"])(controller.delete)