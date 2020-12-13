
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
                yield (path, file_name.split('/')[-1])

def traverseZip(fileName, filePath, jsonObject):
    zippedObject = ZipFile(filePath+'/'+fileName)
    for file in zippedObject.namelist():
        if not file[-1] == '/': # You don't need to process directories
            if '.png'in file or '.jpg' in file or '.jpeg' in file:
                with zippedObject.open(file) as f:
                    jsonObject = process_file(file, filePath, f, jsonObject)
    return jsonObject

def splitPathFileName(fileName, filePath):
    line = filePath+'/'+fileName
    drive, filePath = os.path.splitdrive(line)
    filePath, fileName = os.path.split(filePath)
    return (fileName, filePath)

def create_json():
    return {}

def check_thumbnail(file_name, file_path):
    new_path = file_path.replace(defaults['startingDirectory'],
                                 defaults['thumbNailDirectory']).replace(' ', '_')
    return os.path.exists(new_path+'/'+file_name.replace(' ','_'))

def add_tags():
    return ['','']

def process_file(fileName, filePath, openFile, json):
    fileName, filePath = splitPathFileName(fileName,filePath)
    add_file_to_Json(fileName, filePath, json)
    if not check_thumbnail(fileName, filePath):
        create_thumbnail(fileName, filePath, openFile)
    else:
        add_tags()
    return json

def add_file_to_Json(fileName, filePath, json):
    new_path = filePath.replace(defaults['startingDirectory'],'').replace(' ','_')
    path_parts = new_path.split('/')
    artist = path_parts[0]

    if not artist in json:
        json[artist] = {
            'base_objects' : [],
            'sub_objects': {},
            'sub_sub_objects': {}
        }
    if len(path_parts) == 2:
        subsection = path_parts[1]
        if not subsection in json[artist]['sub_objects']:
            json[artist]['sub_objects'][subsection] = []
        json[artist]['sub_objects'][subsection].append({
            "artist": artist,
            "subsection": subsection,
            "path": new_path,
            "name":fileName.replace(' ', '_'),
            "tags":[]
            })
        print(json[artist]['sub_objects'][subsection][-1])
    elif len(path_parts) > 2:
        subsubsection = path_parts[2]
        if not subsubsection in json[artist]['sub_sub_objects']:
            json[artist]['sub_sub_objects'][subsubsection] = []
        json[artist]['sub_sub_objects'][subsubsection].append({
            "artist": artist,
            "subsubsection": subsubsection,
            "path": new_path,
            "name":fileName.replace(' ', '_'),
            "tags":[]
            })
        print(json[artist]['sub_sub_objects'][subsubsection][-1])
    else:
        json[artist]['base_objects'].append({
            "artist": artist,
            "path": new_path,
            "name":fileName.replace(' ', '_'),
            "tags":[]
            })
        print(json[artist]['base_objects'][-1])
    return json

def create_thumbnail(fileName, file_path, file=None):
    new_path = file_path.replace(defaults['startingDirectory'],
                                 defaults['thumbNailDirectory']).replace(' ', '_')
    # Create a directory if it doesn't exist already:
    create_directory(new_path)
    try:
        image = Image.open(file) if file else Image.open(file_path+'/'+fileName)
        maxSize = (defaults['thumnailSize'],defaults['thumnailSize'])
        image.thumbnail(maxSize)
        image.save(new_path+'/'+fileName.replace(' ','_'))
    except:
        print(f"Error on:{fileName},{file_path}")

def create_directory(filePath):
    try:
        os.makedirs(filePath+'/')
        return
    except FileExistsError:
        return

def do_work(filePath,fileName, json):
    if '.zip' in fileName:
         json = traverseZip(fileName, filePath, json)
    elif '.png' in fileName or '.jpg' in fileName or '.jpeg' in fileName:
        json = process_file(fileName, filePath, None, json)
    return json

def start():
    startingJson = create_json()
    for file in traverse(defaults.get('startingDirectory')):
        startingJson = do_work(file[0], file[1], startingJson)
    with open(defaults['jsonOutput'], 'w') as results:
        results.write(json.dumps(startingJson))

defaults = getConfig('config.json')
start()
