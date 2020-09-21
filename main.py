
import os
import json
from zipfile import ZipFile
# import PIL
from PIL import Image

def getConfig(name):
    with open(name, "r") as configFile:
        data = configFile.read()
    return json.loads(data)

def traverse(directory):
    for path, dirlist, filelist in os.walk(directory):
        for file_name in filelist:
                test = file_name.split('/')
                yield (path, test[-1])

def traverseZip(fileName, filePath, jsonObject):
    zippedObject = ZipFile(filePath+'/'+fileName)
    for file in zippedObject.namelist():
        if not file[-1] == '/': # You don't need to process directories
            with zippedObject.open(file) as f:
                print('zip')
                jsonObject = process_file(file, filePath, f, jsonObject)
    return jsonObject

def splitPathFileName(fileName, filePath):
    line = filePath+'/'+fileName
    drive, filePath = os.path.splitdrive(line)
    filePath, fileName = os.path.split(filePath)
    return (fileName, filePath)

def create_json():
    return {}

def check_thumbnail():
    return False

def add_tags():
    return ['','']

def process_file(fileName, filePath, openFile, json):
    fileName, filePath = splitPathFileName(fileName,filePath)
    add_file_to_Json(fileName, filePath, json)
    if not check_thumbnail():
        create_thumbnail(fileName, filePath, openFile)
    else:
        add_tags()
    return json

def add_file_to_Json(fileName, filePath, json):
    print({'path': filePath.replace(defaults['startingDirectory'],''), "name":fileName})
    json[filePath+'/'+fileName] = \
    {
     "path": filePath.replace(defaults['startingDirectory'],''),
     "name":fileName,
     "tags":[]
    }
    return json

def create_thumbnail(fileName, file_path, file=None):
    #Create a directory if it doesn't exist already:
    new_path = file_path.replace(defaults['startingDirectory'],'')
    create_directory(new_path)
    print(file)
    image = Image.open(file) if file else Image.open(file_path+'/'+fileName)
    maxSize = (defaults['thumnailSize'],defaults['thumnailSize'])
    image.thumbnail(maxSize)
    image.save(new_path+'/'+fileName)
    pass

def create_directory(filePath):
    try:
        os.makedirs(defaults['thumbNailDirectory']+filePath+'/')
        return
    except FileExistsError:
        return

def do_work(filePath,fileName, json):
    if '.zip' in fileName:
        json = traverseZip(fileName, filePath, json)
    elif '.png' in fileName:
        # Open fileName
        json = process_file(fileName, filePath, None, json)
    return json

def start():
    startingJson = create_json()
    for file in traverse(defaults.get('startingDirectory')):
        startingJson = do_work(file[0], file[1], startingJson)
    with open(defaults['jsonOutput'], 'w') as results:
        results.write(json.dumps(startingJson))

print(Image.VERSION)
defaults = getConfig('config.json')
start()
