from flask import Blueprint, Response
from CameraPackageSupport.WebCamService import WebCam

REQUEST_API = Blueprint('request_api', __name__)

def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API

def gen(webcam):
    """Generate frames from the specified webcam instance."""
    while True:
        frame = webcam.get_frame()  # Get frame from the webcam instance
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
        )
