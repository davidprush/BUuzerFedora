import subprocess
import os
import shutil
import datetime
import sys

def check_sudo():
    """Check if the script is running with sudo privileges."""
    try:
        subprocess.run(["sudo", "-n", "true"], check=True)
        print("Sudo privilege check passed.")
        return True
    except subprocess.CalledProcessError:
        print("This script requires sudo privileges to run correctly.")
        return False

def list_usb_drives():
    """List all attached USB drives."""
    try:
        drives = subprocess.check_output(["lsblk", "-o", "NAME,MOUNTPOINT,LABEL,SIZE", "-l", "-n", "-f"]).decode().split('\n')
        usb_drives = [d for d in drives if 'sd' in d.split()[0] and len(d.split()) >= 2]
        if usb_drives:
            print("USB drives found:")
        else:
            print("No USB drives found.")
        return usb_drives
    except subprocess.CalledProcessError as e:
        print(f"Error listing USB drives: {e}")
        return []

def select_drive(usb_drives):
    """Let user select a drive from the list."""
    if not usb_drives:
        print("No USB drives available to select.")
        return None

    for idx, drive in enumerate(usb_drives, 1):
        print(f"{idx}. {drive}")
    while True:
        try:
            choice = int(input("Select a drive by number: "))
            if 1 <= choice <= len(usb_drives):
                mount_point = usb_drives[choice - 1].split()[1]
                if not os.path.ismount(mount_point):
                    print("Selected drive is not mounted. Please try another.")
                    continue
                print(f"Drive selected: {mount_point}")
                return mount_point
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Please enter a valid number.")
        except IndexError:
            print("Drive selection failed. Please try again.")

def save_system_preferences(mount_point):
    """Save all system preferences to a file on the selected drive."""
    # List of directories containing system-wide configurations
    config_dirs = [
        "/etc",  # System-wide configuration files
        "/usr/share",  # Shared data
        os.path.expanduser("~/.config"),  # User-specific configurations for KDE and others
        os.path.expanduser("~/.local/share"),  # User-specific data
        "/var/lib"  # State information
    ]
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dest_path = os.path.join(mount_point, f"system_preferences_{timestamp}.tar.gz")
    
    try:
        # Use tar to compress all these directories into one archive
        tar_command = ["tar", "-czf", dest_path]
        for directory in config_dirs:
            if os.path.exists(directory):
                tar_command.extend(["-C", os.path.dirname(directory), os.path.basename(directory)])
            else:
                print(f"Warning: Directory {directory} does not exist, skipping.")
        
        subprocess.run(tar_command, check=True)
        print(f"All system preferences have been saved to {dest_path}.")
    except subprocess.CalledProcessError as e:
        print(f"Error saving system preferences: {e}")
    except PermissionError:
        print("Permission denied when trying to access one or more configuration directories.")

def backup_user_directory(mount_point):
    """Backup and compress the user directory to the selected drive."""
    home = os.path.expanduser("~")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dest_path = os.path.join(mount_point, f"user_backup_{timestamp}.tar.gz")
    try:
        subprocess.run(["tar", "-czf", dest_path, "-C", os.path.dirname(home), os.path.basename(home)], check=True)
        print(f"User directory has been backed up to {dest_path}.")
    except subprocess.CalledProcessError as e:
        print(f"Error backing up user directory: {e}")

def list_user_programs():
    """List user-installed programs without version numbers."""
    try:
        installed = subprocess.check_output(["dnf", "list", "--installed", "--userinstalled"]).decode()
        programs = [line.split()[0].split('-')[0] for line in installed.split('\n') if line and not 'Installed Packages' in line]
        print(f"Found {len(programs)} user-installed programs.")
        return list(set(programs))  # Remove duplicates
    except subprocess.CalledProcessError as e:
        print(f"Error listing user programs: {e}")
        return []

def save_programs_list(mount_point, programs):
    """Save the list of programs to a file on the selected drive."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    dest_path = os.path.join(mount_point, f"installed_programs_{timestamp}.txt")
    try:
        with open(dest_path, 'w') as f:
            for program in programs:
                f.write(f"{program}\n")
        print(f"List of installed programs saved to {dest_path}.")
    except IOError as e:
        print(f"Error writing program list: {e}")

def main():
    if not check_sudo():
        sys.exit(1)

    usb_drives = list_usb_drives()
    if not usb_drives:
        return

    mount_point = select_drive(usb_drives)
    if not mount_point:
        return

    print("\nStarting backup operations:")
    save_system_preferences(mount_point)
    backup_user_directory(mount_point)
    user_programs = list_user_programs()
    save_programs_list(mount_point, user_programs)
    print("\nAll backup operations have been completed.")

if __name__ == "__main__":
    main()
