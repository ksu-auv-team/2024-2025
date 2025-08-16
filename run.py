from shared import logger
from libs import db_manager  # may init DB side effects
import subprocess
import argparse
import os
import threading
import time

def stream_output(proc, log_obj: logger.Logger, stream_name: str):
    """
    Streams subprocess output through the logger.
    """
    stream = getattr(proc, stream_name)
    if not stream:
        return
    for line in iter(stream.readline, ''):
        line = line.strip()
        if stream_name == "stdout":
            log_obj.info(line)
        else:
            log_obj.error(line)
    stream.close()

def main():
    app_name = "hub"

    # Argument parser setup
    parser = argparse.ArgumentParser(description="Run the application with specified configurations.")
    parser.add_argument("--virtualized-controlled", action="store_true")
    parser.add_argument("--trainer", action="store_true")
    parser.add_argument("--just-db", action="store_true")
    parser.add_argument("--real-world", action="store_true")
    parser.add_argument("--to-qualify", action="store_true", help="Run in qualification mode.")
    parser.add_argument("--print-debug", action="store_true",
                        help="Enable console logging.")
    args = parser.parse_args()

    # Create master logger for this script
    main_log = logger.create_logger(app_name, args.print_debug)
    main_log.info("Starting main application...")
    main_log.info(f"Args: {args}")

    virtualized_controlled_processes = [
        ["python", "-m", "libs.db_manager.run"],
        ["python", "-m", "libs.data_visualizer.run"],

    ]

    trainer_processes = [
        ["python", "-m", "libs.db_manager.run"],
        ["python", "-m", "libs.data_visualizer.run"],

    ]

    real_world_controlled_processes = [
        ["python", "-m", "libs.db_manager.run"],
        # ["python", "-m", "libs.data_visualizer.run"],
        # ["python", "-m", "libs.hardware_interface.run"],
        # ["python", "-m", "libs.movement_package.run"]
    ]

    real_world_processes = [
        ["python", "-m", "libs.db_manager.run"],
        ["python", "-m", "libs.movement_package.run"],
        ["python", "-m", "libs.hardware_interface.run"]
    ]

    to_qualify_processes = [
        ["python", "-m", "libs.db_manager.run"],
        ["python", "-m", "libs.movement_package.run"],
        ["python", "-m", "libs.hardware_interface.run"],
        # ["python", "replay.py", "--from-api", "--post"]
    ]

    init_db_posts = [
        # ---- Inputs ----
        ["curl","-sS","--fail","-X","POST","http://192.168.8.109:5000/inputs/",
        "-H","Content-Type: application/json",
        "-d",'{"step_index":1,"direction":"forward","force":50,"s1":0.0,"s2":0.0,"s3":0.0,"arm":false}'],

        # ---- Outputs ----
        ["curl","-sS","--fail","-X","POST","http://192.168.8.109:5000/outputs/",
        "-H","Content-Type: application/json",
        "-d",'{"step_index":1,"direction":"hold","force":0,"M1":1500,"M2":1500,"M3":1500,"M4":1500,"M5":1500,"M6":1500,"M7":1500,"M8":1500,"S1":1500,"S2":1300,"S3":1300,"arm":false}'],

        # ---- Batteries ----
        ["curl","-sS","--fail","-X","POST","http://192.168.8.109:5000/batteries/",
        "-H","Content-Type: application/json",
        "-d",'{"step_index":1,"voltage1":12.5,"voltage2":12.4,"voltage3":12.3,"current1":1.2,"current2":1.1,"current3":1.3,"temperature1":25.4,"temperature2":26.1,"temperature3":25.8}'],

        # ---- Externals ----
        ["curl","-sS","--fail","-X","POST","http://192.168.8.109:5000/external_pressure",
        "-H","Content-Type: application/json",
        "-d",'{"step_index":1,"pressure":101.3}'],
        ["curl","-sS","--fail","-X","POST","http://192.168.8.109:5000/external_depth",
        "-H","Content-Type: application/json",
        "-d",'{"step_index":1,"depth":0.0}'],

        # ---- IMU ----
        ["curl","-sS","--fail","-X","POST","http://192.168.8.109:5000/imu/",
        "-H","Content-Type: application/json",
        "-d",'{"step_index":1,"X":0.0,"Y":0.0,"Z":9.81,"roll":0.0,"pitch":0.0,"yaw":0.0}'],

        # ---- Internals ----
        ["curl","-sS","--fail","-X","POST","http://192.168.8.109:5000/internal_temperature",
        "-H","Content-Type: application/json",
        "-d",'{"step_index":1,"temperature":25.0}'],
        ["curl","-sS","--fail","-X","POST","http://192.168.8.109:5000/internal_humidity",
        "-H","Content-Type: application/json",
        "-d",'{"step_index":1,"humidity":45.0}'],
        ["curl","-sS","--fail","-X","POST","http://192.168.8.109:5000/internal_pressure",
        "-H","Content-Type: application/json",
        "-d",'{"step_index":1,"pressure":101.3}'],

        # ---- Sonar ----
        ["curl","-sS","--fail","-X","POST","http://192.168.8.109:5000/sonar/",
        "-H","Content-Type: application/json",
        "-d",'{"step_index":1,"distance":3.42,"angle":57.0}'],
    ]


    processes = []
    threads = []
    subprocs = []

    if args.virtualized_controlled:
        processes = virtualized_controlled_processes
    elif args.trainer:
        processes = trainer_processes
    elif args.just_db:
        processes = real_world_controlled_processes
    elif args.real_world:
        processes = real_world_processes
    elif args.to_qualify:
        processes = to_qualify_processes

    i = 0
    proc_name = ""

    for cmd in processes:
        main_log.info(f"Starting subprocess: {' '.join(cmd)}")
        if i == 0:
            proc_name = "db_manager"
        elif i == 1:
            proc_name = "movement_package"
        elif i == 2:
            proc_name = "hardware_interface"
        elif i == 3:
            proc_name = "replay"
        proc_logger = logger.create_logger(proc_name, args.print_debug)
        i += 1

        # Start subprocess with stdout/stderr piped
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )
        subprocs.append(proc)

        # Thread for stdout
        t_out = threading.Thread(target=stream_output, args=(proc, proc_logger, "stdout"))
        t_out.daemon = True
        t_out.start()
        threads.append(t_out)

        # Thread for stderr
        t_err = threading.Thread(target=stream_output, args=(proc, proc_logger, "stderr"))
        t_err.daemon = True
        t_err.start()
        threads.append(t_err)

        if proc_name == "hardware_interface" and args.to_qualify:
            time.sleep(5)
        else:
            time.sleep(2.5)
    
    def terminate_processes():
        main_log.info("Terminating subprocesses...")
        for proc in subprocs:
            proc.terminate()
        for proc in subprocs:
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()

    try:
        for proc in subprocs:
            proc.wait()
    except KeyboardInterrupt:
        main_log.info("KeyboardInterrupt received. Shutting down...")
        terminate_processes()
    finally:
        terminate_processes()
        terminate_processes()

if __name__ == "__main__":
    main()
