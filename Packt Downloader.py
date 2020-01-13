import sys
import os
import shutil
from pathlib import Path
from datetime import datetime
import subprocess


PACKT_BOOKS_DOWNLOAD_PATH = "C:/Users/Jake/OneDrive - rit.edu/Documents/Tech Books/Packt Daily Download Script Files/Tmp Download"
PACKT_BOOKS_FINAL_PATH = "C:/Users/Jake/OneDrive - rit.edu/Documents/Tech Books/Free/Packt Free"


def grab_name(download_path):
    """
    Think about grabbing this information from the Log File. That's the only source that seems to always be right.
    """
    file_name = ""
    for curr_dir, dirs, files in os.walk(download_path):
        for file in files:
            tmp_file_name = os.path.splitext(file)[0]
            if tmp_file_name != file_name and file_name != "":
                logger("ERROR", "probably have more than one book in the tmp download folder")
                exit_code(1)
            else:
                file_name = tmp_file_name
    file_name = file_name.replace("_", " ")
    file_name = file_name.replace("Hands On", "Hands-On")
    return file_name


def erase_folder_contents(folder):
    logger("WARNING", "Erasing all files in " + str(folder))
    for curr_dir, dirs, files in os.walk(folder):
        for file in files:
            logger("WARNING", "Erasing " + file)
            os.remove(folder / file)


def rename_files(folder, name):
    for curr_dir, dirs, files in os.walk(folder):
        for file in files:
            file_name_extension = os.path.splitext(file)[1]
            old_name = str(file)
            new_name = ""

            if file_name_extension == ".zip":
                new_name = name + " Code Files" + file_name_extension
            else:
                new_name = name + file_name_extension

            logger("WARNING", "Renaming File")
            logger("INFO", "Old file name: " + old_name)
            logger("INFO", "New file name: " + new_name)
            os.rename(folder / old_name, folder / new_name)


def move_files(download_path, final_path, name):    
    # Check to see is the book is already there
    book_folder = final_path / name
    if book_folder.exists():
        logger("WARNING", " \"" + name + "\" is already in the Tech Books folder")
        erase_folder_contents(download_path)
        exit_code(1)
    else:
        os.mkdir(book_folder)

    # Move Files
    for curr_dir, dirs, files in os.walk(download_path):
        for file in files:
            shutil.move(download_path / file, book_folder / file)


def exit_code(exit_number):
    logger("EXITING", "")
    exit(exit_code)


def logger(log_type, message):
    log_file_path = Path("C:/Users/Jake/OneDrive - rit.edu/Documents/Tech Books/Packt Daily Download Script Files/Packt Downloader.log")
    with open(log_file_path, "a") as log_file:
        if (message == "\n"):
            log_file.write("\n")
        elif (log_type == "EXITING"):
            log_file.write(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + " [" + log_type + "]")
        else:    
            log_file.write(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + " - [" + log_type + "] - " + message + "\n")


def main ():
    logger(None, "\n")
    logger("INFO", "Starting Script")

    # Change Script Directory
    script_dir = Path("C:/Users/Jake/OneDrive - rit.edu/Documents/Tech Books/Packt Daily Download Script Files")
    os.chdir(script_dir)

    # Run packt-cli
    cmd = "packt-cli --grabd --status_mail 2> \"C:/Users/Jake/OneDrive - rit.edu/Documents/Tech Books/Packt Daily Download Script Files/Packt Downloader Errors.log\""
    logger("INFO", "Running the following command: " + cmd)
    subprocess.call(cmd, shell=True)
    logger("INFO", "Finished packt-cli")

    logger("INFO", "Starting my code")

    # Set Variables
    download_path = Path(PACKT_BOOKS_DOWNLOAD_PATH)
    final_path = Path(PACKT_BOOKS_FINAL_PATH)

    # Get File Name
    file_name = grab_name(download_path)

    # Rename Files
    rename_files(download_path, file_name)

    # Move Files to Desired Directory
    move_files(download_path, final_path, file_name)

    logger("INFO", "Finished my code")


main()