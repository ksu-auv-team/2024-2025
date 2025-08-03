from flask import Blueprint, request, jsonify
from db_manager.models.sonar import Sonar
from db_manager import db

sonar_bp = Blueprint('sonar', __name__)

# Sonar routes
# Post route to add a new sonar data
@sonar_bp.route('/post_sonar', methods=['POST'])
def post_sonar():
    try:
        data = request.get_json()
        new_sonar = Sonar(
            step_index=data['step_index'],
            distance=data['distance'],
            angle=data['angle']
        )
        db.session.add(new_sonar)
        db.session.commit()
        return jsonify({"message": "Sonar data added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve all sonar data
@sonar_bp.route('/get_sonar', methods=['GET'])
def get_sonar():
    try:
        sonar_data = Sonar.query.all()
        return jsonify([sonar.__dict__ for sonar in sonar_data]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve a specific sonar data by step_index
@sonar_bp.route('/get_sonar/<int:step_index>', methods=['GET'])
def get_sonar_by_step(step_index):
    try:
        sonar_data = Sonar.query.filter_by(step_index=step_index).first()
        if sonar_data:
            return jsonify(sonar_data.__dict__), 200
        else:
            return jsonify({"error": "Sonar data not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve the latest sonar data
@sonar_bp.route('/get_latest_sonar', methods=['GET'])
def get_latest_sonar():
    try:
        latest_sonar = Sonar.query.order_by(Sonar.id.desc()).first()
        if latest_sonar:
            return jsonify(latest_sonar.__dict__), 200
        else:
            return jsonify({"error": "No sonar data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
