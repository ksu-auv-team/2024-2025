from flask import Blueprint, request, jsonify
from ..db_utils import create_imu, list_imus, get_latest_imu

imu_bp = Blueprint('imu', __name__)

@imu_bp.route('/imu', methods=['POST'])
def add_imu():
    data = request.json
    try:
        result = create_imu(data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@imu_bp.route('/imu', methods=['GET'])
def get_imus():
    return jsonify(list_imus()), 200

@imu_bp.route('/imu/latest', methods=['GET'])
def get_latest_imu_route():
    try:
        latest_imu = get_latest_imu()
        return jsonify(latest_imu), 200 if latest_imu else 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500