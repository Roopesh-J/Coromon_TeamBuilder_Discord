import json

def coro_files():
    with open('CoromonJsonFiles/coromon_mons.json','r') as f:
        mons = json.load(f)
    with open('CoromonJsonFiles/coromon_helditems.json','r') as f:
        items = json.load(f)
    with open('CoromonJsonFiles/coromon_skills.json','r') as f:
        skills = json.load(f)
    with open('CoromonJsonFiles/coromon_traits.json','r') as f:
        traits = json.load(f)
    
    return mons, items, skills, traits