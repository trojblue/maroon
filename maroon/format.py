import os
import re


def _rename_folders(directory:str):
    # list all folders in the directory
    folders = [
        f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))
    ]

    # filter out folders containing underscore
    folders_to_rename = [f for f in folders if "_" not in f]

    # sort folders
    folders_to_rename.sort()

    # rename folders
    for i, folder in enumerate(folders_to_rename, start=1):
        old_folder_path = os.path.join(directory, folder)
        new_folder_path = os.path.join(directory, f"DISC{i}")
        os.rename(old_folder_path, new_folder_path)

    print(f"Renamed {len(folders_to_rename)} folders.")


def format_music_folder(dir_name):
    print(f"Tidying directory: {dir_name}")
    _rename_folders(dir_name)


if __name__ == "__main__":
    folder = input("Enter folder name: ")
    format_music_folder(folder)
