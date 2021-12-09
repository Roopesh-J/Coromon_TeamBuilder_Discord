import discord
from discord.ext import commands
from mon import MONS, TRAITS, SKILLS, ITEMS

EMBED_COLOR = 0x2d3034

class Misc(commands.Cog):
    """Miscellanous commands"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.command()
    async def ping(self,ctx):
        '''
        Just a command to see your latency to the bot, honestly I don't know why it's here but why not.
        '''
        await ctx.send(f'Hey {ctx.author.name}! :ping_pong: {round(self.bot.latency * 1000)}ms!')
    
    @commands.command()
    async def info(self,ctx, *,query):
        '''
        Shows information for any trait,skill,item, or coromon. The info is not much and is just what is stored locally. 
        If the query does not make a match, and wiki search is done and the link is returned and is abled to be clicked. 
        The link is completely harmless and is just a link to the wiki search of the query. 
        Note: Not case sensitive
        Example: '.query Swurmy'
        '''
        query = query.strip().title()
        if query in MONS.keys():
            info = MONS[query]
            embed = discord.Embed(
                title=query,
                description=f'**Type**: {info["Type"]}',
                color=EMBED_COLOR
            )
            embed.add_field(
                name=f'__Traits__',
                value='\n'.join(f'{trait}' for trait in info['Traits']),
                inline=False
            )
            embed.add_field(
                name=f'__Base Stats__',
                value='\n'.join(f'**{k}**: {v}' for k,v, in info['BST'].items()),
                inline=True
            )
            embed.add_field(
                name=f'__Skills__',
                value='\n'.join(f'{skill}' for skill in info['Skills']),
                inline=True
            )
            embed.set_image(url=info['gif']) 
        elif query in TRAITS.keys():
            info = TRAITS[query]
            embed = discord.Embed(
                title=query,
                description=f'**Type**: {info["Type"]}',
                color=EMBED_COLOR
            )
            embed.add_field(
                name='__Description__',
                value=info["Description"],
                inline=False
            )
            embed.add_field(
                name=f'__Coromon__',
                value='\n'.join(info['Coromon']),
                inline=False
            )
        elif query in SKILLS.keys():
            info = SKILLS[query]
            embed=discord.Embed(
                title=query,
                color=EMBED_COLOR
            )
            embed.add_field(
                name='__Description__',
                value=info['Description'],
                inline=False
            )
            embed.add_field(
                name='__Details__',
                value=f'''
                    **Type**: {info["Type"]}
                    **Category**: {info["Ctgry"]}
                    **Contact**: {'Yes' if info["Contact"] == 1 else 'No'}
                    **Priority**: {info["Priority"]}
                '''
            )
            embed.add_field(
                name=f'__Stats__',
                value=f'''
                    **Power**: {info['Power']}
                    **Accuracy**: {info['Acc.']}
                    **SP**: {info['SP']}
                '''
            )
        elif query in ITEMS.keys():
            info = ITEMS[query]
            embed=discord.Embed(
                title=query,
                color=EMBED_COLOR
            )
            embed.add_field(
                name="__Description__",
                value=info['Description']
            )
        try:
            embed.url=f"https://coromon.fandom.com/wiki/{query.replace(' ','_')}"
        except:
            embed=discord.Embed(
                title=f'Wiki search for {query}',
                color=EMBED_COLOR
            )
            query = query.replace(' ','+').replace(',','%2C')
            embed.url = f"https://coromon.fandom.com/wiki/Special:Search?query={query}&scope=internal&contentType=&ns%5B0%5D=0#"
        finally:
            embed.set_author(name=self.bot.user.name,icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
              
def setup(bot: commands.Bot):
    bot.add_cog(Misc(bot))