import asyncio
from flask import Blueprint, request, jsonify
from ..db_utils import create_battery, list_batteries, get_latest_battery

batteries_bp = Blueprint("batteries", __name__, url_prefix="/batteries")

@batteries_bp.route("/", methods=["POST"])
async def post_battery():
    try:
        data = request.get_json() or {}
        result = await asyncio.to_thread(create_battery, data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), getattr(e, "status_code", 400)

@batteries_bp.route("/", methods=["GET"])
async def get_batteries():
    data = await asyncio.to_thread(list_batteries)
    return jsonify(data), 200

@batteries_bp.route("/latest", methods=["GET"])
async def get_latest_battery_route():
    try:
        result = await asyncio.to_thread(get_latest_battery)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), getattr(e, "status_code", 400)
