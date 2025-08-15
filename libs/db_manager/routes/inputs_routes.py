import asyncio
from flask import Blueprint, request, jsonify
from ..db_utils import create_input, list_inputs, get_latest_input

inputs_bp = Blueprint("inputs", __name__, url_prefix="/inputs")

@inputs_bp.route("/", methods=["POST"])
async def post_input():
    try:
        data = request.get_json() or {}
        result = await asyncio.to_thread(create_input, data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@inputs_bp.route("/", methods=["GET"])
async def get_all_inputs():
    data = await asyncio.to_thread(list_inputs)
    return jsonify(data), 200

@inputs_bp.route("/latest", methods=["GET"])
async def get_latest():
    result = await asyncio.to_thread(get_latest_input)
    return jsonify(result or {"error": "No inputs found"}), 200
