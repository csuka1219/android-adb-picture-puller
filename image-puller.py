import os
from ppadb.client import Client as AdbClient

# Define supported image and video file extensions
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', 'webp']
VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mkv', '.mov' '.gif']

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

def get_folders(device, folder):
    dir = f"/storage/emulated/0/{folder}"
    
    # Check if the directory exists on the Android device
    result = run_adb_shell(device, f'ls "{dir}"')
    if "No such file or directory" in result:
        print("DCIM directory not found on the device.")
        return []
    
    # List directories
    result = run_adb_shell(device, f'find "{dir}" -mindepth 1 -maxdepth 1 -type d')
    folders = [folder.strip() for folder in result.splitlines()]
    folders.append(dir)
    
    return folders

def get_pictures_from_android():
    # Connect to ADB and get the device list
    client = AdbClient(host="127.0.0.1", port=5037)
    try:
        devices = client.devices()
    except:
        print("Adb connection error.")
        return

    if not devices:
        print("No Android device found.")
        return

    # Get the first connected device (you can modify this if you have multiple devices connected)
    device = devices[0]

    # Create a folder to store the pictures
    if not os.path.exists("Android_Pictures"):
        os.makedirs("Android_Pictures")

    # Get the list of subdirectories inside the DCIM and Download directory on the Android device (you can extend it with another folders)
    folders = get_folders(device, "DCIM")
    folders.extend(get_folders(device, "Download"))

    # Pull pictures and videos from each subdirectory
    for folder in folders:
        pull_pictures_from_dir(device, folder)

if __name__ == "__main__":
    get_pictures_from_android()
