from datetime import datetime
import subprocess
import logging
import argparse
import time
import os


def main():
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Ensure the log directory exists
    log_dir = f'logs/{start_time}'
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    # Setup the logging configuration
    logging.basicConfig(
        filename=os.path.join(log_dir, 'app.log'),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info("Starting the application...")
    logging.info("Current working directory: %s", os.getcwd())
    logging.info("Python version: %s", os.sys.version)
    logging.info("Starting time: %s", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
    logging.info("Log directory: %s", log_dir)    
    
    # Insure the required packages are installed
    logging.info("Checking for required packages...")
    try:
        required_packages = [
            'flask',
            'opencv-python',
            'numpy',
            'requests',
            'flask-sqlalchemy',
            'asyncpg',
            'sqlalchemy[asyncio]'
        ]
        for package in required_packages:
            subprocess.check_call([os.sys.executable, '-m', 'pip', 'install', package])
            logging.info(f"Package {package} installed successfully.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error installing packages: {e}")
        return
    
    parser = argparse.parser()
    
    # Flask Server Arguments
    parser.add_argument('--flask-port', type=int, default=5000, help='Port for the Flask server')
    parser.add_argument('--flask-host', type=str, default='localhost', help='Host for the Flask server')
    parser.add_argument('--flask-debug', action='store_true', help='Run Flask server in debug mode')
    
    # AI Package Arguments
    parser.add_argument('--ai-package', type=bool, default=False, help='Use AI package for processing')
    
    # Camera Package Arguments
    parser.add_argument('--camera-package', type=bool, default=False, help='Use Camera package for video processing')
    
    # Hardware Interface Arguments
    parser.add_argument('--hardware-interface', type=bool, default=False, help='Use hardware interface for device control')
    
    # Movement Package Arguments
    parser.add_argument('--movement-package', type=bool, default=False, help='Use movement package for controlling movements')
    
    # Sonar Package Arguments
    parser.add_argument('--sonar-package', type=bool, default=False, help='Use sonar package for distance measurement')