from flask import Blueprint, request, jsonify
from db_manager.models.batteries import Batteries
from db_manager import db

batteries_bp = Blueprint('inputs', __name__)

# Batteries routes
# Post route to add a new battery data
@batteries_bp.route('/post_battery', methods=['POST'])
def post_battery():
    try:
        data = request.get_json()
        new_battery = Batteries(
            step_index=data['step_index'],
            voltage1=data['voltage1'],
            voltage2=data['voltage2'],
            voltage3=data['voltage3'],
            current1=data['current1'],
            current2=data['current2'],
            current3=data['current3'],
            temperature1=data['temperature1'],
            temperature2=data['temperature2'],
            temperature3=data['temperature3']
        )
        db.session.add(new_battery)
        db.session.commit()
        return jsonify({"message": "Battery data added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve all battery data
@batteries_bp.route('/get_battery', methods=['GET'])
def get_battery():
    try:
        battery_data = Batteries.query.all()
        return jsonify([battery.__dict__ for battery in battery_data]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get route to retrieve a specific battery data by step_index
@batteries_bp.route('/get_battery/<int:step_index>', methods=['GET'])
def get_battery_by_step(step_index):
    try:
        battery_data = Batteries.query.filter_by(step_index=step_index).first()
        if battery_data:
            return jsonify(battery_data.__dict__), 200
        else:
            return jsonify({"error": "Battery data not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get route to retrieve the latest battery data
@batteries_bp.route('/get_latest_battery', methods=['GET'])
def get_latest_battery():
    try:
        latest_battery = Batteries.query.order_by(Batteries.id.desc()).first()
        if latest_battery:
            return jsonify(latest_battery.__dict__), 200
        else:
            return jsonify({"error": "No battery data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
