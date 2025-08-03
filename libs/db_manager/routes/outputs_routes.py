from flask import Blueprint, request, jsonify
from db_manager.models.outputs import Outputs
from db_manager import db

outputs_bp = Blueprint('outputs', __name__)

# Outputs routes
# Post route to add a new output
@outputs_bp.route('/post_output', methods=['POST'])
def post_output():
    try:
        data = request.get_json()
        new_output = Outputs(
            step_index=data['step_index'],
            direction=data['direction'],
            force=data['force'],
            M1=data['M1'],
            M2=data['M2'],
            M3=data['M3'],
            M4=data['M4'],
            M5=data['M5'],
            M6=data['M6'],
            M7=data['M7'],
            M8=data['M8'],
            S1=data['S1'],
            S2=data['S2'],
            S3=data['S3'],
            arm=data['arm']
        )
        db.session.add(new_output)
        db.session.commit()
        return jsonify({"message": "Output added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve all outputs
@outputs_bp.route('/get_outputs', methods=['GET'])
def get_outputs():
    try:
        outputs = Outputs.query.all()
        return jsonify([output.__dict__ for output in outputs]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve a specific output by step_index
@outputs_bp.route('/get_output/<int:step_index>', methods=['GET'])
def get_output(step_index):
    try:
        output_data = Outputs.query.filter_by(step_index=step_index).first()
        if output_data:
            return jsonify(output_data.__dict__), 200
        else:
            return jsonify({"error": "Output not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve the latest output
@outputs_bp.route('/get_latest_output', methods=['GET'])
def get_latest_output():
    try:
        latest_output = Outputs.query.order_by(Outputs.id.desc()).first()
        if latest_output:
            return jsonify(latest_output.__dict__), 200
        else:
            return jsonify({"error": "No outputs found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
