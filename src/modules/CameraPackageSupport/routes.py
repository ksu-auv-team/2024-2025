from flask import Blueprint, Response, request
from modules.CameraPackageSupport.WebCamService import WebCam
import cv2
import pyzed.sl as sl
import time
REQUEST_API = Blueprint('request_api', __name__)


def get_blueprint():
    """Return the blueprint for the main app module"""
    return REQUEST_API


def gen(webcam):
    if(webcam.camera_number==0):
        init = sl.InitParameters(depth_mode=sl.DEPTH_MODE.NEURAL,
                                coordinate_units=sl.UNIT.METER,
                                coordinate_system=sl.COORDINATE_SYSTEM.RIGHT_HANDED_Y_UP, 
                                camera_fps= 15, 
                                camera_resolution=sl.RESOLUTION.HD720)
        init.set_from_serial_number(34092091) ##used to ensure that ZED camera is accessed
        zed = sl.Camera()
        err = zed.open(init)
        image = sl.Mat()
        depthMap = sl.Mat()
    else:
        capture = cv2.VideoCapture(webcam.camera_number)
        if not capture:
            raise Exception("Error accessing the WebCam")
    while True:
        if(webcam.camera_number==0):##zed camera is handled differently from regular IP cams
            if err==sl.ERROR_CODE.SUCCESS:
                if zed.grab() == sl.ERROR_CODE.SUCCESS:##retrieves a frame from the ZED
                    zed.retrieve_measure(depthMap, sl.MEASURE.DEPTH)
                    zed.retrieve_image(image, sl.VIEW.LEFT)
            else:
                print("Issue with accessing ZED camera.")
            frame = webcam.get_frame(image.get_data()) ##converts the ZED frame to OpenCV's format
        else:
            frame = webcam.get_frame(capture)
        yield (
            b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'
        )


@REQUEST_API.route('/stream')
def monitoring():
    try:
        webcam = WebCam()
        return Response(gen(webcam), mimetype='multipart/x-mixed-replace; boundary=frame') ##Returns a picture essentially
    except Exception as err:
        return Response(f'Error {err}')