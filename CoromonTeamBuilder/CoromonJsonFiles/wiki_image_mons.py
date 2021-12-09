import re
import json
import requests
from bs4 import BeautifulSoup

with open('CoromonJsonFiles/coromon_mons.json','r') as f:
    mons = json.load(f)

for mon in mons.keys():
    mon_url = "https://coromon.fandom.com/wiki/" + mon
    mon_req = requests.get(mon_url)
    mon_soup = BeautifulSoup(mon_req.content,'html.parser')
    mon_img = mon_soup.find(class_='pi-image-thumbnail')['src']
    gif_url = re.findall(r'^.+\.gif', mon_img)[0]

    mons[mon]['gif'] = gif_url
    
with open('CoromonJsonFiles/coromon_mons.json' ,'w') as f:
    json.dump(mons, f, indent=4)