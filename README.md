# snort
This command line program sorts images by renaming them to their date of creation.

# Usage
Specify the directory which you want to sort:
```
python snort.py ~/some_directory
```
# Features
* Supports .png, .jpeg and .jpg extensions, uppercase included.
* Recursively goes through directories.
* Checks for EXIF data in images, if it doesn't find EXIF data, snort renames the image to the date of creation or date of modification.
* Multiple images created at the same time get treated as duplicates, these duplicates get incremented by +1 in the filename, in order to preserve the images without deleting them.
* Works on Linux, should also work on Windows and MacOS.
