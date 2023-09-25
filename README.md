# Mac SSD Organizer

![Python](https://img.shields.io/badge/python-v3.6+-blue.svg)

## Description

Mac SSD Organizer is a Python script designed exclusively for macOS users to automate and streamline the process of backing up files to an external Solid State Drive (SSD). The script meticulously organizes each file according to its type and date, and copies it to the SSD, thereby taking the tedium out of manual backups. It also formats the SSD to the exFAT file system before beginning the backup process. 

## Purpose 

- To assist macOS users in backing up their data effortlessly to an external SSD. 
- To systematically categorize and organize files on the SSD according to file type and date.
- To abandon the copying of duplicate media files and thus save space.
- To generate a log file to record any errors that might occur during the backup process.


## Features

- Categorizes files and organizes them by date and type.
- Formats the SSD to exFAT to support cross-platform compatibility.
- Avoids copying duplicate media files to save space.
- Creates a log file to record any errors encountered during the backup process.

## Installation Instructions

Clone the repository and navigate to the project directory by running:

```bash
git clone https://github.com/imhsouna/Mac-SSD-Organizer.git
cd Mac-SSD-Organizer
```

## Dependencies Installation Instructions

This script requires Python 3.6+ to run. Install all Python dependencies by running:

```bash
pip install -r requirements.txt
```

You may also need to install 'ExifTool' if it's not available on your system. You can do so by following the instructions [here](https://exiftool.org).

## File Structure 

In the SSD, files will be copied and organized as follows:

```
.
+-- SSD_Name
|     |-- YYYYMMDD_HHMMSS (timestamped session folder)
|           |-- Documents
|               |-- YYYY
|                   |-- MM
|                       |-- DD
|                           |-- Document
|                               |-- FILES
|           |-- Media
|               |-- YYYY
|                   |-- MM
|                       |-- DD
|                           |-- Identified
|                               |-- Camera Model
|                                   |-- IMAGES/VIDEOS
|                           |-- Unidentified
|                               |-- IMAGES/VIDEOS
|           |-- SystemImages
|               |-- YYYY
|                   |-- MM
|                       |-- DD
|                           |-- SystemImages
|                               |-- IMAGES
```

## Usage Instructions

Run the script by executing:

```bash
python macssd_organizer.py
```
The console will display the list of detected external SSDs. Select the one you want to use for backup by typing its associated number. If you choose to format the SSD to exFAT, please make sure to back up any important data beforehand, as this operation is irreversible and will erase all existing data. Once you confirm, the script will start the copying and organizing process.

## Notes 

1. This script is designed exclusively for macOS and may not work correctly on other operating systems.
2. Ensuring the right permissions for the script to access the filesystem and perform operations is essential.
3. Formatting the SSD will erase all data on it. Make sure the data is backed up before proceeding.
4. The script deals with common file types but may skip unrecognized or uncommon file types.
   
## License  

This project is released under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contribution

Contributions for bug fixes, features, and improvements are welcome! You can create a pull request or open an issue on the [issues page](https://github.com/imhsouna/Mac-SSD-Organizer/issues) of this repository.

## Author

Maintained by [Hsouna Zinoubi](https://github.com/imhsouna).

## Acknowledgements

I'd like to thank the Python open-source community for their amazing modules. This script wouldn't have been possible without their contributions.

## Disclaimer

I am not responsible for any loss of data that might occur due to the use of this script. Please use it at your own risk. Always ensure to verify your backups and store them securely.

## Happy organizing!
