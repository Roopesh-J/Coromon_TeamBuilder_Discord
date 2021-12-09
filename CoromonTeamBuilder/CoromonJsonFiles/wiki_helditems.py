import json
import requests
from bs4 import BeautifulSoup

items_list = {}

url = "https://coromon.fandom.com/wiki/Items#Held_Items"
req = requests.get(url)

soup = BeautifulSoup(req.content,'html.parser')
items_table = soup.find_all('tbody')[3]
header = items_table.find('a', string='Fruits').find_parent('tr')

for item in header.next_siblings:
    if item == '\n':
        continue
    details = [detail for detail in item.stripped_strings]
    items_list[details[0]]={
        'Description':' '.join(details[1:4]),
        'Condition':None,
        'Effect':None
    }
    
with open('coromon_helditems.json' ,'w') as f:
    json.dump(items_list, f, indent=4)
