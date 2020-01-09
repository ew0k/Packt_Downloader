import sys
import os
import shutil
from pathlib import Path
from datetime import datetime
import subprocess


PACKT_BOOKS_DOWNLOAD_PATH = "C:/Users/Jake/OneDrive - rit.edu/Documents/Tech Books/Packt Daily Download Script Files/Tmp Download"
PACKT_BOOKS_FINAL_PATH = "C:/Users/Jake/OneDrive - rit.edu/Documents/Tech Books/Free/Packt Free"


def grab_name(download_path):
    file_name = ""
    for curr_dir, dirs, files in os.walk(download_path):
        for file in files:
            tmp_file_name = os.path.splitext(file)[0]
            if tmp_file_name != file_name and file_name != "":
                logger("ERROR: probably have more than one book in the tmp download folder")
                exit(1)
            else:
                file_name = tmp_file_name
    return file_name


def erase_folder_contents(folder):
    logger("Erasing all files in: " + str(folder))
    for curr_dir, dirs, files in os.walk(folder):
        for file in files:
            logger("Erasing: " + file)
            os.remove(folder / file)


def rename_files(folder, name):
    for curr_dir, dirs, files in os.walk(folder):
        for file in files:
            file_name_extension = os.path.splitext(file)[1]
            if file_name_extension == ".zip":
                os.rename(folder / file, str(folder / name) + " Code Files" + file_name_extension)


def move_files(download_path, final_path, name):
    """
    1) copy all files in tmp_path into final_path with the new name
    2) append "Code Files" to .zip file
    3) check to make sure the book isn't already there and erase tmp folder if it is
    """
    
    # Check to see is the book is already there
    book_folder = final_path / name
    if book_folder.exists():
        logger("ERROR: \"" + name + "\" is already in the Tech Books folder")
        erase_folder_contents(download_path)
        logger("EXITING")
        exit(1)
    else:
        os.mkdir(book_folder)

    # Rename all files in the downloads directory
    rename_files(download_path, name)

    # Move Files
    for curr_dir, dirs, files in os.walk(download_path):
        for file in files:
            shutil.move(download_path / file, book_folder / file)


def logger(message):
    log_file_path = Path("C:/Users/Jake/OneDrive - rit.edu/Documents/Tech Books/Packt Daily Download Script Files/run-scrips-log.txt")
    with open(log_file_path, "a") as log_file:
        log_file.write(datetime.now().strftime("%H:%M:%S") + " " + message + "\n")


def main ():
    logger("\n")
    #Grab Books
    script_dir = Path("C:/Users/Jake/OneDrive - rit.edu/Documents/Tech Books/Packt Daily Download Script Files")
    os.chdir(script_dir)
    logger("Current directory: " + os.getcwd())
    cmd = "packt-cli --grabd --status_mail >> \"C:/Users/Jake/OneDrive - rit.edu/Documents/Tech Books/Packt Daily Download Script Files/run-scrips-log.txt\" 2> \"C:/Users/Jake/OneDrive - rit.edu/Documents/Tech Books/Packt Daily Download Script Files/run-scrips-error-log.txt\""
    # cmd = "ipconfig >> \"C:/Users/Jake/OneDrive - rit.edu/Documents/Tech Books/Packt Daily Download Script Files/run-scrips-log.txt\" 2> \"C:/Users/Jake/OneDrive - rit.edu/Documents/Tech Books/Packt Daily Download Script Files/run-scrips-error-log.txt\""
    logger("Running this cmd: " + cmd)
    os.system(cmd)
    logger("Finished packt-cli")

    logger("Starting my code")
    # Set Variables
    download_path = Path(PACKT_BOOKS_DOWNLOAD_PATH)
    final_path = Path(PACKT_BOOKS_FINAL_PATH)

    # Move Files
    file_name = grab_name(download_path)
    move_files(download_path, final_path, file_name)
    logger("Finished my code")


main()