import math
import discord
import itertools
from corovert import coro_files

LVL = 25
EMBED_COLOR = 0x2d3034
MONS, ITEMS, SKILLS, TRAITS = coro_files()

class Coromon:
    id_iter = itertools.count(1)
    
    def __init__(self, slot, name, trait, skills, item=None):
        self.slot = slot
        self.id = next(Coromon.id_iter)
        self.name = name 
        self.trait = trait
        self.skills = skills
        self.item = item
        self.raw = statconvert(MONS[name]['BST'])
        self.stats = {}
        self.update_stats()

    def edit(self,Trainer,trait=None,skills=None,item=None):
        if trait:
            self.trait = trait
        if skills:    
            self.skills = skills
        if item:            
            self.item = item
        self.summary(Trainer,edit=True)
        
    def summary(self,Trainer,edit=False):
        try: # updates summary
            if edit:
                raise Exception
            else:
                self.summ.set_field_at(0, 
                    name="**Stats**\n", 
                    value='' + '\n'.join(f'**{k}**: {v}' for k,v in self.stats.items()) + '', 
                    inline=True
                    )
            self.summ.set_footer(text=f'Coromon {self.slot}/{Trainer.team_size}')
        except: # makes summary
            summary=discord.Embed(
                title=f'Lvl.{LVL} **{self.name}**',
                description=f'**Trait**: {self.trait}\n**Item**: {self.item}',
                color=EMBED_COLOR
            )
            summary.set_author(name = Trainer.name,icon_url = Trainer.icon)
            summary.add_field(
                name="Stats", 
                value='' + '\n'.join(f'**{k}**: {v}\u3000' for k,v in self.stats.items()) + '', 
                inline=True
                )
            summary.add_field(
                name="Skills", 
                value='' + '\n'.join(self.skills) + '', 
                inline=True
                )
            summary.set_image(url=MONS[self.name]['gif'])
            summary.set_footer(text=f'Coromon {self.slot}/{Trainer.team_size}')

            self.summ =  summary
        finally:
            if edit:
                return
            else:
                return self.summ
        
    def update_stats(self):
        for k,v in self.raw.items():
            self.stats[k] = sum(v)
        
    def set_potential(self,stat,value):
        self.raw[stat][1] = value
        self.update_stats()

def statconvert(bst):
    real = {}
    for name,value in bst.items():
        if name == 'HP': base = 10 + LVL
        elif name == 'SP': base = 20
        else: base = 5
        
        real[name] = [base + math.floor((LVL/99) * value),0]
        
    return real 