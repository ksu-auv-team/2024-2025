from datetime import datetime
import subprocess
import logging
import argparse
import time
import os

all_packages = {
    'ai-package': 'modules/AIPackage.py',
    'camera-package': '--cameras',
    'hardware-interface': 'modules/HardwareInterface.py',
    'movement-package': 'modules/MovementPackage.py',
    'sonar-package': 'modules/SonarPackage.py',
    'flask-server': 'modules/DBHandler.py'
}

def main(args : argparse.Namespace):
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
        required_packages = []
        processes = []
        if args.ai_package:
            required_packages.append('ai-package')
        if args.camera_package:
            required_packages.append('camera-package')
        if args.hardware_interface:
            required_packages.append('hardware-interface')
        if args.movement_package:
            required_packages.append('movement-package')
        if args.sonar_package:
            required_packages.append('sonar-package')
        
        for package in required_packages:
            logging.info(f"Checking for {package}...")
            if package in all_packages:
                logging.info(f"Package {package} found")
                subprocess.run(['python', all_packages[package]])
            else:
                logging.error(f"Package {package} not found")
                return
            
            processes.append(subprocess.Popen(['python3', required_packages[package]]))

    except subprocess.CalledProcessError as e:
        logging.error(f"Error installing packages: {e}")
        return
    

if __name__ == "__main__":
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

    args = parser.parse_args()
    main(args)
