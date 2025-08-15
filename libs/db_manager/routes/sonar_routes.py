import asyncio
from flask import Blueprint, request, jsonify
from ..db_utils import create_sonar, list_sonars, get_latest_sonar

sonar_bp = Blueprint("sonar", __name__, url_prefix="/sonar")

@sonar_bp.route("/", methods=["POST"])
async def post_sonar():
    try:
        payload = request.get_json() or {}
        result = await asyncio.to_thread(create_sonar, payload)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), getattr(e, "status_code", 400)

@sonar_bp.route("/", methods=["GET"])
async def list_all():
    data = await asyncio.to_thread(list_sonars)
    return jsonify(data), 200

@sonar_bp.route("/latest", methods=["GET"])
async def latest():
    try:
        result = await asyncio.to_thread(get_latest_sonar)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), getattr(e, "status_code", 400)
