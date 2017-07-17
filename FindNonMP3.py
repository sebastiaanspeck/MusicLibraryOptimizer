import os
import shutil

path = str(input("\
Give the filepath you want to look for non-MP3 files\
\n(If you want to look on a USB/External Hard Drive: ea. D: or C:)\
\nFilepath: \
"))

exclusions = ["nonMP3", "System Volume Information", "VirtualDJ"]


def move_file(filename, dirpath):
    if not os.path.exists(dirpath+r'\_nonMP3'):
        os.makedirs(dirpath+r'\_nonMP3')
    current_path = os.path.join(dirpath, filename)
    new_path = os.path.join(dirpath+r'\_nonMP3', filename)
    try:
        os.rename(current_path, new_path)
    except FileExistsError:
        print("File already in folder")


def delete_file(filename, dirpath):
    delete_path = r"C:\Users\\" + os.getlogin() + "\Desktop"
    current_path = os.path.join(dirpath, filename)
    new_path = os.path.join(delete_path, filename)
    try:
        shutil.move(current_path, new_path)
    except FileExistsError:
        print("File already in folder")
    try:
        os.unlink(os.path.join(delete_path, filename))
    except OSError:
        print("Failed to delete the file")
    print("File deleted")


def find_files():
    print("Indexing files ", path, "...", sep='')
    for (dirpath, dirnames, filenames) in os.walk(path):
        if not any(exclusion in dirpath for exclusion in exclusions):
            for filename in filenames:
                _, fileext = os.path.splitext(filename)
                if not fileext == ".mp3":
                    print(dirpath, ": ", filename, sep='')
                    choice = str(input("Press M to move the file\
\nPress D to delete the file\
\nPress S to skip the file\
\nChoice: "))
                    if choice.upper() == "M":
                        move_file(filename, dirpath)
                    elif choice.upper() == "D":
                        delete_file(filename, dirpath)
                    elif choice.upper() == "S":
                        exclusions.extend([filename])
                        print("File skipped")


def get_non_mp3_folders():
    non_mp3_folders = []
    for dirpath, dirnames, filenames in os.walk(path):
        if "_nonMP3" in dirpath:
            print(dirpath)
            non_mp3_folders.extend([dirpath])
    return non_mp3_folders


def output():
    print("Folders with non-MP3 files:\n")
    if not non_mp3_folders:
        print("No folders with non-MP3 files")
    else:
        for dirpath in non_mp3_folders:
            print(dirpath)


find_files()
non_mp3_folders = get_non_mp3_folders()
output()
