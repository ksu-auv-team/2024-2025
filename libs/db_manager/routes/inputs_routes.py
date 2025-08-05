from flask import Blueprint, request, jsonify
from ..db_utils import create_input, list_inputs, get_latest_input

inputs_bp = Blueprint("inputs", __name__, url_prefix="/inputs")

@inputs_bp.route("/", methods=["POST"])
def post_input():
    try:
        data = request.get_json()
        return jsonify(create_input(data)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@inputs_bp.route("/", methods=["GET"])
def get_all_inputs():
    return jsonify(list_inputs()), 200

@inputs_bp.route("/latest", methods=["GET"])
def get_latest():
    result = get_latest_input()
    return jsonify(result or {"error": "No inputs found"}), 200
