import os
import shutil
import hashlib
import argparse
import time
import logging

def setup_logging(log_file):
    # Configure logging to write to a file and display messages on the console
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)

def compute_file_hash(file_path, block_size=65536):
    """Calculate the hash of a file."""
    hash_object = hashlib.md5()
    with open(file_path, 'rb') as f:
        for block in iter(lambda: f.read(block_size), b''):
            hash_object.update(block)
    return hash_object.hexdigest()

def create_directory(directory):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(directory):
        os.makedirs(directory)

def copy_file(source_file, replica_file):
    """Copy a file if source and replica files differ."""
    source_file_hash = compute_file_hash(source_file)
    replica_file_hash = compute_file_hash(replica_file) if os.path.exists(replica_file) else None

    if source_file_hash != replica_file_hash:
        shutil.copy2(source_file, replica_file)
        return True  # File was copied
    return False  # File was not copied

def handle_deletions(replica_folder, source_contents, logged_items):
    """Handle deletions in the replica folder, including files and directories inside deleted directories."""
    replica_contents = set()

    for root, dirs, files in os.walk(replica_folder):
        for item in dirs + files:
            item_path = os.path.join(root, item)
            replica_contents.add(os.path.relpath(item_path, replica_folder))

    for item_path in replica_contents - source_contents:
        if item_path not in logged_items:
            item_path = os.path.join(replica_folder, item_path)

            if os.path.isfile(item_path):
                os.remove(item_path)
                log_message = f"File deleted: {item_path}"
                logging.info(log_message)
                logged_items.add(item_path)
            elif os.path.isdir(item_path):
                # Recursively handle deletions inside the deleted directory
                handle_deletions(item_path, source_contents, logged_items)

                shutil.rmtree(item_path)
                log_message = f"Directory deleted: {item_path}"
                logging.info(log_message)
                logged_items.add(item_path)

            # Add the parent directory to logged items
            parent_dir = os.path.dirname(item_path)
            logged_items.add(parent_dir)

def sync_folders(source_folder, replica_folder, log_file, interval):
    """Synchronize the source folder to the replica folder periodically."""
    logged_items = set()  # To keep track of logged items

    while True:
        try:
            source_contents = set()

            for root, dirs, files in os.walk(source_folder):
                for directory in dirs:
                    source_dir_path = os.path.join(root, directory)
                    replica_dir_path = os.path.join(replica_folder, os.path.relpath(source_dir_path, source_folder))
                    source_contents.add(os.path.relpath(source_dir_path, source_folder))

                    if not os.path.exists(replica_dir_path):
                        create_directory(replica_dir_path)
                        log_message = f"Directory created: {replica_dir_path}"
                        logging.info(log_message)
                        logged_items.add(replica_dir_path)

                for file in files:
                    source_file_path = os.path.join(root, file)
                    replica_file_path = os.path.join(replica_folder, os.path.relpath(source_file_path, source_folder))
                    source_contents.add(os.path.relpath(source_file_path, source_folder))

                    if copy_file(source_file_path, replica_file_path):
                        log_message = f"File copied: {source_file_path} to {replica_file_path}"
                        logging.info(log_message)
                        logged_items.add(replica_file_path)

            handle_deletions(replica_folder, source_contents, logged_items)
            
            time.sleep(interval)
        except KeyboardInterrupt:
            break

# Main function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Synchronize two folders")
    parser.add_argument("source_folder", help="Source folder path")
    parser.add_argument("replica_folder", help="Replica folder path")
    parser.add_argument("log_file", help="Log file path")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")

    args = parser.parse_args()

    setup_logging(args.log_file)

    if not os.path.exists(args.source_folder) or not os.path.exists(args.replica_folder):
        logging.error("Source and replica folders must exist.")
    else:
        logging.info(f"Synchronizing {args.source_folder} to {args.replica_folder} every {args.interval} seconds.")
        sync_folders(args.source_folder, args.replica_folder, args.log_file, args.interval)