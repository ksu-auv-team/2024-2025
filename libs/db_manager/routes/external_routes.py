from flask import Blueprint, request, jsonify
from db_manager.models.externals import ExternalDepth, ExternalPressure
from db_manager import db

external_bp = Blueprint('external', __name__)

# External Pressure routes
# Post route to add a new external pressure data
@external_bp.route('/post_external_pressure', methods=['POST'])
def post_external_pressure():
    try:
        data = request.get_json()
        new_external_pressure = ExternalPressure(
            step_index=data['step_index'],
            pressure=data['pressure']
        )
        db.session.add(new_external_pressure)
        db.session.commit()
        return jsonify({"message": "External pressure data added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve all external pressure data
@external_bp.route('/get_external_pressure', methods=['GET'])
def get_external_pressure():
    try:
        external_pressure_data = ExternalPressure.query.all()
        return jsonify([pressure.__dict__ for pressure in external_pressure_data]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve a specific external pressure data by step_index
@external_bp.route('/get_external_pressure/<int:step_index>', methods=['GET'])
def get_external_pressure_by_step(step_index):
    try:
        external_pressure_data = ExternalPressure.query.filter_by(step_index=step_index).first()
        if external_pressure_data:
            return jsonify(external_pressure_data.__dict__), 200
        else:
            return jsonify({"error": "External pressure data not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve the latest external pressure data
@external_bp.route('/get_latest_external_pressure', methods=['GET'])
def get_latest_external_pressure():
    try:
        latest_external_pressure = ExternalPressure.query.order_by(ExternalPressure.id.desc()).first()
        if latest_external_pressure:
            return jsonify(latest_external_pressure.__dict__), 200
        else:
            return jsonify({"error": "No external pressure data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# External Depth routes
# Post route to add a new external depth data
@external_bp.route('/post_external_depth', methods=['POST'])
def post_external_depth():
    try:
        data = request.get_json()
        new_external_depth = ExternalDepth(
            step_index=data['step_index'],
            depth=data['depth']
        )
        db.session.add(new_external_depth)
        db.session.commit()
        return jsonify({"message": "External depth data added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve all external depth data
@external_bp.route('/get_external_depth', methods=['GET'])
def get_external_depth():
    try:
        external_depth_data = ExternalDepth.query.all()
        return jsonify([depth.__dict__ for depth in external_depth_data]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve a specific external depth data by step_index
@external_bp.route('/get_external_depth/<int:step_index>', methods=['GET'])
def get_external_depth_by_step(step_index):
    try:
        external_depth_data = ExternalDepth.query.filter_by(step_index=step_index).first()
        if external_depth_data:
            return jsonify(external_depth_data.__dict__), 200
        else:
            return jsonify({"error": "External depth data not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve the latest external depth data
@external_bp.route('/get_latest_external_depth', methods=['GET'])
def get_latest_external_depth():
    try:
        latest_external_depth = ExternalDepth.query.order_by(ExternalDepth.id.desc()).first()
        if latest_external_depth:
            return jsonify(latest_external_depth.__dict__), 200
        else:
            return jsonify({"error": "No external depth data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
