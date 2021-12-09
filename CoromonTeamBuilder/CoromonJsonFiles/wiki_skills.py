import json
import requests
from bs4 import BeautifulSoup

skill_id = 0
skills_list = {}

url = "https://coromon.fandom.com/wiki/Skills"
req = requests.get(url)

soup = BeautifulSoup(req.content,'html.parser')
skills = soup.find_all('tr')[1:]

for skill in skills:
    details = [detail for detail in skill.stripped_strings]
    
    try:
        skill_url = "https://coromon.fandom.com/wiki/" + details[0].replace(" ","_")
        skill_req = requests.get(skill_url)
        skill_soup = BeautifulSoup(skill_req.content,'html.parser')
        skill_desc= skill_soup.find_all('i')
        desc = skill_desc[0].string.strip('\"')
    except:
        desc = ''
 
    skill_id += 1
    skills_list[details[0]]={
        'id':skill_id,
        'Type':details[1].rstrip('Type').strip(),
        'Ctgry':details[5],
        'SP':int(details[2]),
        'Power':(0 if details[3] == '-' else int(details[3])),
        'Acc.':(0 if details[4] == '-' else int(details[4])),
        'Contact':(0 if details[6] == 'no' else 1),
        'Priority':None,
        'Effect':None,
        'Description':desc
    }

with open('coromon_skills2.0.json' ,'w') as f:
    json.dump(skills_list, f, indent=4)
