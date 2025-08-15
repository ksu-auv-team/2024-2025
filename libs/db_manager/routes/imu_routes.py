import asyncio
from flask import Blueprint, request, jsonify
from ..db_utils import create_imu, list_imus, get_latest_imu

imu_bp = Blueprint('imu', __name__, url_prefix='/imu')

@imu_bp.route('/', methods=['POST'])
async def add_imu():
    data = request.get_json() or {}
    try:
        result = await asyncio.to_thread(create_imu, data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@imu_bp.route('/', methods=['GET'])
async def get_imus():
    data = await asyncio.to_thread(list_imus)
    return jsonify(data), 200

@imu_bp.route('/latest', methods=['GET'])
async def get_latest_imu_route():
    try:
        latest_imu = await asyncio.to_thread(get_latest_imu)
        return jsonify(latest_imu), 200 if latest_imu else 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
