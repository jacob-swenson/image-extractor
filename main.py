import os
import zipfile
import ntpath
import string

INPUT_FOLDER = 'input\\'
OUTPUT_FOLDER = 'output\\'
TRASH_FOLDER = 'trash\\'
ZIPS_FOLDER = 'zips\\'
EXTENSIONS_PATH = 'extensions.txt'
STRIPPERS_PATH = 'strippers.txt'
FILE_EXTENSIONS = [line.rstrip('\n') for line in open(EXTENSIONS_PATH)]
STRIPPERS = [line.rstrip('\n') for line in open(STRIPPERS_PATH)]
IMAGE_COUNT = 0


def setup():
    global INPUT_FOLDER, OUTPUT_FOLDER, TRASH_FOLDER, ZIPS_FOLDER
    if not os.path.exists(INPUT_FOLDER):
        print('Creating input folder')
        os.mkdir(INPUT_FOLDER)
    if not os.path.exists(OUTPUT_FOLDER):
        print('Creating output folder')
        os.mkdir(OUTPUT_FOLDER)
    if not os.path.exists(TRASH_FOLDER):
        print('Creating trash folder')
        os.mkdir(TRASH_FOLDER)
    if not os.path.exists(ZIPS_FOLDER):
        print('Creating zips folder')
        os.mkdir(ZIPS_FOLDER)
    if not os.path.isdir(INPUT_FOLDER) or not os.path.isdir(OUTPUT_FOLDER):
        print('input/ or output/ is not a folder. Quitting.')
        print('Take all your shit and put it together')
        exit(1)


def is_image(entry):
    for extension in FILE_EXTENSIONS:
        if entry.path.endswith(extension):
            print("Found one!!!: " + entry.name)
            return True
    return False


def move(source, destination):
    print("Moving " + (source if isinstance(source, str) else source.path) +
          " to " + (destination if isinstance(destination, str) else destination.path))
    if not os.path.exists(destination):
        os.rename(source, destination)
    else:
        increment = 0
        filename, extension = os.path.splitext(destination)
        while True:
            new_name = filename + '-' + str(increment) + extension
            if not os.path.exists(new_name):
                os.rename(source, new_name)
                return
            else:
                increment += 1


def get_images(path, prefix):
    global IMAGE_COUNT
    print("Looking for images in " + (path if isinstance(path, str) else path.path))
    prefix = prefix + ntpath.basename(path) + '_'
    for entry in os.scandir(path):
        if os.path.isdir(entry):
            get_images(entry, prefix)
            move(entry, TRASH_FOLDER + strip(prefix + entry.name))
        elif is_image(entry):
            IMAGE_COUNT += 1
            move(entry, OUTPUT_FOLDER + strip(prefix + entry.name))
        else:
            move(entry, TRASH_FOLDER + strip(prefix + entry.name))


def strip(name):
    for stripper in STRIPPERS:
        name = name.replace(stripper, '')
    name = name.lstrip(string.punctuation)
    return name


def unzip_folders(directory):
    for entry in os.scandir(directory):
        if entry.path.endswith('.zip'):
            name, extension = os.path.splitext(entry)
            zip_destination = name
            if not os.path.exists(zip_destination):
                os.mkdir(zip_destination)
            with zipfile.ZipFile(entry, 'r') as zip_ref:
                print("Unzipping " + entry.name + " to " + zip_destination)
                zip_ref.extractall(zip_destination)
            move(entry, ZIPS_FOLDER + entry.name)


def bordered_print(sentence):
    length = len(sentence) + 4
    print('*' * length)
    print('* ' + sentence + ' *')
    print('*' * length)


def run():
    global INPUT_FOLDER
    global IMAGE_COUNT
    bordered_print("Setting up folders")
    setup()
    bordered_print("Unzipping folders")
    unzip_folders(INPUT_FOLDER)
    bordered_print("Looking for images")
    get_images(INPUT_FOLDER, '')
    print()
    bordered_print("Found " + str(IMAGE_COUNT) + " images! They've been placed in the output folder.")


run()
