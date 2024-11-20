from flask import Flask, url_for
from CameraPackageSupport import routes
from CameraPackageSupport.Camera_1 import zedcam_blueprint
from CameraPackageSupport.Camera_2 import anchor_blueprint

import logging
import argparse

# Set up logging configuration
logging.basicConfig(
    filename='logs/main.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

app = Flask(__name__)
app.register_blueprint(zedcam_blueprint)
app.register_blueprint(anchor_blueprint)
app.register_blueprint(routes.get_blueprint())

@app.route('/video_0')
def video_0():
    video_url = url_for('camera_1.video_0')
    response = app.test_client().get(video_url)
    return response.data

@app.route('/video_1')
def video_1():
    video_url = url_for('camera_2.video_1')
    response = app.test_client().get(video_url)
    return response.data

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run the Camera Package Server")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host IP address")
    parser.add_argument("--port", type=int, default=5001, help="Port number")
    parser.add_argument('--debug', type=bool, default=True, help="Debug mode")
    args = parser.parse_args()
    app.run(host=args.host, port=args.port, debug=args.debug)
