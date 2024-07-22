import pywinauto
import time
import subprocess
import os
import argparse
import sys

telemetry_dir = "./TelemetryLogs"

# Function to check if the executable name/path exists
def check_executable(executable_name):
    if not executable_name.endswith(".exe"):
        executable_name += ".exe"

    if os.path.isfile(executable_name):
        return executable_name
    
    # Check if the executable is in the PATH
    for path in os.getenv('PATH').split(os.pathsep):
        full_path = os.path.join(path, executable_name)
        if os.path.isfile(full_path):
            return full_path
    
    raise FileNotFoundError(f"Executable '{executable_name}' not found in the specified path, current directory, or system PATH.")

# Function to start the workload
def start_workload(workload_executable):
    app = pywinauto.Application().start(workload_executable)
    app.window(title_re=".*").set_focus()
    print("Workload application started")
    return app

# Function to start telemetry collection
def start_telemetry(presentmon_executable):
    if not os.path.exists(telemetry_dir):
        os.makedirs(telemetry_dir)

    telemetry_log_path = f"{telemetry_dir}/telemetry{time.strftime('%Y%m%d_%H%M%S')}.csv"
    subprocess.Popen([presentmon_executable, "--stop_existing_session", "-output_file", telemetry_log_path], shell=True)
    print("Telemetry collection started")

# Function to stop telemetry collection
def stop_telemetry(presentmon_executable):
    # Stop PresentMon and collect data
    subprocess.call(["taskkill", "/IM", presentmon_executable, "/F"])

    # Clear console window
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Telemetry collection stopped")

# Function to analyze telemetry data. Parse the CSV file created by presentmon and generate summary statistics
def analyze_telemetry():
    print("Analyzing telemetry data...")
    telemetry_files = os.listdir(telemetry_dir)
    telemetry_file = telemetry_files[-1]
    print(telemetry_file)
    telemetry_file_path = f"{telemetry_dir}/{telemetry_file}"
    with open(telemetry_file_path, 'r') as telemetry_file:
        frameTimeHeader = "FrameTime"
        telemetry_data = telemetry_file.readlines()
        headers = telemetry_data[0].split(',')
        frameTimeIndex = headers.index(frameTimeHeader)
        telemetry_data = [float(line.split(',')[frameTimeIndex]) for line in telemetry_data[1:]]
        print(f"Number of frames: {len(telemetry_data)}")
        print(f"Average frame time: {sum(telemetry_data) / len(telemetry_data)} ms")
        print(f"Minimum frame time: {min(telemetry_data)} ms")
        print(f"Maximum frame time: {max(telemetry_data)} ms")
    print("Telemetry analysis complete")

# Function to run the test scenario
def run_test(presentmon_executable, workload_executable):
    try:
        start_telemetry(presentmon_executable)
        app = start_workload(workload_executable)
        time.sleep(252000)  # Uncomment to run for 70 hours
        app.kill()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        stop_telemetry(presentmon_executable)
        analyze_telemetry()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated workload testing and telemetry collection.")
    parser.add_argument('--presentmon', type=str, default='PresentMon64.exe', help='Filename or path of the PresentMon executable. This also checks PATH')
    parser.add_argument('--workload', type=str, default='workload.exe', help='Filename or path of the workload executable. This also checks PATH')
    args = parser.parse_args()

    try:
        presentmon_executable = check_executable(args.presentmon)
        workload_executable = check_executable(args.workload)
        run_test(presentmon_executable, workload_executable)
    except FileNotFoundError as e:
        print(e)
        sys.exit(1)
