from flask import Blueprint, Response
from CameraPackageSupport import routes
from CameraPackageSupport.WebCamService import WebCam

zedcam_blueprint = Blueprint('camera_1', __name__)

@zedcam_blueprint.route('/video_0')
def video_0():
    try:
        zedcam = WebCam(camera_number=0)  # Use camera number 0 for this view
        return Response(routes.gen(zedcam), mimetype='multipart/x-mixed-replace; boundary=frame')
    except Exception as err:
        return Response(f'Error {err}')
