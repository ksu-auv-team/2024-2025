from flask import Blueprint, request, jsonify
from ..db_utils import create_output, list_outputs, get_latest_output

outputs_bp = Blueprint("outputs", __name__, url_prefix="/outputs")

@outputs_bp.route("/", methods=["POST"])
def post_output():
    try:
        return jsonify(create_output(request.json or {})), 201
    except Exception as e:
        return jsonify({"error": str(e)}), getattr(e, "status_code", 400)


@outputs_bp.route("/", methods=["GET"])
def list_all():
    return jsonify(list_outputs()), 200

@outputs_bp.route("/latest", methods=["GET"])
def latest():
    try:
        return jsonify(get_latest_output()), 200
    except Exception as e:
        return jsonify({"error": str(e)}), getattr(e, "status_code", 400)