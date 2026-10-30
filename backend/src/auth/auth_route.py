from flask import Blueprint
from . import auth_controller as controller

auth_bp = Blueprint("auth", __name__)
auth_bp.route("/api/login", methods=["POST"])(controller.login)