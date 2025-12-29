import filetype
import exiftool
import tabulate
import pypdf
import constants
import random
import string
import re
def print_in_table(metadata):
    table = [(i+1, k, v) for i, (k, v) in enumerate(metadata.items())]
    print(tabulate.tabulate(table, headers=["No.", "Tag", "Value"]))  

def normalize_pypdf_metadata(pdfMeta):
    normalized = {}
    if not pdfMeta:
        return normalized
    for k, v in pdfMeta.items():
        key = k.lstrip("/")
        normalized[f"pypdf:{key}"] = str(v)
    return normalized


def filter_editable(metadata, editable_tags):
    editable = {}
    for k, v in metadata.items():
        tag = k.split(":")[-1]
        if k in editable_tags or tag in editable_tags:
            editable[k] = v
    return editable


def print_editable_table(editable_meta):
    rows = []
    for i, (k, v) in enumerate(editable_meta.items(), 1):
        rows.append((i, k, str(v)))
    rows.append(("-", "e / q", "Exit editor"))
    print(tabulate.tabulate(rows, headers=["#", "Tag", "Value"]))


def write_metadata(file, tag,new_value):
    with exiftool.ExifTool() as et:
        et.execute(
            f"-{tag}={new_value}".encode(),
            b"-overwrite_original",
            file.encode()
        )

def edit_user_input(file,editable,editable_tags,mime):
    print("Keep in mind that some tags are read-only, so even if it says the update was successful, always double-check using the read function.")
    while True:
        choice = input(
            "\nSelect field number to edit "
            "(e/q/0/x to exit): "
        ).strip().lower()

        if choice in ("e", "q", "0", "exit","quit","x"):
            print("Exiting metadata editor.")
            break
        if not choice.isdigit():
            print("Invalid input. Please enter a number or 'e' to exit.")
            continue
        index = int(choice) - 1
        keys = list(editable.keys())
        if index < 0 or index >= len(keys):
            print("Selection out of range.")
            continue
        tag = keys[index]               
        current_value = editable[tag]
        print(f"\nEditing {tag}")
        print(f"Current value: {current_value}")
        new_value = input("New value (leave empty to cancel): ").strip()
        if new_value == "":
            print("Edit cancelled.")
            continue
        try:
            write_metadata(file, tag, new_value)
            print("Metadata updated successfully.")
        except Exception as e:
            print(f"Failed to write metadata: {e}")
            continue
        with exiftool.ExifToolHelper() as et:
            metadata = et.get_metadata([file])[0]
        editable = filter_editable(metadata,editable_tags)
        if not editable:
            print("No editable metadata fields found")
            return
        print_editable_table(editable)

def delete_metadata(file, tags):
    with exiftool.ExifToolHelper() as et:
        args = []
        for tag in tags:
            args.append(f"-{tag}=")
        et.execute(*args, file)

def delete_all_editable(file, metadata, editable_tags):
    tags_to_delete = []
    filtered_list = filter_editable(metadata,editable_tags)
    for tag in filtered_list:
        if tag in metadata:
            tags_to_delete.append(tag)

    if not tags_to_delete:
        print("No editable metadata found.")
        return
    print("The following tags will be deleted:")
    for t in tags_to_delete:
        print(f" - {t}")
    confirm = input("Proceed? (y/n): ").lower()
    if confirm != "y":
        print("Cancelled.")
        return
    delete_metadata(file, tags_to_delete)
    print("Deletion attempted\n")
    with exiftool.ExifToolHelper() as et:
            metadata = et.get_metadata([file])[0]
    editable = filter_editable(metadata,editable_tags)
    if not editable:
        print("No editable metadata fields found")
        return
    print_editable_table(editable)

def scramble_editable_metadata(file,editable_metadata):
    new_values  = []
    datetime_regex = re.compile(r"^\d{4}:\d{2}:\d{2}(\s\d{2}:\d{2}:\d{2}([+-]\d{2}:\d{2})?)?$")
    for tag, value in editable_metadata.items():
        if value is None:
            continue
        else:
            if isinstance(value, str) and datetime_regex.match(value):
                time_scrambled = ""
                for c in value:
                    if c.isdigit():
                        time_scrambled += str(random.randint(0, 9))
                    else:
                        time_scrambled += c
                scrambled = time_scrambled
            elif isinstance(value, str):
                scrambled = ''.join(random.choices(string.ascii_letters + string.digits, k=len(value)))
            elif isinstance(value, (int, float)):
                scrambled = str( max(1, int(value)))
            else:
                scrambled = "lol"
            print(f"Scrambling {tag}: {value} -> {scrambled}")
            new_values.append(f"{str(scrambled)}")
            if not new_values:
                print("Nothing to scramble")
            else:
                for new in new_values:
                    with exiftool.ExifTool() as et:
                        et.execute(
                            f"-{tag}={new}".encode(),
                            b"-overwrite_original",
                            file.encode()
                        )
    print("Done scrambling, recheck the metadata.")
    with exiftool.ExifToolHelper() as et:
            metadata_list = et.get_metadata([file])
    metadata = metadata_list[0]
    print_in_table(metadata)


def rscramble_editable_metadata(file,editable_metadata):
    new_values  = []
    datetime_regex = re.compile(r"^\d{4}:\d{2}:\d{2}(\s\d{2}:\d{2}:\d{2}([+-]\d{2}:\d{2})?)?$")
    for tag, value in editable_metadata.items():
        if value is None:
            continue
        else:
            if isinstance(value, str) and datetime_regex.match(value):
                time_scrambled = ""
                for c in value:
                    if c.isdigit():
                        time_scrambled += str(random.randint(0, 9))
                    else:
                        time_scrambled += c
                scrambled = time_scrambled
            elif isinstance(value, str):
                scrambled = ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(0,max(1,len(value)))))
            elif isinstance(value, (int, float)):
                scrambled = str(random.randint(0, max(1, int(value))))
            else:
                scrambled = "lol"
            print(f"Random scrambling {tag}: {value} -> {scrambled}")
            new_values.append(f"{str(scrambled)}")
            if not new_values:
                print("Nothing to scramble")
            else:
                for new in new_values:
                    with exiftool.ExifTool() as et:
                        et.execute(
                            f"-{tag}={new}".encode(),
                            b"-overwrite_original",
                            file.encode()
                        )
    print("Done random scrambling, recheck the metadata.")
    with exiftool.ExifToolHelper() as et:
            metadata_list = et.get_metadata([file])
    metadata = metadata_list[0]
    print_in_table(metadata)
    

def read_meta(file,identity,exifPath):
    mime = identity[1]
    exiftool.constants.DEFAULT_EXECUTABLE = exifPath
    if mime in constants.images_mime:
        with exiftool.ExifToolHelper() as et:
            metadata_list = et.get_metadata([file])
        metadata = metadata_list[0]
        print_in_table(metadata)

    elif mime in constants.video_audio_mime:
        with exiftool.ExifToolHelper() as et:
            metadata_list = et.get_metadata([file])
        metadata = metadata_list[0]
        print_in_table(metadata)
        
    elif mime in constants.documents_mime:
        with exiftool.ExifToolHelper() as et:
            metadata_list = et.get_metadata([file])
        metadata = metadata_list[0]
        if mime == "application/pdf":
            pdfMeta = pypdf.PdfReader(file).metadata
            pdfMetaNorm = normalize_pypdf_metadata(pdfMeta)
            metadata = {**metadata, **pdfMetaNorm}
        print_in_table(metadata)

    elif mime in constants.archives_mime:
        with exiftool.ExifToolHelper() as et:
            metadata_list = et.get_metadata([file])
        metadata = metadata_list[0]
        print_in_table(metadata)
    else:
        print(f"The MIME type is not known in the list")


def scramble_meta(file,identity,exifPath):
    mime = identity[1]
    exiftool.constants.DEFAULT_EXECUTABLE = exifPath
    if mime in constants.images_mime:
        with exiftool.ExifToolHelper() as et:
            metadata_list = et.get_metadata([file])
        metadata = metadata_list[0]
        editable = filter_editable(metadata,constants.EDITABLE_IMAGE_TAGS)
        if not editable:
            print("No editable metadata fields found")
            return
        print_editable_table(editable)
        scramble_editable_metadata(file,editable)
    elif mime in constants.video_audio_mime:
        with exiftool.ExifToolHelper() as et:
            metadata_list = et.get_metadata([file])
        metadata = metadata_list[0]
        editable = filter_editable(metadata,constants.EDITABLE_VIDEO_AUDIO_TAGS)
        if not editable:
            print("No editable metadata fields found")
            return
        print_editable_table(editable)
        scramble_editable_metadata(file,editable)
        
    elif mime in constants.documents_mime:
        with exiftool.ExifToolHelper() as et:
            metadata_list = et.get_metadata([file])
        metadata = metadata_list[0]
        editable = filter_editable(metadata,constants.EDITABLE_DOCUMENT_TAGS)
        if not editable:
            print("No editable metadata fields found")
            return
        print_editable_table(editable)
        scramble_editable_metadata(file,editable)

    elif mime in constants.archives_mime:
        with exiftool.ExifToolHelper() as et:
            metadata_list = et.get_metadata([file])
        metadata = metadata_list[0]
        editable = filter_editable(metadata,constants.EDITABLE_ARCHIVE_TAGS)
        if not editable:
            print("No editable metadata fields found")
            return
        print_editable_table(editable)
        scramble_editable_metadata(file,editable)
        
    else:
        print(f"The MIME type is not known in the list")

    

def rscramble_meta(file,identity,exifPath):
    mime = identity[1]
    exiftool.constants.DEFAULT_EXECUTABLE = exifPath
    if mime in constants.images_mime:
        with exiftool.ExifToolHelper() as et:
            metadata_list = et.get_metadata([file])
        metadata = metadata_list[0]
        editable = filter_editable(metadata,constants.EDITABLE_IMAGE_TAGS)
        if not editable:
            print("No editable metadata fields found")
            return
        print_editable_table(editable)
        rscramble_editable_metadata(file,editable)
    elif mime in constants.video_audio_mime:
        with exiftool.ExifToolHelper() as et:
            metadata_list = et.get_metadata([file])
        metadata = metadata_list[0]
        editable = filter_editable(metadata,constants.EDITABLE_VIDEO_AUDIO_TAGS)
        if not editable:
            print("No editable metadata fields found")
            return
        print_editable_table(editable)
        rscramble_editable_metadata(file,editable)
        
    elif mime in constants.documents_mime:
        with exiftool.ExifToolHelper() as et:
            metadata_list = et.get_metadata([file])
        metadata = metadata_list[0]
        editable = filter_editable(metadata,constants.EDITABLE_DOCUMENT_TAGS)
        if not editable:
            print("No editable metadata fields found")
            return
        print_editable_table(editable)
        rscramble_editable_metadata(file,editable)

    elif mime in constants.archives_mime:
        with exiftool.ExifToolHelper() as et:
            metadata_list = et.get_metadata([file])
        metadata = metadata_list[0]
        editable = filter_editable(metadata,constants.EDITABLE_ARCHIVE_TAGS)
        if not editable:
            print("No editable metadata fields found")
            return
        print_editable_table(editable)
        rscramble_editable_metadata(file,editable)
        
    else:
        print(f"The MIME type is not known in the list")


def delete_meta(file,identity,exifPath):
    mime = identity[1]
    exiftool.constants.DEFAULT_EXECUTABLE = exifPath
    if mime in constants.images_mime:
        with exiftool.ExifToolHelper() as et:
            metadata_list = et.get_metadata([file])
        metadata = metadata_list[0]
        delete_all_editable(file,metadata,constants.EDITABLE_IMAGE_TAGS)
    elif mime in constants.video_audio_mime:
        with exiftool.ExifToolHelper() as et:
            metadata_list = et.get_metadata([file])
        metadata = metadata_list[0]
        delete_all_editable(file,metadata,constants.EDITABLE_VIDEO_AUDIO_TAGS)
    elif mime in constants.documents_mime:
        with exiftool.ExifToolHelper() as et:
            metadata_list = et.get_metadata([file])
        metadata = metadata_list[0]
        delete_all_editable(file,metadata,constants.EDITABLE_DOCUMENT_TAGS)
    elif mime in constants.archives_mime:
        with exiftool.ExifToolHelper() as et:
            metadata_list = et.get_metadata([file])
        metadata = metadata_list[0]
        delete_all_editable(file,metadata,constants.EDITABLE_ARCHIVE_TAGS)
    else:
        print(f"The MIME type is not known in the list")



def edit_meta(file,identity,exifPath):
    mime = identity[1]
    exiftool.constants.DEFAULT_EXECUTABLE = exifPath
    if mime in constants.images_mime:
        with exiftool.ExifToolHelper() as et:
            metadata_list = et.get_metadata([file])
        metadata = metadata_list[0]
        editable = filter_editable(metadata,constants.EDITABLE_IMAGE_TAGS)
        if not editable:
            print("No editable metadata fields found")
            return
        print_editable_table(editable)
        edit_user_input(file,editable,constants.EDITABLE_IMAGE_TAGS,mime)
    elif mime in constants.video_audio_mime:
        with exiftool.ExifToolHelper() as et:
            metadata_list = et.get_metadata([file])
        metadata = metadata_list[0]
        editable = filter_editable(metadata,constants.EDITABLE_VIDEO_AUDIO_TAGS)
        if not editable:
            print("No editable metadata fields found")
            return
        print_editable_table(editable)
        edit_user_input(file,editable,constants.EDITABLE_VIDEO_AUDIO_TAGS,mime)
        
    elif mime in constants.documents_mime:
        with exiftool.ExifToolHelper() as et:
            metadata_list = et.get_metadata([file])
        metadata = metadata_list[0]
        editable = filter_editable(metadata,constants.EDITABLE_DOCUMENT_TAGS)
        if not editable:
            print("No editable metadata fields found")
            return
        print_editable_table(editable)
        edit_user_input(file,editable,constants.EDITABLE_DOCUMENT_TAGS,mime)

    elif mime in constants.archives_mime:
        with exiftool.ExifToolHelper() as et:
            metadata_list = et.get_metadata([file])
        metadata = metadata_list[0]
        editable = filter_editable(metadata,constants.EDITABLE_ARCHIVE_TAGS)
        if not editable:
            print("No editable metadata fields found")
            return
        print_editable_table(editable)
        edit_user_input(file,editable,constants.EDITABLE_ARCHIVE_TAGS,mime)
    else:
        print(f"The MIME type is not known in the list")

