import os
import shutil

path = str(input("\
Give the filepath you want to look for non-MP3 files\
\n(If you want to look on a USB/External Hard Drive: ea. D: or C:)\
\nFilepath: \
"))

exclusions = ["nonMP3", "System Volume Information", "VirtualDJ"]


def moveFile(filename, dirpath):
    if not os.path.exists(dirpath+r'\_nonMP3'):
        os.makedirs(dirpath+r'\_nonMP3')
    currentPath = os.path.join(dirpath, filename)
    newPath = os.path.join(dirpath+r'\_nonMP3', filename)
    try:
        os.rename(currentPath, newPath)
    except FileExistsError:
        print("File already in folder")


def deleteFile(filename, dirpath):
    deletePath = r"C:\Users\\" + os.getlogin() + "\Desktop"
    currentPath = os.path.join(dirpath, filename)
    newPath = os.path.join(deletePath, filename)
    try:
        shutil.move(currentPath, newPath)
    except FileExistsError:
        print("File already in folder")
    try:
        os.unlink(os.path.join(deletePath, filename))
    except:
        print("Failed to delete the file")
    print("File deleted")


def findFiles(path):
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
                        moveFile(filename, dirpath)
                    elif choice.upper() == "D":
                        deleteFile(filename, dirpath)
                    elif choice.upper() == "S":
                        exclusions.extend([filename])
                        print("File skipped")


def getNonMP3Folders(path):
    nonMP3Folders = []
    for dirpath, dirnames, filenames in os.walk(path):
        if "_nonMP3" in dirpath:
            print(dirpath)
            nonMP3Folders.extend([dirpath])
    return nonMP3Folders


def output(nonMP3Folders):
    print("Folders with non-MP3 files:\n")
    if nonMP3Folders == []:
        print("No folders with non-MP3 files")
    else:
        for dirpath in nonMP3Folders:
            print(dirpath)


findFiles(path)
nonMP3Folders = getNonMP3Folders(path)
output(nonMP3Folders)
