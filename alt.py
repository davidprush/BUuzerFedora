import subprocess
import os
import tarfile
import shutil
import logging
import pwd

# Configure logging to both file and console
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    handlers=[logging.FileHandler("backup_script.log"),
                              logging.StreamHandler()])
logger = logging.getLogger(__name__)

def check_sudo():
    """Check if the script is running with root privileges."""
    if os.getuid() != 0:
        logger.error("This script must be run as root or with sudo privileges.")
        raise PermissionError("Root privileges required.")

def get_usb_devices():
    """Return a list of USB storage devices."""
    try:
        output = subprocess.check_output(["lsblk", "-J", "-o", "NAME,MOUNTPOINT,LABEL"], encoding='utf-8')
        import json
        data = json.loads(output)
        usb_devices = []
        for device in data['blockdevices']:
            if 'children' in device:
                for child in device['children']:
                    if child.get('mountpoint') and child['mountpoint'].startswith('/media/'):
                        usb_devices.append({
                            'name': child['name'],
                            'mountpoint': child['mountpoint'],
                            'label': child.get('label', 'No Label')
                        })
        return usb_devices
    except subprocess.CalledProcessError as e:
        logger.error(f"Error listing USB devices: {e}")
        return []
    except Exception as e:
        logger.error(f"Unexpected error in get_usb_devices: {e}")
        return []

def select_usb_device(usb_devices):
    """Allow user to select a USB device from the list."""
    if not usb_devices:
        logger.warning("No USB devices found.")
        return None

    print("Available USB drives:")
    for i, device in enumerate(usb_devices, 1):
        print(f"{i}. {device['label']} - {device['mountpoint']}")
    
    try:
        choice = int(input("Enter the number of the USB drive to use: ")) - 1
        if 0 <= choice < len(usb_devices):
            return usb_devices[choice]['mountpoint']
        else:
            logger.warning("Invalid selection")
            return None
    except ValueError:
        logger.error("Invalid input for USB drive selection.")
        return None

def backup_apps(backup_path):
    """Backup user-installed applications."""
    backup_file = os.path.join(backup_path, "installed_packages.txt")
    try:
        print("Backing up installed applications...")
        with open(backup_file, 'w') as f:
            subprocess.run(["dnf", "repoquery", "--userinstalled"], stdout=f, check=True)
        logger.info(f"Applications backed up to {backup_file}")
        print(f"Applications backed up to {backup_file}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error backing up applications: {e}")
        print(f"Error backing up applications: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in backup_apps: {e}")
        print(f"Unexpected error in backup_apps: {e}")

def backup_kde_config(backup_path):
    """Backup KDE configuration and settings."""
    kde_config_dir = os.path.expanduser("~/.config")
    kde_backup_dir = os.path.join(backup_path, "kde_config")
    try:
        print("Backing up KDE configuration...")
        shutil.copytree(kde_config_dir, kde_backup_dir, dirs_exist_ok=True)
        logger.info(f"KDE configuration backed up to {kde_backup_dir}")
        print(f"KDE configuration backed up to {kde_backup_dir}")
    except shutil.Error as e:
        logger.error(f"Error copying KDE config: {e}")
        print(f"Error copying KDE config: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in backup_kde_config: {e}")
        print(f"Unexpected error in backup_kde_config: {e}")

def backup_home_dir(backup_path):
    """Create a compressed backup of the user's directory."""
    home_dir = os.path.expanduser("~")
    backup_file = os.path.join(backup_path, "home_backup.tar.gz")
    try:
        print("Backing up home directory...")
        with tarfile.open(backup_file, "w:gz") as tar:
            tar.add(home_dir, arcname="home")
        logger.info(f"Home directory backed up to {backup_file}")
        print(f"Home directory backed up to {backup_file}")
    except tarfile.TarError as e:
        logger.error(f"Error creating tar archive: {e}")
        print(f"Error creating tar archive: {e}")
    except Exception as e:
        logger.error(f"Unexpected error in backup_home_dir: {e}")
        print(f"Unexpected error in backup_home_dir: {e}")

def main():
    try:
        check_sudo()
        
        usb_devices = get_usb_devices()
        backup_path = select_usb_device(usb_devices)
        
        if backup_path:
            try:
                os.makedirs(backup_path, exist_ok=True)
                logger.info(f"Backup directory created at {backup_path}")
                print(f"Backup directory created at {backup_path}")
                
                backup_apps(backup_path)
                backup_kde_config(backup_path)
                backup_home_dir(backup_path)
                
                logger.info("Backup operations completed successfully.")
                print("Backup operations completed successfully.")
            except OSError as e:
                logger.error(f"Error creating backup directory: {e}")
                print(f"Error creating backup directory: {e}")
            except Exception as e:
                logger.error(f"An unexpected error occurred during the backup process: {e}")
                print(f"An unexpected error occurred during the backup process: {e}")
        else:
            logger.warning("Backup operation cancelled or no valid USB drive selected.")
            print("Backup operation cancelled or no valid USB drive selected.")
    except PermissionError:
        logger.info("Please run this script with sudo privileges.")
        print("Please run this script with sudo privileges.")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
