import asyncio
from flask import Blueprint, request, jsonify
from ..db_utils import create_output, list_outputs, get_latest_output

outputs_bp = Blueprint("outputs", __name__, url_prefix="/outputs")

@outputs_bp.route("/", methods=["POST"])
async def post_output():
    try:
        payload = request.get_json() or {}
        result = await asyncio.to_thread(create_output, payload)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), getattr(e, "status_code", 400)

@outputs_bp.route("/", methods=["GET"])
async def list_all():
    data = await asyncio.to_thread(list_outputs)
    return jsonify(data), 200

@outputs_bp.route("/latest", methods=["GET"])
async def latest():
    try:
        result = await asyncio.to_thread(get_latest_output)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), getattr(e, "status_code", 400)
