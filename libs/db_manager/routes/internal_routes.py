from flask import Blueprint, request, jsonify
from db_manager.models.internals import InternalTemperature, InternalHumidity, InternalPressure
from db_manager import db

internal_bp = Blueprint('internal', __name__)

# Internal Humidity routes
# Post route to add a new internal humidity data
@internal_bp.route('/post_internal_humidity', methods=['POST'])
def post_internal_humidity():
    try:
        data = request.get_json()
        new_internal_humidity = InternalHumidity(
            step_index=data['step_index'],
            humidity=data['humidity']
        )
        db.session.add(new_internal_humidity)
        db.session.commit()
        return jsonify({"message": "Internal humidity data added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve all internal humidity data
@internal_bp.route('/get_internal_humidity', methods=['GET'])
def get_internal_humidity():
    try:
        internal_humidity_data = InternalHumidity.query.all()
        return jsonify([humidity.__dict__ for humidity in internal_humidity_data]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve a specific internal humidity data by step_index
@internal_bp.route('/get_internal_humidity/<int:step_index>', methods=['GET'])
def get_internal_humidity_by_step(step_index):
    try:
        internal_humidity_data = InternalHumidity.query.filter_by(step_index=step_index).first()
        if internal_humidity_data:
            return jsonify(internal_humidity_data.__dict__), 200
        else:
            return jsonify({"error": "Internal humidity data not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve the latest internal humidity data
@internal_bp.route('/get_latest_internal_humidity', methods=['GET'])
def get_latest_internal_humidity():
    try:
        latest_internal_humidity = InternalHumidity.query.order_by(InternalHumidity.id.desc()).first()
        if latest_internal_humidity:
            return jsonify(latest_internal_humidity.__dict__), 200
        else:
            return jsonify({"error": "No internal humidity data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Internal Pressure routes
# Post route to add a new internal pressure data
@internal_bp.route('/post_internal_pressure', methods=['POST'])
def post_internal_pressure():
    try:
        data = request.get_json()
        new_internal_pressure = InternalPressure(
            step_index=data['step_index'],
            pressure=data['pressure']
        )
        db.session.add(new_internal_pressure)
        db.session.commit()
        return jsonify({"message": "Internal pressure data added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve all internal pressure data
@internal_bp.route('/get_internal_pressure', methods=['GET'])
def get_internal_pressure():
    try:
        internal_pressure_data = InternalPressure.query.all()
        return jsonify([pressure.__dict__ for pressure in internal_pressure_data]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve a specific internal pressure data by step_index
@internal_bp.route('/get_internal_pressure/<int:step_index>', methods=['GET'])
def get_internal_pressure_by_step(step_index):
    try:
        internal_pressure_data = InternalPressure.query.filter_by(step_index=step_index).first()
        if internal_pressure_data:
            return jsonify(internal_pressure_data.__dict__), 200
        else:
            return jsonify({"error": "Internal pressure data not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve the latest internal pressure data
@internal_bp.route('/get_latest_internal_pressure', methods=['GET'])
def get_latest_internal_pressure():
    try:
        latest_internal_pressure = InternalPressure.query.order_by(InternalPressure.id.desc()).first()
        if latest_internal_pressure:
            return jsonify(latest_internal_pressure.__dict__), 200
        else:
            return jsonify({"error": "No internal pressure data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
