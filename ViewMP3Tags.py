import os
import sys
from time import sleep

# 3rd party

from mutagen.easyid3 import EasyID3
import mutagen
from tabulate import tabulate

exclusions = ["ID3", "nonMP3", "System Volume Information", "VirtualDJ"]
ID3_tags = ['tracknumber', 'artist', 'title', 'album', 'discnumber']
all_mp3 = []


def start():
    path = input_user()
    print_mp3(path)


def correct_input(path, multi_disc):
    return os.path.exists(path) and multi_disc.upper() == "N" or os.path.exists(path) and multi_disc.upper() == "Y"


def print_mp3(path):
    get_mp3(path)
    list_mp3 = sorted(all_mp3, key=lambda x: int(x[0]))
    print(tabulate(list_mp3, headers=ID3_tags, tablefmt="orgtbl"))
    choice = str(input('Do you want to view another filepath? (Y/N): '))
    if choice.upper() == 'Y':
        cls()
        input_user()
    elif choice.upper() == 'N':
        close()


def load_mp3(dirpath, filename):
    try:
        mp3 = EasyID3(os.path.join(dirpath, filename))
    except mutagen.id3._util.ID3NoHeaderError:
        mp3 = {}
    return mp3


def has_tags(dirpath, filename):
    values = []
    mp3 = load_mp3(dirpath, filename)
    for tag_name in ID3_tags:
        try:
            values.extend([mp3[tag_name][0]])
        except KeyError:
            pass
    all_mp3.extend([values])


def get_mp3(path):
    print("Indexing files ", path, "...", sep='')
    file_id = 1
    for (dirpath, dirnames, filenames) in os.walk(path):
        if not any(exclusion in dirpath for exclusion in exclusions):
            total_files = len(filenames)
            for filename in filenames:
                print("Scanning file no. {0}/{1}: {2}".format(file_id, total_files, filename))
                _, fileext = os.path.splitext(filename)
                if fileext == ".mp3":
                    has_tags(dirpath, filename)
                file_id += 1


def input_user():
    cls()
    path = str(input("\
Give the filepath you want to look for MP3 files\
\n(If you want to look on a USB/External Hard Drive: ea. D: or C:)\
\nFilepath: "))

    multi_disc = input("\
Is the album a multi-disc album?\
\nChoice (Y/N): ")

    while not correct_input(path, multi_disc):
        print("You entered input that is not correct")
        path = str(input("\
Give the filepath you want to look for MP3 files\
\n(If you want to look on a USB/External Hard Drive: ea. D: or C:)\
\nFilepath: "))

        multi_disc = input("\
Is the album a multi-disc album?\
\nChoice (Y/N): ")

        if multi_disc.upper() == "N":
            ID3_tags.remove("discnumber")

        elif multi_disc.upper() == "Y" and "discnumber" not in ID3_tags:
            ID3_tags.extend(["discnumber"])
    return path


def close():
    print("The programm will be closed.")
    sleep(1)
    sys.exit()


def cls():
    os.system('CLS')

start()
