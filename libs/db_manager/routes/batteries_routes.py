from flask import Blueprint, request, jsonify
from ..db_utils import create_battery, list_batteries, get_latest_battery

batteries_bp = Blueprint("batteries", __name__, url_prefix="/batteries")

@batteries_bp.route("/", methods=["POST"])
def post_battery():
    try:
        return jsonify(create_battery(request.json or {})), 201
    except Exception as e:
        return jsonify({"error": str(e)}), getattr(e, "status_code", 400)

@batteries_bp.route("/", methods=["GET"])
def get_batteries():
    return jsonify(list_batteries()), 200

@batteries_bp.route("/latest", methods=["GET"])
def get_latest_battery_route():
    try:
        return jsonify(get_latest_battery()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), getattr(e, "status_code", 400)