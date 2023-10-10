# Folder Synchronization Script

This Python script is designed to synchronize the contents of two folders. It monitors a source folder and copies any new or modified files and subdirectories to a replica folder. Additionally, it tracks and logs deletions.

## Features

- Real-time synchronization between a source folder and a replica folder.
- File copying only when changes are detected.
- Automatic creation of missing directories.
- Deletion tracking for files and directories.
- Logging of synchronization activities.

## Prerequisites

Before using this script, ensure that you have:

- Python 3.x installed on your system.
- Required Python packages installed (you can install them using `pip install -r requirements.txt`).

## Usage

1. Clone or download the repository to your local machine.

2. Open a terminal or command prompt and navigate to the script's directory.

3. Run the script with the following command:

```bash
python sync_folders.py source_folder_path replica_folder_path log_file_path synchronization_interval```

Replace the placeholders with actual paths and values:

- `source_folder_path`: The path to the source folder you want to synchronize.
- `replica_folder_path`: The path to the replica folder where changes will be copied.
- `log_file_path`: The path to the log file for tracking synchronization activities.
- `synchronization_interval`: The time interval (in seconds) for checking changes and performing synchronization. E.g., use 30 for a 30-second interval.

4. The script will continuously monitor and synchronize the folders at the specified interval.

## Logging

The script generates log files that record synchronization activities. You can review these log files for insights into what the script is doing.

## Customization

You can customize the script's behavior by modifying the source code to meet your specific requirements. For example, you can change the hashing method or adjust the logging level.

## Acknowledgments

This script was created as a simple utility to synchronize folders and can be further extended or modified to fit your needs.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
