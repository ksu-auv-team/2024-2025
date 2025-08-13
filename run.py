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
    parser.add_argument("--real-world-controlled", action="store_true")
    parser.add_argument("--real-world", action="store_true")
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
        ["python", "-m", "libs.data_visualizer.run"],
        ["python", "-m", "libs.hardware_interface.run"],

    ]

    real_world_processes = [
        ["python", "-m", "libs.db_manager.run"],
        ["python", "-m", "libs.data_visualizer.run"],
        ["python", "-m", "libs.hardware_interface.run"],

    ]

    processes = []
    threads = []
    subprocs = []

    if args.virtualized_controlled:
        processes = virtualized_controlled_processes
    elif args.trainer:
        processes = trainer_processes
    elif args.real_world_controlled:
        processes = real_world_controlled_processes
    elif args.real_world:
        processes = real_world_processes

    for cmd in processes:
        proc_name = cmd[-1].split('.')[-1]  # e.g., 'run' from 'libs.db_manager.run'
        proc_logger = logger.create_logger(proc_name, args.print_debug)

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

        time.sleep(5)
    
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
