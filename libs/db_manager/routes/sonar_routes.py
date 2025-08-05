from flask import Blueprint, request, jsonify
from ..db_utils import create_sonar, list_sonars, get_latest_sonar

sonar_bp = Blueprint("sonar", __name__, url_prefix="/sonar")

@sonar_bp.route("/", methods=["POST"])
def post_sonar():
    try:
        return jsonify(create_sonar(request.json or {})), 201
    except Exception as e:
        return jsonify({"error": str(e)}), getattr(e, "status_code", 400)
    
@sonar_bp.route("/", methods=["GET"])
def list_all():
    return jsonify(list_sonars()), 200

@sonar_bp.route("/latest", methods=["GET"])
def latest():
    try:
        return jsonify(get_latest_sonar()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), getattr(e, "status_code", 400)