from flask import Blueprint, request, jsonify
from db_manager.models.imu import IMU
from db_manager import db

imu_bp = Blueprint('imu', __name__)

# IMU routes
# Post route to add a new IMU data
@imu_bp.route('/post_imu', methods=['POST'])
def post_imu():
    try:
        data = request.get_json()
        new_imu = IMU(
            step_index=data['step_index'],
            X=data['X'],
            Y=data['Y'],
            Z=data['Z'],
            roll=data['roll'],
            pitch=data['pitch'],
            yaw=data['yaw']
        )
        db.session.add(new_imu)
        db.session.commit()
        return jsonify({"message": "IMU data added successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve all IMU data
@imu_bp.route('/get_imu', methods=['GET'])
def get_imu():
    try:
        imu_data = IMU.query.all()
        return jsonify([imu.__dict__ for imu in imu_data]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get route to retrieve a specific IMU data by step_index
@imu_bp.route('/get_imu/<int:step_index>', methods=['GET'])
def get_imu_by_step(step_index):
    try:
        imu_data = IMU.query.filter_by(step_index=step_index).first()
        if imu_data:
            return jsonify(imu_data.__dict__), 200
        else:
            return jsonify({"error": "IMU data not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
# Get route to retrieve the latest IMU data
@imu_bp.route('/get_latest_imu', methods=['GET'])
def get_latest_imu():
    try:
        latest_imu = IMU.query.order_by(IMU.id.desc()).first()
        if latest_imu:
            return jsonify(latest_imu.__dict__), 200
        else:
            return jsonify({"error": "No IMU data found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
