import os
import hashlib
import subprocess
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import time
from colorama import Fore, init

# Suppress warnings from the warnings module
import warnings
warnings.filterwarnings('ignore')

init(autoreset=True)

ascii_art = r"""
                         ___    ___    ___       _____                                                 
/'\_/`\                 (  _`\ (  _`\ (  _`\    (  _  )                           _                    
|     |   _ _    ___    | (_(_)| (_(_)| | ) |   | ( ) | _ __   __     _ _   ___  (_) ____    __   _ __ 
| (_) | /'_` ) /'___)   `\__ \ `\__ \ | | | )   | | | |( '__)/'_ `\ /'_` )/' _ `\| |(_  ,) /'__`\( '__)
| | | |( (_| |( (___    ( )_) |( )_) || |_) |   | (_) || |  ( (_) |( (_| || ( ) || | /'/_ (  ___/| |   
(_) (_)`\__,_)`\____)   `\____)`\____)(____/'   (_____)(_)  `\__  |`\__,_)(_) (_)(_)(____)`\____)(_)   
                                                            ( )_) |                                    
                                                             \___/'                                    
"""

def animate_ascii_art():
    for line in ascii_art.splitlines():
        print(Fore.GREEN + line)
        time.sleep(0.1)  # Adjust the speed of animation by changing the sleep time

if __name__ == "__main__":
    animate_ascii_art()
    # Mac SSD Organizer script starts here

def install_dependencies():
    try:
        import PIL
        import pyexifinfo
        import alive_progress
    except ImportError:
        subprocess.run(["pip", "install", "Pillow", "pyexifinfo", "alive-progress"], stderr=subprocess.PIPE)

def get_external_drives():
    volumes_dir = "/Volumes"
    drives = [os.path.join(volumes_dir, d) for d in os.listdir(volumes_dir) if os.path.ismount(os.path.join(volumes_dir, d)) and d != "Macintosh HD"]
    return drives

def choose_ssd(external_drives):
    print("External SSDs found:")
    for i, drive in enumerate(external_drives, 1):
        print(f"{i}. {drive}")
    choice = int(input("Select the SSD to use (Enter the number): "))
    return external_drives[choice - 1]

def format_ssd(ssd_path):
    response = input(f"Do you want to format {ssd_path} to exFAT? (y/n): ").lower()
    if response == 'y':
        subprocess.run(["diskutil", "eraseDisk", "ExFAT", "MySSD", "GPT", ssd_path], stderr=subprocess.PIPE)

def calculate_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def organize_and_copy_file(file_path, external_ssd_dir, log_file, hash_set):
    from PIL import Image
    import pyexifinfo
    
    try:
        mod_time = os.path.getmtime(file_path)
        year = datetime.fromtimestamp(mod_time).strftime('%Y')
        month = datetime.fromtimestamp(mod_time).strftime('%m')
        day = datetime.fromtimestamp(mod_time).strftime('%d')
        date = datetime.fromtimestamp(mod_time).strftime('%d-%m-%Y')
        time = datetime.fromtimestamp(mod_time).strftime('%H.%M.%S')
        
        if file_path.lower().endswith(('.txt', '.docx', '.pdf', '.csv', '.xlsx', '.sql', '.key')):
            original_name = os.path.basename(file_path)
            file_type = original_name.split('.')[-1].upper()
            new_dir = os.path.join(external_ssd_dir, "Documents", year, month, day, "Document")
            new_file_path = os.path.join(new_dir, f"{file_type}-{original_name}")
        elif file_path.lower().endswith(('.png', '.jpg', '.jpeg', '.mp4', '.mov', '.avi', '.mkv')):
            file_hash = calculate_hash(file_path)
            if file_hash in hash_set:
                return  # Skip duplicate media files
            
            hash_set.add(file_hash)
            media_type = 'Photos' if file_path.lower().endswith(('.png', '.jpg', '.jpeg')) else 'Videos'
            
            metadata = pyexifinfo.get_json(file_path)
            if metadata:
                metadata = metadata[0]  # pyexifinfo returns a list with a single dictionary
                model = metadata.get('EXIF:Model', 'Unidentified')
                new_dir = os.path.join(external_ssd_dir, "Media", year, month, day, "Identified", model)
            else:
                new_dir = os.path.join(external_ssd_dir, "Media", year, month, day, "Unidentified")
            
            new_file_path = os.path.join(new_dir, f"{date}-{time}.{file_path.split('.')[-1]}")
        elif file_path.lower().endswith(('.iso', '.img')):
            original_name = os.path.basename(file_path)
            os_name_version = original_name.rsplit('.', 1)[0]  # Remove extension
            new_dir = os.path.join(external_ssd_dir, "SystemImages", year, month, day, "SystemImages")
            new_file_path = os.path.join(new_dir, f"{os_name_version}.{file_path.split('.')[-1]}")
        else:
            return  # Skip uncommon files
        
        subprocess.run(["mkdir", "-p", new_dir], stderr=log_file)
        subprocess.run(["cp", "-n", file_path, new_file_path], stderr=log_file)
    except Exception as e:
        log_file.write(f"{datetime.now()} - Error processing {file_path}: {str(e)}\n")

def traverse_and_copy(directory, external_ssd_dir, log_file):
    from alive_progress import alive_bar
    
    file_paths = []
    hash_set = set()
    for foldername, subfolders, filenames in os.walk(directory):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            if os.path.exists(file_path):  # Check if the file exists
                file_paths.append(file_path)
    
    with alive_bar(len(file_paths), title="Copying Files") as bar:
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(organize_and_copy_file, file_path, external_ssd_dir, log_file, hash_set) for file_path in file_paths]
            for future in concurrent.futures.as_completed(futures):
                bar()

def main():
    install_dependencies()
    
    external_drives = get_external_drives()
    if not external_drives:
        print("No external SSD found. Please attach your external SSD and run the script again.")
        return
    
    external_ssd_base_dir = choose_ssd(external_drives)
    
    format_ssd(external_ssd_base_dir)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    external_ssd_dir = os.path.join(external_ssd_base_dir, timestamp)
    
    log_file_path = f"{external_ssd_dir}_log.txt"
    
    with open(log_file_path, 'w') as log_file:
        home_dir = os.path.expanduser("~")
        traverse_and_copy(home_dir, external_ssd_dir, log_file)

if __name__ == "__main__":
    main()
