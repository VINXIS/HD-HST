import pywinauto

# Function to start the workload
def start_workload(workload_executable):
    app = pywinauto.Application().start(workload_executable)
    app.window(title_re=".*").set_focus()
    print("Workload application started")
    return app
