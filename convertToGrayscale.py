from pathlib import Path
from PIL import Image
from sys import argv
from getopt import getopt
from os.path import exists

safety = True
first = True
NAMING = 'g-'
QUALITY = 98

def convert(img_path) -> None:
    global safety, first
    if(img_path.name in exclude or img_path.stem in exclude):
        print(f'Skipping {img_path.name},')
        return
    try:
        img = Image.open(img_path).convert('L')
        newpath = f'{img_path.parent}/{NAMING}{img_path.name}'
        if exists(newpath) and safety:
            print(f"{newpath} already exists, overwrite it?")
            ask = input("Type the letter 'y' to continue or anything else to skip this file, alternatively use CTRL+C to exit the program")
            if ask == 'y'and first:
                    first = False
                    ask = input("Overwrite future files without asking? type 'y' to enable this feature or anything else to continue as normal")
                    if ask == 'y': safety = False
            else: 
                print(f'Skipping {img_path.name},')
                return
        img.save(newpath,quality=QUALITY,optimize=True)
        print(f'Converted {img_path},')
    except Exception as e:
        print(f'Failed to convert file {img_path}, error thrown:')
        print(e)
        print('Continuing...')

path = Path(r"C:/PythonCode/") if len(argv) < 2 else Path(argv[1])
exclude = {name[1] for name in getopt(argv[2:],"x:")[0]}

images: list = [p for p in path.glob("*") if p.suffix in {'.png', '.jpg', '.jpeg', '.webp', '.jfif', '.jif'} and p.stem[:2] != NAMING]

for filepath in images:
    convert(filepath)