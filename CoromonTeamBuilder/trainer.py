import discord
from mon import Coromon
from mon import MONS, ITEMS
from corovert import coro_files

EMBED_COLOR = 0x2d3034

class Trainer:
    def __init__(self, user):
        self.id = user.id
        self.name = user.name
        self.icon = str(user.avatar_url)
        self.team = []
        self.team_size = 0

    def team_view(self):
        summary=discord.Embed(
            title='Your Team', 
            color=EMBED_COLOR, 
        ) 
        summary.set_author(name=f'{self.name}', icon_url=self.icon)
        for Coromon in self.team:
            summary.add_field(
                name=f'__**{Coromon.name}**__',
                value=f'''
                **Item: **{Coromon.item}\u3000
                **Skills:**\n'''+'\n'.join(skill+'\u3000' for skill in Coromon.skills)+"\n\u200b", 
                inline=True
        )
        return summary

    def quick_addMon(self, coroset):
        if setcheck(*coroset):
            self.team_size += 1
            self.team.append(Coromon(self.team_size,coroset[0],coroset[1],coroset[3:],coroset[2]))
        else:
            raise ValueError 
        
    def addMon(self,name=None,trait=None,skills=None,item=None):
        self.team_size += 1
        self.team.append(Coromon(self.team_size,name,trait,skills,item))   
        
    def removeMon(self, slot):
        flag = True
        for Coromon in self.team:
            if Coromon.slot == slot and flag:
                remove_mon = Coromon
                flag = False
            elif not flag:
                Coromon.slot -= 1
                
        self.team.remove(remove_mon)
        self.team_size -= 1
        return remove_mon.name       

def setcheck(name, trait, item, *skills): 
    
    if name not in MONS.keys():
        return False
    elif trait not in MONS[name]['Traits']:
        return False
    elif item not in ITEMS.keys():
        return False
    elif not set(skills).issubset(set(MONS[name]['Skills'])):
        return False
    else:
        return True