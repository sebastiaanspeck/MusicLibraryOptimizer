import os
import sys
import string
from time import sleep

# 3rd party

from mutagen.easyid3 import EasyID3
import mutagen

exclusions = ["ID3", "nonMP3", "System Volume Information", "VirtualDJ"]
ID3_tags = ['tracknumber', 'artist', 'title', 'album', 'discnumber']
all_ID3_tags = [tag for tag in EasyID3.valid_keys.keys()]


def start():
    path, multi_disc = input_user()
    mp3_actions(path, multi_disc)


def correct_input(path, multi_disc):
    return os.path.exists(path) and multi_disc.upper() == "N" or os.path.exists(path) and multi_disc.upper() == "Y"


def rename_file(dirpath, filename, correct_named_filename):
    old_name, new_name = os.path.join(dirpath, filename), os.path.join(dirpath, correct_named_filename)
    choice_rename = input("Do you want to renme {0} to {1}\
\nChoice (Y/N): ".format(filename, correct_named_filename))
    if choice_rename.upper() == "Y":
        try:
            os.rename(old_name, new_name)
            print("File is succesfully renamed")
        except OSError:
            print("File couldn't be renamed")
    else:
        print("User canceled to rename the file")
        return


def write_tag(tag_name, filename, mp3, multi_disc):
    if tag_name == "discnumber" and multi_disc.upper() == "N":
        return
    try:
        tag_value = input("Give the value for the tag: " + tag_name + " for the MP3: " + filename + "\
    \nValue: ")
        if tag_name == "tracknumber" or tag_name == "discnumber":
            int(tag_value)
        mp3[tag_name] = tag_value
        mp3.save()
        print("{0}-tag is succesfully changed to {1}".format(tag_name, tag_value))
    except KeyError:
        print("{0}-tag couldn't be written".format(tag_name))


def test_tag_capwords(tag_name, mp3):
    old = mp3[tag_name][0]
    try:
        if old != string.capwords(old):
            mp3[tag_name] = string.capwords(old)
            mp3.save()
            print("{0}-tag is succesfully changed from {1} to {2}".format(tag_name, old, mp3[tag_name][0]))
    except KeyError:
        print("{0}-tag couldn't be written".format(tag_name))


def delete_unused_tags(mp3):
    for tag in all_ID3_tags:
        try:
            if tag not in ID3_tags and mp3[tag]:
                del mp3[tag]
                mp3.save()
        # tag not in mp3
        except KeyError:
            pass


def load_mp3(dirpath, filename):
    try:
        mp3 = EasyID3(os.path.join(dirpath, filename))
    except mutagen.id3._util.ID3NoHeaderError:
        mp3 = {}
    return mp3


def correct_filename(filename, correct_named_filename):
    return correct_named_filename == filename


def has_tags(dirpath, filename, multi_disc):
    mp3 = load_mp3(dirpath, filename)
    for tag_name in ID3_tags:
        try:
            if mp3[tag_name]:
                if tag_name == "artist" or tag_name == "title":
                    test_tag_capwords(tag_name, mp3)
            else:
                write_tag(tag_name, filename, mp3, multi_disc)
        except KeyError:
            write_tag(tag_name, filename, mp3, multi_disc)
    correct_named_filename = mp3["artist"][0] + " - " + mp3["title"][0] + ".mp3"
    if not correct_filename(filename, correct_named_filename):
        rename_file(dirpath, filename, correct_named_filename)
    delete_unused_tags(mp3)


def mp3_actions(path, multi_disc):
    print("Indexing files ", path, "...", sep='')
    file_id = 1
    for (dirpath, dirnames, filenames) in os.walk(path):
        if not any(exclusion in dirpath for exclusion in exclusions):
            total_files = len(filenames)
            for filename in filenames:
                print("Scanning file no. {0}/{1}: {2}".format(file_id, total_files, filename))
                _, fileext = os.path.splitext(filename)
                if fileext == ".mp3":
                    has_tags(dirpath, filename, multi_disc)
                file_id += 1
    choice = str(input('Do you want to check another filepath? (Y/N): '))
    if choice.upper() == 'Y':
        cls()
        input_user()
    elif choice.upper() == 'N':
        close()


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
    return path, multi_disc


def close():
    print("The programm will be closed.")
    sleep(1)
    sys.exit()


def cls():
    os.system('CLS')

start()
