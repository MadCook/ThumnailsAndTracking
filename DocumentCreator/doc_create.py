from pylatex import Document, Section, Figure, SubFigure, NoEscape, Subsection, Subsubsection
import os
import json

def get_json(name):
    with open(name, "r") as configFile:
        data = configFile.read()
    return json.loads(data)

def breakUp(art,width):
    for i in range(0, len(art), width):
        yield art[i:i + width]

def importLinedFigures(doc, listImages):
    num = 0
    for artLine in breakUp(listImages, defaults.get('lineWidth')):
        num += 1
        with doc.create(Figure(position='H')) as line:
            for eachArt in artLine:
                with doc.create(SubFigure(
                    position='b',
                    width=NoEscape(r'0.2\linewidth'))) as image:
                    name = f'{defaults.get("thumbNailDirectory")}{eachArt["path"]}/{eachArt["name"]}'
                    print(name)
                    image.add_image(name, width=NoEscape(r'\linewidth'))
                    image.add_caption(f'{eachArt["name"][0:5]}')
                    if num % 5 ==0:
                        doc.append(NoEscape(r'\clearpage'))


def start():
    info = get_json(f"../{defaults.get('jsonOutput')}")

    doc = Document(default_filepath=defaults.get('pdfPath'))

    for artist, artistListStuff in info.items():
        with doc.create(Section(f'Artist: {artist}')):
            importLinedFigures(doc, artistListStuff['base_objects'])
        for subsection, subsectionList in artistListStuff['sub_objects'].items():
            with doc.create(Subsection(f'Folder: {subsection}')):
                importLinedFigures(doc, subsectionList)
            doc.append(NoEscape(r'\clearpage'))
        for subsubsection, subsubsectionList in artistListStuff['sub_sub_objects'].items():
            with doc.create(Subsubsection(f'Sub Folder: {subsubsection}')):
                importLinedFigures(doc, subsubsectionList)
        doc.append(NoEscape(r'\clearpage'))
    try:
        doc.generate_tex()
        doc.generate_pdf(clean_tex=False)
        print('done?')
    except Exception as e:
        print(f"OH NO")
        print(e)

if __name__ == '__main__':
    defaults = get_json('../config.json')
    start()
