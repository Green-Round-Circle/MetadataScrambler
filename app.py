import filetype
import argparse
import os
import platform
import sys
from actions import (
    read_meta,
    scramble_meta,
    rscramble_meta,
    delete_meta,
    edit_meta
)
def get_exifPath():
    try:
        system = platform.system()
        base = os.path.join(os.path.dirname(__file__), "exiftool")
        if system == "Windows":
            path = os.path.join(base, "Windows", "exiftool(-k).exe")
        elif system == "Linux":
            path = os.path.join(base, "Linux", "exiftool")
        else:
            raise RuntimeError(f"Unsupported OS: {system}")
        if not os.path.isfile(path):
            raise FileNotFoundError(path)
        return path
    except Exception as e:
        print("ExifTool could not be loaded. Please check if it matches the name exiftool and is in the same directory")
        sys.exit(0)


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("InputFile", help="Input file")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-r", "--read", action="store_true", help="Read metadata")
    group.add_argument("-s", "--scramble", action="store_true", help="Scramble metadata (same size)")
    group.add_argument("-sr", "--rscramble", action="store_true", help="Scramble metadata (random size)")
    group.add_argument("-d", "--delete", action="store_true", help="Delete metadata")
    group.add_argument("-e", "--edit", action="store_true", help="Edit metadata")
    group.add_argument("-x", "--exit", action="store_true", help="Exit program")
    args = parser.parse_args()
    return args

def get_choice_from_args(args):
    if args.read:
        return "r"
    if args.scramble:
        return "s"
    if args.delete:
        return "d"
    if args.edit:
        return "e"
    if args.rscramble:
        return "sr"
    if args.exit:
        print("Exiting...")
        sys.exit(0)
    return None

def file_identifier(name_of_file):
    if not os.path.isfile(name_of_file):
        print(f"Input file does not exist: {name_of_file}")
        return 
    kind = filetype.guess(name_of_file)
    if kind is None:
        print('Cannot guess file type!')
        return
    return kind.extension,  kind.mime

def print_FileType(extension,mime):
    print(f"File extension: {extension}")
    print(f"File MIME type: {mime}")

def choice_wizard():
    print("Select action:")
    print("  r  - read metadata")
    print("  s  - scramble metadata (same size)")
    print("  sr - scramble metadata (random size)")
    print("  d  - delete metadata")
    print("  e  - edit metadata")
    print("  x  - exit")
    while True:
        choice = input("\nYour choice: ").strip().lower()
        if choice in {"r", "s", "sr", "d", "e"}:
            return choice
        if choice in {"x", "exit"}:
            print("Exiting...")
            exit(0)
        print("Invalid option, try again.")

def file_worker(choice,inputFile,identity):
    exifPath = get_exifPath()
    match choice:
        case "r":
            read_meta(inputFile,identity,exifPath)
        case "s":
            scramble_meta(inputFile,identity,exifPath)
        case "sr":
            rscramble_meta(inputFile,identity,exifPath)
        case "d":
            delete_meta(inputFile,identity,exifPath)
        case "e":
            edit_meta(inputFile,identity,exifPath)
        case _:
            print("Something is wrong")
def main():
    args = parser()
    choice =  get_choice_from_args(args)
    inputFile = args.InputFile
    identity = file_identifier(inputFile)
    if not identity:
        return
    print_FileType(identity[0],identity[1])
    if not choice:
        choice = choice_wizard()
    choice = choice.lower()
    file_worker(choice,inputFile,identity)



if __name__ == '__main__':
    main()
