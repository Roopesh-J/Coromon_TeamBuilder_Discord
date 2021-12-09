import json
import requests
from bs4 import BeautifulSoup

trait_id = 0
traits_list = {}

url = "https://coromon.fandom.com/wiki/Traits#List_of_Traits"
req = requests.get(url)

soup = BeautifulSoup(req.content,'html.parser')
trait_table = soup.find_all('tbody')[0]
traits = trait_table.find_all('tr')[1:]

for trait in traits:
    details = [detail for detail in trait.stripped_strings]
    trait_id += 1
    traits_list[details[0]]={
        'id':trait_id,
        'Type':details[1],
        'Description':details[2],
        'Condition':None,
        'Effect':None,
        'Coromon':details[3:] #, (if i want this for later, add a comma to previous line)
    }

with open('coromon_traits.json' ,'w') as f:
    json.dump(traits_list, f, indent=4)
