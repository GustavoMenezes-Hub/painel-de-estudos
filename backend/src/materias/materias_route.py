from flask import Blueprint
from . import materias_controller as controller

materias_bp = Blueprint("materias", __name__)
materias_bp.route("/api/materias", methods=["GET"])(controller.get_all)