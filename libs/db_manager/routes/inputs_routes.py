# libs/db_manager/routes/inputs_routes.py
from flask import Blueprint, request, jsonify
from ..logic import (
    create_input,
    list_inputs,
    get_latest_input,
    get_input_by_step,
    create_inputs_batch,
    Error,
    NotFound,
    DuplicateStep,
)

inputs_bp = Blueprint("inputs", __name__, url_prefix="/inputs")


@inputs_bp.route("/", methods=["POST"])
def post_input():
    try:
        result = create_input(request.json or {})
        return jsonify(result), 201
    except Error as e:
        code = getattr(e, "status_code", 400)
        return jsonify({"error": str(e)}), code


@inputs_bp.route("/batch", methods=["POST"])
def post_batch():
    try:
        if not isinstance(request.json, list):
            raise Error("Payload must be a JSON‐array")
        result = create_inputs_batch(request.json)
        return jsonify({"count": len(result), "items": result}), 201
    except Error as e:
        return jsonify({"error": str(e)}), getattr(e, "status_code", 400)


@inputs_bp.route("/", methods=["GET"])
def list_all():
    offset = request.args.get("offset", type=int, default=0)
    limit = request.args.get("limit", type=int, default=100)
    return jsonify(list_inputs(offset, limit)), 200


@inputs_bp.route("/latest", methods=["GET"])
def latest():
    try:
        return jsonify(get_latest_input()), 200
    except NotFound as e:
        return jsonify({"error": str(e)}), 404


@inputs_bp.route("/<int:step_index>", methods=["GET"])
def get_by_step(step_index):
    try:
        return jsonify(get_input_by_step(step_index)), 200
    except NotFound as e:
        return jsonify({"error": str(e)}), 404

    