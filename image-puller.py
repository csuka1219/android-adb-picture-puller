import os
from ppadb.client import Client as AdbClient

# Define supported image and video file extensions
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mkv', '.mov']

def run_adb_shell(device, command):
    # Execute a shell command on the connected Android device using ADB
    result = device.shell(command)
    return result.strip()

def pull_pictures_from_dir(device, remote_dir):
    # List files in the remote directory
    file_list = run_adb_shell(device, f'ls "{remote_dir}"').split()
    
    for file_name in file_list:
        remote_path = os.path.join(remote_dir, file_name).replace("\\", "/")
        local_path = os.path.join("Android_Pictures", file_name).replace("\\", "/")
        
        _, ext = os.path.splitext(file_name)
        if ext.lower() in (IMAGE_EXTENSIONS + VIDEO_EXTENSIONS):
            # If the file has a supported image or video extension, pull it from the Android device to the local machine
            device.pull(remote_path, local_path)

def get_folders_in_dcim(device):
    dcim_dir = "/storage/emulated/0/DCIM"
    
    # Check if the DCIM directory exists on the Android device
    result = run_adb_shell(device, f'ls "{dcim_dir}"')
    if "No such file or directory" in result:
        print("DCIM directory not found on the device.")
        return []
    
    # List directories inside DCIM
    result = run_adb_shell(device, f'find "{dcim_dir}" -mindepth 1 -maxdepth 1 -type d')
    folders = [folder.strip() for folder in result.splitlines()]
    
    return folders

def get_pictures_from_android():
    # Connect to ADB and get the device list
    client = AdbClient(host="127.0.0.1", port=5037)
    devices = client.devices()
    
    if not devices:
        print("No Android device found.")
        return

    # Get the first connected device (you can modify this if you have multiple devices connected)
    device = devices[0]

    # Create a folder to store the pictures
    if not os.path.exists("Android_Pictures"):
        os.makedirs("Android_Pictures")

    # Get the list of subdirectories inside the DCIM directory on the Android device
    folders = get_folders_in_dcim(device)

    # Pull pictures and videos from each subdirectory
    for folder in folders:
        pull_pictures_from_dir(device, folder)

if __name__ == "__main__":
    get_pictures_from_android()
