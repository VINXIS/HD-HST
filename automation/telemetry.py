import os
import time
import subprocess
import statistics

telemetry_dir = "./TelemetryLogs"

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

# Function to analyze telemetry data
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
        telemetry_data = [float(line.split(',')[frameTimeIndex]) for line in telemetry_data[1:] if len(line.split(",")) > frameTimeIndex]
        
        frame_count = len(telemetry_data)
        avg_frame_time = sum(telemetry_data) / frame_count
        min_frame_time = min(telemetry_data)
        max_frame_time = max(telemetry_data)
        stddev_frame_time = statistics.stdev(telemetry_data)
        percentile_90 = statistics.quantiles(telemetry_data, n=10)[8]  # 90th percentile
        
        print(f"Number of frames: {frame_count}")
        print(f"Average frame time: {avg_frame_time:.2f} ms")
        print(f"Minimum frame time: {min_frame_time:.2f} ms")
        print(f"Maximum frame time: {max_frame_time:.2f} ms")
        print(f"Standard deviation of frame time: {stddev_frame_time:.2f} ms")
        print(f"90th percentile of frame time: {percentile_90:.2f} ms")

    print("Telemetry analysis complete")
