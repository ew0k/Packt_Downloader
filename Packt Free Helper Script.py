import sys
import os
import shutil
from pathlib import Path


PACKT_BOOKS_DOWNLOAD_PATH = "D:/OneDrive - rit.edu/Documents/Tech Books/Packt Daily Download Script Files/Tmp Download"
PACKT_BOOKS_FINAL_PATH = "D:/OneDrive - rit.edu/Documents/Tech Books/Free/Packt Free"


def grab_name(download_path):
    file_name = ""
    for curr_dir, dirs, files in os.walk(download_path):
        for file in files:
            tmp_file_name = os.path.splitext(file)[0]
            if tmp_file_name != file_name and file_name != "":
                # print("Error: probably have more than one book in the tmp download folder")
                exit(1)
            else:
                file_name = tmp_file_name
    return file_name


def erase_folder_contents(folder):
    # print("Erasing all files in:", folder)
    for curr_dir, dirs, files in os.walk(folder):
        for file in files:
            # print("Erasing:", file)
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
        # print("Book is already there")
        erase_folder_contents(download_path)
        exit(1)
    else:
        os.mkdir(book_folder)

    # Rename all files in the downloads directory
    rename_files(download_path, name)

    # Move Files
    for curr_dir, dirs, files in os.walk(download_path):
        for file in files:
            shutil.move(download_path / file, book_folder / file)


def main ():
    # Set Variables
    download_path = Path(PACKT_BOOKS_DOWNLOAD_PATH)
    final_path = Path(PACKT_BOOKS_FINAL_PATH)

    # Move Files
    file_name = grab_name(download_path)
    move_files(download_path, final_path, file_name)
    
main()