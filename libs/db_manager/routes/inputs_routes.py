from flask import Blueprint, request, jsonify
from db_manager.models.inputs import Inputs
from db_manager import db

inputs_bp = Blueprint('inputs', __name__)

# Inputs routes
# Post route to add a new input
@inputs_bp.route('/post_input', methods=['POST'])
def post_input():
    try:
        data = request.get_json()
        new_input = Inputs(
            step_index=data['step_index'],
            direction=data['direction'],
            force=data['force'],
            s1=data['s1'],
            s2=data['s2'],
            s3=data['s3'],
            arm=data['arm']
        )
        db.session.add(new_input)
        db.session.commit()
        return jsonify({"message": "Input added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
# Get route to retrieve all inputs
@inputs_bp.route('/get_inputs', methods=['GET'])
def get_inputs():
    try:
        inputs = Inputs.query.all()
        return jsonify([input.__dict__ for input in inputs]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get route to retrieve a specific input by step_index
@inputs_bp.route('/get_input/<int:step_index>', methods=['GET'])
def get_input(step_index):
    try:
        input_data = Inputs.query.filter_by(step_index=step_index).first()
        if input_data:
            return jsonify(input_data.__dict__), 200
        else:
            return jsonify({"error": "Input not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get route to retrieve the latest input
@inputs_bp.route('/get_latest_input', methods=['GET'])
def get_latest_input():
    try:
        latest_input = Inputs.query.order_by(Inputs.id.desc()).first()
        if latest_input:
            return jsonify(latest_input.__dict__), 200
        else:
            return jsonify({"error": "No inputs found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    