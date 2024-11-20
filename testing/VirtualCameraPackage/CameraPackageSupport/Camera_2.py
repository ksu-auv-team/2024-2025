from flask import Blueprint, Response
from CameraPackageSupport import routes
from CameraPackageSupport.WebCamService import WebCam

anchor_blueprint = Blueprint('camera_2', __name__)

@anchor_blueprint.route('/video_1')
def video_1():
    try:
        anchor_camera = WebCam(camera_number=1)  # Use camera number 1 for this view
        return Response(routes.gen(anchor_camera), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as err:
        return Response(f'Error {err}')
