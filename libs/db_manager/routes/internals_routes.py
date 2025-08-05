from flask import Blueprint, request, jsonify
from ..db_utils import (
    create_internal_temperature,
    list_internal_temperatures,
    get_latest_internal_temperature,
    create_internal_humidity,
    list_internal_humidities,
    get_latest_internal_humidity,
    create_internal_pressure,
    list_internal_pressures,
    get_latest_internal_pressure
)

internals_bp = Blueprint('internals', __name__)

@internals_bp.route('/internal_temperature', methods=['POST'])
def add_internal_temperature():
    data = request.json
    try:
        result = create_internal_temperature(data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@internals_bp.route('/internal_temperature', methods=['GET'])
def get_internal_temperatures():
    try:
        temperatures = list_internal_temperatures()
        return jsonify(temperatures), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@internals_bp.route('/internal_temperature/latest', methods=['GET'])
def get_latest_internal_temperature():
    try:
        temperature = get_latest_internal_temperature()
        return jsonify(temperature), 200 if temperature else 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@internals_bp.route('/internal_humidity', methods=['POST'])
def add_internal_humidity():
    data = request.json
    try:
        result = create_internal_humidity(data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400  
    
@internals_bp.route('/internal_humidity', methods=['GET'])
def get_internal_humidities():
    try:
        humidities = list_internal_humidities()
        return jsonify(humidities), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@internals_bp.route('/internal_humidity/latest', methods=['GET'])
def get_latest_internal_humidity():
    try:
        humidity = get_latest_internal_humidity()
        return jsonify(humidity), 200 if humidity else 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@internals_bp.route('/internal_pressure', methods=['POST'])
def add_internal_pressure():
    data = request.json
    try:
        result = create_internal_pressure(data)
        return jsonify(result), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    
@internals_bp.route('/internal_pressure', methods=['GET'])
def get_internal_pressures():
    try:
        pressures = list_internal_pressures()
        return jsonify(pressures), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@internals_bp.route('/internal_pressure/latest', methods=['GET'])
def get_latest_internal_pressure():
    try:
        pressure = get_latest_internal_pressure()
        return jsonify(pressure), 200 if pressure else 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500