# DBHandler.py
from flask import Flask, request, jsonify, url_for, render_template
from modules.DBSupport.db import engine, async_session
from modules.DBSupport.models import Base, Inputs, Outputs, Sonar, Batteries, IMU, Sensors
# from modules.CameraPackageSupport import WebCamService, routes
# from modules.CameraPackageSupport.camera_1 import zedcam_blueprint as camera_1
# from modules.CameraPackageSupport.camera_2 import anchor_blueprint as camera_2
import asyncio
import argparse
import os

app = Flask(__name__)

# This must run AFTER all models are imported
async def init_models():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

# Call it before Flask starts
asyncio.run(init_models())

# app.register_blueprint(camera_1)
# app.register_blueprint(camera_2)
# app.register_blueprint(routes.get_blueprint())

# ---------------------- Inputs ----------------------
@app.route('/inputs', methods=['POST'])
async def create_input():
    data = request.json
    if data is None or not isinstance(data, dict):
        data = {
            'x': 0.0,
            'y': 0.0,
            'z': 0.0,
            'roll': 0.0,
            'pitch': 0.0,
            'yaw': 0.0,
            's1': 0.0,
            's2': 0.0,
            's3': 0.0,
            'arm': 0,
        }
    async with async_session() as session:
        new_input = Inputs(**data)
        session.add(new_input)
        await session.commit()
        await session.refresh(new_input)
        return jsonify(data), 201


@app.route('/inputs', methods=['GET'])
async def get_inputs():
    async with async_session() as session:
        result = await session.execute(Inputs.__table__.select())
        return jsonify([dict(row._mapping) for row in result.fetchall()])


# ---------------------- Outputs ----------------------
@app.route('/outputs', methods=['POST'])
async def create_output():
    data = request.json
    if data is None or not isinstance(data, dict):
        data = {
            'm1': 0.0,
            'm2': 0.0,
            'm3': 0.0,
            'm4': 0.0,
            'm5': 0.0,
            'm6': 0.0,
            'm7': 0.0,
            'm8': 0.0,
            's1': 0.0,
            's2': 0.0,
            's3': 0.0,
        }
    async with async_session() as session:
        new_output = Outputs(**data)
        session.add(new_output)
        await session.commit()
        await session.refresh(new_output)
        return jsonify(data), 201


@app.route('/outputs', methods=['GET'])
async def get_outputs():
    async with async_session() as session:
        result = await session.execute(Outputs.__table__.select())
        return jsonify([dict(row._mapping) for row in result.fetchall()])


# ---------------------- Sonar ----------------------
@app.route('/sonar', methods=['POST'])
async def create_sonar():
    data = request.json
    if data is None or not isinstance(data, dict):
        data = {
            'distance': 0.0,
            'angle': 0.0,
        }
    async with async_session() as session:
        new_sonar = Sonar(**data)
        session.add(new_sonar)
        await session.commit()
        await session.refresh(new_sonar)
        return jsonify(data), 201


@app.route('/sonar', methods=['GET'])
async def get_sonar():
    async with async_session() as session:
        result = await session.execute(Sonar.__table__.select())
        return jsonify([dict(row._mapping) for row in result.fetchall()])


# ---------------------- Batteries ----------------------
@app.route('/batteries', methods=['POST'])
async def create_battery():
    data = request.json
    if data is None or not isinstance(data, dict):
        data = {
            'voltage1': 0.0,
            'current1': 0.0,
            'voltage2': 0.0,
            'current2': 0.0,
            'voltage3': 0.0,
            'current3': 0.0,
        }
    async with async_session() as session:
        new_battery = Batteries(**data)
        session.add(new_battery)
        await session.commit()
        await session.refresh(new_battery)
        return jsonify(data), 201


@app.route('/batteries', methods=['GET'])
async def get_batteries():
    async with async_session() as session:
        result = await session.execute(Batteries.__table__.select())
        return jsonify([dict(row._mapping) for row in result.fetchall()])


# ---------------------- IMU ----------------------
@app.route('/imu', methods=['POST'])
async def create_imu():
    data = request.json
    if data is None or not isinstance(data, dict):
        data = {
            'acceleration_x': 0.0,
            'acceleration_y': 0.0,
            'acceleration_z': 0.0,
            'gyro_x': 0.0,
            'gyro_y': 0.0,
            'gyro_z': 0.0,
            'magnetometer_x': 0.0,
            'magnetometer_y': 0.0,
            'magnetometer_z': 0.0,
        }
    async with async_session() as session:
        new_imu = IMU(**data)
        session.add(new_imu)
        await session.commit()
        await session.refresh(new_imu)
        return jsonify(data), 201


@app.route('/imu', methods=['GET'])
async def get_imu():
    async with async_session() as session:
        result = await session.execute(IMU.__table__.select())
        return jsonify([dict(row._mapping) for row in result.fetchall()])


# ---------------------- Sensors ----------------------
@app.route('/sensors', methods=['POST'])
async def create_sensor():
    data = request.json
    if data is None or not isinstance(data, dict):
        data = {
            'temperature': 0.0,
            'humidity': 0.0,
            'pressure': 0.0,
            'depth': 0.0,
        }
    async with async_session() as session:
        new_sensor = Sensors(**data)
        session.add(new_sensor)
        await session.commit()
        await session.refresh(new_sensor)
        return jsonify(data), 201


@app.route('/sensors', methods=['GET'])
async def get_sensors():
    async with async_session() as session:
        result = await session.execute(Sensors.__table__.select())
        return jsonify([dict(row._mapping) for row in result.fetchall()])

# ========================= Camera Routes =========================
# Opening cameras through flask based on configuration

# This will be set in main based on argparse
# ENABLED_CAMERAS = []

# @app.route('/video_0')
# def video_0():
#     if "0" not in ENABLED_CAMERAS:
#         return jsonify({"error": "Camera 0 is disabled"}), 403
#     video_url = url_for('camera_1.video_0')
#     response = app.test_client().get(video_url)
#     return response.data

# @app.route('/video_1')
# def video_1():
#     if "1" not in ENABLED_CAMERAS:
#         return jsonify({"error": "Camera 1 is disabled"}), 403
#     video_url = url_for('camera_2.video_1')
#     response = app.test_client().get(video_url)
#     return response.data

# ========================= Main Application =========================
@app.route('/')
def index():
    return render_template('index.html')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask DBHandler application.')
    parser.add_argument('--host', type=str, default='localhost', help='Host for the Flask server')
    parser.add_argument('--port', type=int, default=5000, help='Port for the Flask server')
    parser.add_argument('--debug', action='store_true', help='Run Flask server in debug mode')
    parser.add_argument('--both-cameras', action='store_true', help='Enable both cameras')
    parser.add_argument('--camera-0', action='store_true', help='Enable camera 0')
    parser.add_argument('--camera-1', action='store_true', help='Enable camera 1')
    args = parser.parse_args()
    
    if args.both_cameras:
        ENABLED_CAMERAS = ["0", "1"]
    elif args.camera_0:
        ENABLED_CAMERAS = ["0"]
    elif args.camera_1:
        ENABLED_CAMERAS = ["1"]
    else:
        ENABLED_CAMERAS = []
    
    app.run(debug=True)
