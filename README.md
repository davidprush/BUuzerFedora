# Fedora System and User Data Backup Script

## Overview

This Python script is designed for Fedora Asahi Remix users to perform backups of system preferences, user directories, and installed software. It offers:

- **USB Drive Selection**: Lists and allows selection of USB drives for backup storage.
- **Backup of System Preferences**: Saves configurations from multiple system directories.
- **User Directory Backup**: Compresses and saves the user's home directory.
- **Software Inventory**: Lists user-installed software and saves it to a text file.

**Important:** This script requires root privileges to access and backup system directories. Run with sudo.

## Prerequisites

- **Fedora Asahi Remix** installed.
- **Python 3** installed on your system.
- **A USB drive** connected and mounted for backup storage.
- **Sudo privileges** to execute the script.

## Script Functions

### `check_sudo()`
Checks if the script is running with sudo privileges.

### `list_usb_drives()`
Lists all currently mounted USB drives.

### `select_drive(usb_drives)`
Allows the user to select a drive for backup from the list.

### `save_system_preferences(mount_point)`
Backs up configurations from various system directories to the selected USB drive:
  - `/etc`
  - `/usr/share`
  - `~/.config`
  - `~/.local/share`
  - `/var/lib`

### `backup_user_directory(mount_point)`
Compresses and backs up the user's home directory.

### `list_user_programs()`
Lists all user-installed programs, excluding version numbers.

### `save_programs_list(mount_point, programs)`
Writes the list of programs to a text file on the selected USB drive.

## How to Use

1. **Save the Script**: Copy the provided Python script into a file named `BUuzerFedora.py` on your Fedora Asahi Remix system.

2. **Connect USB Drive**: Ensure at least one USB drive is connected and mounted.

3. **Run the Script**:
   - Open a terminal.
   - Navigate to the directory containing `BUuzerFedora.py`.
   - Execute with:
     ```bash
     sudo python3 BUuzerFedora.py
     ```

4. **Follow Prompts**:
   - The script will list available USB drives; enter the number of the drive you wish to use for backup.
   - Wait for the backup processes to complete. The script will provide feedback on each step.

## Notes

- **Backup Size**: Backing up directories like `/etc` and `/usr/share` can result in large backups. Adjust the `config_dirs` list in the `save_system_preferences` function if you need a more tailored backup.
- **Permissions**: If you encounter permission errors, ensure you're running the script with sudo.
- **Space**: Check available space on the USB drive before running the script, especially for large backups.

## Safety

- **Test First**: Before using on critical data, test the script on a non-critical system or user account to ensure it behaves as expected.
- **Data Integrity**: Always verify backups for completeness and integrity after the process is done.

## Disclaimer

Use this script at your own risk. While it's designed to be safe and effective, there's always a potential for data loss or corruption when dealing with system-level backups. Ensure you have other backups or recovery options available.

---

