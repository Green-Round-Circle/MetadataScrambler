images = ["png","jpeg","jpg","tiff","heic","heif","cr2","nef","arw","dng"]
video_audio = ["mp4","mov","mkv","avi","mp3","flac","wav","ogg","aac"]
documents = ["pdf","docx","doc","docs","xlsx","pptx","ppt","odt","ods","rtf","epub"]
archive = ["zip","rar","7z","tar","gz","iso"]

images_mime = {
    "image/png",
    "image/jpeg",
    "image/tiff",
    "image/heic",
    "image/heif",
    "image/x-canon-cr2",
    "image/x-nikon-nef",
    "image/x-sony-arw",
    "image/dng",
}

video_audio_mime = {
    "video/mp4",
    "video/quicktime",  
    "video/x-matroska", # mkv
    "video/x-msvideo",  # avi
    "audio/mpeg",       # mp3
    "audio/flac",
    "audio/wav",
    "audio/ogg",
    "audio/aac",
    "audio/x-wav"
}

documents_mime = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",  # docx
    "application/msword",  # doc
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",  # xlsx
    "application/vnd.ms-excel",  # xls
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",  # pptx
    "application/vnd.ms-powerpoint",  # ppt
    "application/rtf",
    "application/epub+zip",
}

archives_mime = {
    "application/zip",
    "application/x-rar-compressed",
    "application/x-7z-compressed",
    "application/x-tar",
    "application/gzip",
    "application/x-iso9660-image",
}

EDITABLE_IMAGE_TAGS = {
    "CameraID",
    "FlashIntensity",
    "ManualFlashStrength",
    "WriterName",
    "ReaderName",
    # ---- EXIF ----
    "EXIF:Artist",
    "EXIF:Copyright",
    "EXIF:UserComment",
    "EXIF:ImageDescription",
    "EXIF:Software",
    "EXIF:DateTimeOriginal",
    "EXIF:CreateDate",
    "EXIF:ModifyDate",
    "EXIF:Make",
    "EXIF:Model",
    "EXIF:Software",
    "EXIF:UserComment",
    "EXIF:Orientation",
    "EXIF:GPSLatitude",
    "EXIF:GPSLongitude",
    "EXIF:GPSAltitude",
    "EXIF:GPSVersionID",
    "EXIF:FocalLength",
    "EXIF:Flash",
    "EXIF:DateTimeOriginal",
    "EXIF:CreateDate",
    "EXIF:ISO",
    "EXIF:ExposureTime",

    # ---- XMP ----
    "XMP:CreatorTool",
    "XMP:CreateDate",
    "XMP:ModifyDate",
    "XMP:MetadataDate",
    "XMP:Author",
    "XMP:Description",
    "XMP:Label",
    "XMP:Rating",

    # ---- IPTC ----
    "IPTC:By-line",
    "IPTC:CopyrightNotice",
    "IPTC:ObjectName",
    "IPTC:Caption-Abstract",
}

EDITABLE_VIDEO_AUDIO_TAGS = {
    "Title",
    "Artist",
    "Album",
    "Genre",
    "Track",
    "Comment",
    "Description",
    "Copyright",
    "EncodedBy",
    "CreationDate",
    "ModifyDate",
}
EDITABLE_DOCUMENT_TAGS = {
    "Title",
    "Author",
    "Subject",
    "Keywords",
    "Creator",
    "Producer",
    "CreateDate",
    "ModifyDate",
    "Description",
    "DocInfo:Title",
    "DocInfo:Author",
    "DocInfo:Subject",
    "DocInfo:Keywords",
    "DocInfo:CreateDate",
    "DocInfo:ModifyDate",
    "CreatorTool"
}
EDITABLE_ARCHIVE_TAGS = {
    "Comment",
    "CreateDate",
    "ModifyDate",
}
