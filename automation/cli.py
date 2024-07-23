import argparse
import sys
import time
from .utils import check_executable
from .telemetry import start_telemetry, stop_telemetry, analyze_telemetry
from .workload import start_workload

def run_test(presentmon_executable, workload_executable):
    try:
        start_telemetry(presentmon_executable)
        app = start_workload(workload_executable)
        time.sleep(10)  # Run for 10 seconds for testing
        # time.sleep(252000)  # Uncomment to run for 70 hours
        app.kill()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        stop_telemetry(presentmon_executable)
        analyze_telemetry()

def main():
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

if __name__ == "__main__":
    main()
