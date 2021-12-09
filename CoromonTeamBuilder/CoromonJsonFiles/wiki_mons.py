import json
import requests
from bs4 import BeautifulSoup

mons_list = {}

url = "https://coromon.fandom.com/wiki/List_of_Coromon"
req = requests.get(url)

soup = BeautifulSoup(req.content,'html.parser')
mons_table = soup.find_all('tbody')[0]
mons = mons_table.find_all('tr')[2:]

with open('CoromonJsonFiles/coromon_bst.json','r') as f:
    bst_master = json.load(f)

for mon in mons:
    details = [detail for detail in mon.stripped_strings]
    if details[2] != '*':
        continue
    
    name = details[1]
    bst = bst_master[name]
    bst_name = details[4:15:2]
    
    mons_list[name]= {
        'id':int(details[0]),
        'Type':details[3],
        'BST':{
            bst_name[0]:bst[0], # HP
            bst_name[2]:bst[2], # ATK
            bst_name[3]:bst[3], # DEF
            bst_name[4]:bst[4], # Sp.ATK
            bst_name[5]:bst[5], # Sp.DEF
            'Spe':bst[6],       # Speed
            'SP':34             # SP
        },
        'Traits':[],
        'Skills':[]
    }
    
with open('coromon_mons.json' ,'w') as f:
    json.dump(mons_list, f, indent=4)