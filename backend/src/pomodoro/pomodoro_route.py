from flask import Blueprint
from . import pomodoro_controller as controller

pomodoro_bp = Blueprint("pomodoro", __name__)

pomodoro_bp.route("/api/pomodoro", methods=["GET"])(controller.get_all)
pomodoro_bp.route("/api/pomodoro", methods=["POST"])(controller.create)
pomodoro_bp.route("/api/pomodoro/<int:id_pomodoro>", methods=["GET"])(controller.get_one)
pomodoro_bp.route("/api/pomodoro/<int:id_pomodoro>", methods=["PUT", "PATCH"])(controller.update)
pomodoro_bp.route("/api/pomodoro/<int:id_pomodoro>", methods=["DELETE"])(controller.delete)