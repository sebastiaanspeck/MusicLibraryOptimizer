import os

exclusions = []
counter = {"Duplicate files": 0, }


def get_user_input():
    path1 = str(input("Give the first filepath: "))
    path2 = str(input("Give the second filepath: "))
    return path1, path2


def find_files(path):
    print("Indexing files ", path, "...", sep='')
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f)) and
             not any(exclusion in path for exclusion in exclusions) and f.endswith('.mp3')]
    return files


def compare_files(files1, files2):
    print("Comparing files...")
    files12 = []
    for filename in files1:
        if filename in files2:
            files12.extend([filename])
    for filename in files2:
        if filename in files1:
            files12.extend([filename])
    files12 = set(files12)
    return files12


def print_result(files12):
    print("\nREPORT:\n")
    output = sorted(files12)
    if not output:
        print("No duplicate files were found")
    else:
        for file in output:
            print("The following file is duplicated:", file)
            counter["Duplicate files"] += 1
    for k, v in counter.items():
        print(k, ': ', v, sep='')
    input("\nPress any key to exit...")


def main():
    path1, path2 = get_user_input()
    files1 = find_files(path1)
    files2 = find_files(path2)
    files12 = compare_files(files1, files2)
    print_result(files12)


main()
