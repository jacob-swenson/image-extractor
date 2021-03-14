import os
import zipfile
import ntpath

INPUT_FOLDER = 'input\\'
OUTPUT_FOLDER = 'output\\'
TRASH_FOLDER = 'trash\\'
EXTENSIONS_PATH = 'extensions.txt'
STRIPPERS_PATH = 'strippers.txt'
FILE_EXTENSIONS = [line.rstrip('\n') for line in open(EXTENSIONS_PATH)]
STRIPPERS = [line.rstrip('\n') for line in open(STRIPPERS_PATH)]


def setup():
    if not os.path.exists(INPUT_FOLDER):
        print('Creating input folder')
        os.mkdir(INPUT_FOLDER)
    if not os.path.exists(OUTPUT_FOLDER):
        print('Creating output folder')
        os.mkdir(OUTPUT_FOLDER)
    if not os.path.exists(TRASH_FOLDER):
        print('Creating trash folder')
        os.mkdir(TRASH_FOLDER)
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
    print("Looking for images in " + (path if isinstance(path, str) else path.path))
    prefix = prefix + ntpath.basename(path) + '_'
    for entry in os.scandir(path):
        if os.path.isdir(entry):
            get_images(entry, prefix)
            move(entry, TRASH_FOLDER + prefix + entry.name)
        elif is_image(entry):
            move(entry, OUTPUT_FOLDER + prefix + entry.name)
        else:
            move(entry, TRASH_FOLDER + prefix + entry.name)


def strip(name):
    file, extension = os.path.splitext(name)
    output = file
    for stripper in STRIPPERS:
        output = output.replace(stripper, '')
    return output


def unzip_folders():
    directory = INPUT_FOLDER
    print('ZZZZZIIIIPPP')
    print('Unzipping your folders ;)')
    for entry in os.scandir(directory):
        if entry.path.endswith('.zip'):
            zip_destination = strip(entry)
            if not os.path.exists(zip_destination):
                os.mkdir(zip_destination)
            with zipfile.ZipFile(entry, 'r') as zip_ref:
                print("Unzipping " + entry.name + " to " + zip_destination)
                zip_ref.extractall(zip_destination)
            os.rename(entry, TRASH_FOLDER + entry.name)



setup()
unzip_folders()
get_images(INPUT_FOLDER, '')