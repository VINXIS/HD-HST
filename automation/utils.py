import os

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
