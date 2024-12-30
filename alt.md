
Here's the complete content for the README.md file:

markdown
# Backup Script for Fedora Linux

This Python script provides a comprehensive backup solution for Fedora Linux users, focusing on backing up installed applications, KDE configuration, and the entire home directory to a USB drive.

## Overview

- **Purpose:** To automate the backup of critical user data to a chosen USB drive.
- **Target System:** Fedora Linux with KDE environment.
- **Dependencies:** 
  - Python 3
  - `dnf` package manager
  - `lsblk` utility (part of `util-linux` package)
  - `tar` for compression

## Script Features

- **USB Drive Selection:** Lists available USB drives for user selection.
- **Backup Types:**
  - **Applications:** Lists all user-installed packages using `dnf`.
  - **KDE Configuration:** Copies the KDE configuration directory.
  - **Home Directory:** Compresses and backs up the entire home directory.

- **Error Handling:** Extensive try-except blocks for graceful error management.
- **Logging:** Logs all operations to a file (`backup_script.log`) and outputs to console for real-time feedback.
- **Sudo Check:** Ensures the script runs with root privileges.

## How to Use

1. **Run with sudo:**
   ```bash
   sudo python3 backup_script.py
   ```

2. Select a USB Device: 
The script will list all available USB drives. Choose one by entering its corresponding number.
Backup Process: 
The script will then proceed to backup applications, KDE settings, and your home directory.

3. Detailed Component Explanation
check_sudo()
Purpose: Verifies if the script is running with root privileges. If not, it raises a PermissionError.

4. get_usb_devices()
Functionality: Utilizes lsblk to get a JSON formatted list of block devices, filters for USB drives, and returns a list of mount points.

5. select_usb_device(usb_devices)
User Interaction: Displays available USB drives and asks for user input to select one.

6. backup_apps(backup_path)
Operation: 
Uses dnf repoquery --userinstalled to list all user-installed packages.
Saves the list to installed_packages.txt in the selected backup path.

7. backup_kde_config(backup_path)
Operation: 
Copies the .config directory (assumed to contain KDE settings) to the backup location.

8. backup_home_dir(backup_path)
Operation: 
Compresses the home directory into a .tar.gz file for complete backup.

9. main()
Orchestration: 
Orchestrates the flow of the script, calling other functions in order.
Manages exceptions and ensures operations run in sequence.

10. Logging
Logging is set to both file and console:
File: backup_script.log for persistent logging.
Console: Real-time output for user feedback.

11. Error Handling
Each major function has try-except blocks to catch specific exceptions like subprocess.CalledProcessError, shutil.Error, tarfile.TarError, and general exceptions.

12. Security and Permissions
The script checks for sudo privileges at the start to ensure it can perform necessary operations like accessing USB drives and backing up system data.

13. Known Limitations
Space: Assumes enough space on the USB drive for all backups.
KDE Assumption: The script assumes KDE settings are in ~/.config. If this changes or if using a different desktop environment, you'll need to adjust the script.

14. Future Enhancements
Exclusion lists for home directory backup to skip temporary or unnecessary files.
Option to backup to network locations or cloud storage.
Progress bars for long operations.
