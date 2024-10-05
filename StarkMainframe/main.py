import requests
import subprocess
import threading
import logging
import time
import os
import signal
import platform

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

# Determine the current operating system
CURRENT_OS = platform.system()

# Define service configurations with updated ports (5000, 5001, etc.)
SERVICES = {
    'ProjectSTARK.API': {
        'name': 'ProjectSTARK.API',
        'start_command': ['dotnet', 'run', '--project', 'ProjectSTARK.API/ProjectSTARK.API.csproj'],
        'health_check_url': 'http://localhost:5000/health',
        'api_base_url': 'http://localhost:5000/api'
    },
    'JarvisHealthAPI': {
        'name': 'JarvisHealthAPI',
        'start_command': ['dotnet', 'run', '--project', 'Services/Jarvis/JarvisHealthAPI/JarvisHealthAPI.csproj'],
        'health_check_url': 'http://localhost:5001/health',
        'api_base_url': 'http://localhost:5001/api'
    },
    'EcoVisionAPI': {
        'name': 'EcoVisionAPI',
        'start_command': ['python3', 'Services/EcoVision/EcoVisionAPI/app.py'],  # Use 'python3' for Linux
        'health_check_url': 'http://localhost:5002/health',
        'api_base_url': 'http://localhost:5002/api'
    },
    'FridayLearningBackend': {
        'name': 'FridayLearningBackend',
        'start_command': ['node', 'Services/Friday/FridayLearningBackend/server.js'],
        'health_check_url': 'http://localhost:5003/health',
        'api_base_url': 'http://localhost:5003/api'
    },
    # Add more services as needed
}

# Global dictionary to keep track of service processes
service_processes = {}

def start_service(service_config):
    """Starts a service as a subprocess."""
    name = service_config['name']
    command = service_config['start_command']
    logging.info(f"Starting service: {name}")
    try:
        if CURRENT_OS == 'Linux':
            # For Unix-like systems, use setsid to start a new session
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                preexec_fn=os.setsid,
                cwd=os.path.dirname(command[-1]) if os.path.isfile(command[-1]) else None
            )
        elif CURRENT_OS == 'Windows':
            # For Windows, use CREATE_NEW_PROCESS_GROUP
            CREATE_NEW_PROCESS_GROUP = 0x00000200
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=CREATE_NEW_PROCESS_GROUP,
                cwd=os.path.dirname(command[-1]) if os.path.isfile(command[-1]) else None
            )
        else:
            # For other OSes, proceed without special flags
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=os.path.dirname(command[-1]) if os.path.isfile(command[-1]) else None
            )
        service_processes[name] = process
        logging.info(f"Service {name} started with PID {process.pid}")
    except Exception as e:
        logging.error(f"Failed to start service {name}: {e}")

def check_service_health(service_config):
    """Checks if a service is healthy by making a request to its health endpoint."""
    url = service_config['health_check_url']
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            logging.info(f"Service {service_config['name']} is healthy")
            return True
        else:
            logging.warning(f"Service {service_config['name']} health check failed with status code {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        logging.warning(f"Service {service_config['name']} health check failed: {e}")
        return False

def monitor_services():
    """Continuously monitors the health of services."""
    while True:
        for service_config in SERVICES.values():
            if not check_service_health(service_config):
                logging.warning(f"Service {service_config['name']} is not healthy. Attempting to restart...")
                stop_service(service_config)
                start_service(service_config)
        time.sleep(30)  # Check every 30 seconds

def stop_service(service_config):
    """Stops a running service."""
    name = service_config['name']
    process = service_processes.get(name)
    if process:
        logging.info(f"Stopping service {name}")
        try:
            if CURRENT_OS == 'Linux':
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            elif CURRENT_OS == 'Windows':
                process.send_signal(signal.CTRL_BREAK_EVENT)
            process.wait(timeout=10)
            logging.info(f"Service {name} stopped")
        except Exception as e:
            logging.warning(f"Failed to stop service {name}: {e}")
            try:
                if CURRENT_OS == 'Linux':
                    os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                elif CURRENT_OS == 'Windows':
                    process.kill()
                logging.info(f"Service {name} forcefully killed")
            except Exception as e:
                logging.error(f"Failed to kill service {name}: {e}")
        finally:
            del service_processes[name]
    else:
        logging.info(f"Service {name} is not running")

def make_api_call(service_name, endpoint, method='GET', data=None, params=None):
    """Makes an API call to a specified service."""
    service_config = SERVICES.get(service_name)
    if not service_config:
        logging.error(f"Service {service_name} configuration not found")
        return None
    url = f"{service_config['api_base_url']}/{endpoint}"
    try:
        if method.upper() == 'GET':
            response = requests.get(url, params=params, timeout=10)
        elif method.upper() == 'POST':
            response = requests.post(url, json=data, timeout=10)
        else:
            logging.error(f"HTTP method {method} not supported")
            return None
        if response.status_code == 200:
            logging.info(f"API call to {service_name} {endpoint} succeeded")
            return response.json()
        else:
            logging.error(f"API call to {service_name} {endpoint} failed with status code {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"API call to {service_name} {endpoint} failed: {e}")
        return None

def monitor_process_output(process, name):
    """Monitors the stdout and stderr of a subprocess."""
    for line in iter(process.stdout.readline, b''):
        logging.info(f"[{name} stdout] {line.decode().rstrip()}")
    for line in iter(process.stderr.readline, b''):
        logging.error(f"[{name} stderr] {line.decode().rstrip()}")

def main():
    # Start all services
    for service_config in SERVICES.values():
        start_service(service_config)
        time.sleep(2)  # Brief pause between starting services

    # Start monitoring thread
    monitor_thread = threading.Thread(target=monitor_services, daemon=True)
    monitor_thread.start()

    # Start threads to monitor subprocess output
    for name, process in service_processes.items():
        output_thread = threading.Thread(target=monitor_process_output, args=(process, name), daemon=True)
        output_thread.start()

    # Allow services time to start up
    time.sleep(10)

    # Example usage of API calls
    # Interact with ProjectSTARK.API
    stark_api_data = make_api_call('ProjectSTARK.API', 'status', method='GET')
    if stark_api_data:
        logging.info(f"ProjectSTARK.API response: {stark_api_data}")

    # Interact with JarvisHealthAPI
    health_data = make_api_call('JarvisHealthAPI', 'users/profile', method='GET', params={'userId': 1})
    if health_data:
        logging.info(f"JarvisHealthAPI response: {health_data}")

    # Interact with EcoVisionAPI
    eco_vision_data = make_api_call('EcoVisionAPI', 'analyze', method='POST', data={'imagePath': '/path/to/image.jpg'})
    if eco_vision_data:
        logging.info(f"EcoVisionAPI response: {eco_vision_data}")

    # Interact with FridayLearningBackend
    learning_data = make_api_call('FridayLearningBackend', 'learn', method='POST', data={'topic': 'Machine Learning'})
    if learning_data:
        logging.info(f"FridayLearningBackend response: {learning_data}")

    # Keep the main thread alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Shutting down StarkMainframe...")
        # Stop all services
        for service_config in SERVICES.values():
            stop_service(service_config)
        logging.info("All services have been stopped.")

if __name__ == '__main__':
    main()

