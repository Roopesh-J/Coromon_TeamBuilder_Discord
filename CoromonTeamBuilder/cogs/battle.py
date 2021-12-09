import math
import discord
from discord.ext import commands
from mon import SKILLS

class Battle(commands.Cog):
    """Coromon Battles!"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def d(self,ctx,slot1:int,skill1:int,slot2:int):
        Trainer = self.bot.master[ctx.message.author.id]
        Mon1 = Trainer.team[slot1-1]
        Mon2 = Trainer.team[slot2-1]
        skill = Mon1.skills[skill1 - 1]

        level = 25
        skill_power = SKILLS[skill]["Power"]
        a = Mon1.stats["Atk"]
        d = Mon2.stats["Def"]
        damage_dealt = self.damage(level,skill_power,a,d)
                                   
        embed= discord.Embed(
            title="testing damage"
        )
        embed.add_field(name="Coromon 1",value=f"{Mon1.name}\nLevel: 25\nSkill: {skill}\nSkill Power: {skill_power},Atk: {a}")
        embed.add_field(name="Coromon 2",value=f"{Mon2.name}\nLevel: 25\nDef: {d}")
        embed.add_field(name="Damage Dealt",value=damage_dealt,inline=False)
        await ctx.send(embed=embed)
    
    def damage(self,level,power,a,d):
        return math.floor((((((2*level)/5)+2)*(power)*(a/d))/50) + 2)
    
def setup(bot: commands.Bot):
    bot.add_cog(Battle(bot))