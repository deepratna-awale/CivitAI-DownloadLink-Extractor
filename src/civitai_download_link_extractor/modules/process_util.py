import psutil
import subprocess
import time
import pathlib
from pathlib import Path
from termcolor import colored
import platform


def process_exists(process_name):
    for process in psutil.process_iter():
        # check whether the process name matches
        if process_name in process.name():
            return True
    return False


def findPath(process_name):
    for pid in psutil.pids():
        if process_name in psutil.Process(pid).name():
            return psutil.Process(pid).exe()


def terminate_process(process_name, pid=None):
    # Detect the operating system
    os_name = platform.system()

    try:
        if os_name == "Windows":
            # Command to kill Chrome on Windows
            subprocess.run(["taskkill", "/F", "/IM", process_name], check=True)

        elif os_name == "Linux":
            # Command to kill Chrome on Linux
            subprocess.run(["pkill", "chrome"], check=True)

        else:
            print(f"Unsupported operating system: {os_name}")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")


def get_path_from_process(process_name):
    first_run = True

    while True:
        if process_exists(process_name):
            process_path = findPath(process_name)
            print(f"Found {process_name} at:", process_path)
            terminate_process(process_name)
            break
        else:
            if first_run:
                first_run = False

                print(
                    colored(
                        f"{process_name.capitalize()} is NOT Running. \
                    Please run {process_name} to begin.",
                        "red",
                    )
                )
            time.sleep(3)

    return process_path


def open_process(process_path, args):
    process = None
    try:
        process = subprocess.Popen([process_path, args])

    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
        process = subprocess.Popen([process_path, args])

    finally:
        return process


def default_launch(default_paths):
    os_name = platform.system()
    print("Trying default file locations.")
    
    if os_name == "Windows":
        process_path = default_paths["WINDOWSx86"]
        process = open_process(default_paths["WINDOWSx64"], "")
        if not process:
            process_path = default_paths["WINDOWSx64"]
            open_process(default_paths["WINDOWSx64"], "")

    elif os_name == "Linux":
        process_path = default_paths["LINUX"]
        open_process(default_paths["LINUX"], "")

    elif os_name == "Darwin":
        process_path = default_paths["MACOS"]
        open_process(default_paths["MACOS"], "")

    return process_path
