from PIL import Image
from mon import MONS
import urllib.request


# background = Image.open('background.png')
# print(background.size)
# background=background.resize((800,440))
# background.show()

for k,v in MONS.items():
    link = v['gif']
    filename = k+'1f'
    urllib.request.urlretrieve(link, filename+'.gif')
    asset = Image.open(f'/Users/roopesh_m/Documents/Python/Coromon Battlesim/{filename}.gif')
    asset.convert('RGBA').save(filename+'.png')
# background.paste(asset,(20,20),asset)
# background.show()

