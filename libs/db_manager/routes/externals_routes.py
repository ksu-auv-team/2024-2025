from flask import Blueprint, request, jsonify
from ..db_utils import create_external_pressure, list_external_pressures, get_latest_external_pressure
from ..db_utils import create_external_depth, list_external_depths, get_latest_external_depth

externals_bp = Blueprint('externals', __name__)

@externals_bp.route('/external_pressure', methods=['POST'])
def add_external_pressure():
    data = request.json
    try:
        result = create_external_pressure(data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@externals_bp.route('/external_pressure', methods=['GET'])
def get_external_pressures():
    try:
        pressures = list_external_pressures()
        return jsonify(pressures), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@externals_bp.route('/external_pressure/latest', methods=['GET'])
def get_latest_external_pressure_route():
    try:
        latest_pressure = get_latest_external_pressure()
        return jsonify(latest_pressure), 200 if latest_pressure else 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@externals_bp.route('/external_depth', methods=['POST'])
def add_external_depth():
    data = request.json
    try:
        result = create_external_depth(data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@externals_bp.route('/external_depth', methods=['GET'])
def get_external_depths():
    try:
        depths = list_external_depths()
        return jsonify(depths), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@externals_bp.route('/external_depth/latest', methods=['GET'])
def get_latest_external_depth_route():
    try:
        latest_depth = get_latest_external_depth()
        return jsonify(latest_depth), 200 if latest_depth else 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500