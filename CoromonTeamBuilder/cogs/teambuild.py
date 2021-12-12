import pickle
import asyncio
import discord
from tabulate import tabulate
from asyncio.tasks import FIRST_COMPLETED
from trainer import Trainer
from mon import EMBED_COLOR, MONS, ITEMS, SKILLS, TRAITS
from discord.ext import commands
from discord_ui import Button, SelectMenu, SelectOption

class TeamBuild(commands.Cog, name="Team Building"):
    """Starting a team and adding/removing/editing Coromon"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        
    @commands.command()
    async def build(self,ctx):
        '''Creates a team for the user. This command must be run to use any of the other commands in this category.'''
        author = ctx.message.author
        if author.id in self.bot.master.keys():
            await ctx.send("You already have a team! Use `.add` to add a coromon to your team.")    
        else:
            self.bot.master[author.id] = Trainer(author)
            await ctx.send("A team was made for you! Use `.add` to add a coromon to your team.")
    
    @commands.command()
    async def quick(self, ctx, *, args):
        '''
        Old '.add' command. It is mainly just for testing to add coromon quickly.
        It is recommended to use the current '.add' command but to use this command,
        the inputs must be in the following format: '.quick coromon, trait, item, skill1, skill2, skill3, skill4
        '''
        author = ctx.message.author
        try:
            Trainer = self.bot.master[author.id]
        except KeyError:
            await ctx.send("You don't have a team yet! Use `.build` to start one.")
        else:
            if Trainer.team_size == 6:
                await ctx.send("You already have 6 coromon!")
            else:
                try:
                    coroset = list(map(str.strip,args.title().split(',')))
                except:
                    await ctx.send("Your input format is wrong!")
                else:
                    try:
                        Trainer.quick_addMon(coroset)
                    except ValueError:
                        await ctx.send(f'That coromon set is not allowed! (Check the trait, item, and/or skills)')
                    else:
                        await ctx.send(f'Your coromon was created and added to the team!')
    
    @commands.command()
    async def add(self, ctx, mon_name):
        '''
        New add function to add coromon. To add a coromon simply enter the name (mon_name) of the coromon after the function.
        You will then be prompted with options for a trait, set of skills, and item.
        Example: '.add Cubzero'
        '''
        author = ctx.message.author
        try:
            Trainer = self.bot.master[author.id]
            mon_name = mon_name.capitalize()
        except KeyError:
            await ctx.send("You don't have a team yet! Use `.build` to start one.")
        else:
            try:
                coromon = MONS[mon_name]
            except KeyError:
                await ctx.send(f"'{mon_name}' is not an existing coromon!")
            else:
                components_list = [
                    SelectMenu(
                            options=[SelectOption(
                                value=trait,
                                label=trait,
                                description=TRAITS[trait]['Description'][:100]) for trait in coromon['Traits']],
                            custom_id='t',
                            placeholder="Choose a trait",
                            max_values=1
                        ),
                    SelectMenu(
                        options=[SelectOption(
                            value=skill,
                            label=f"{skill} ({SKILLS[skill]['Type']})",
                            description=SKILLS[skill]['Description'][:100]) for skill in coromon['Skills']],
                        custom_id='s',
                        placeholder="Choose up to 4 skills",
                        max_values=4
                    ),
                    SelectMenu(
                        options=[SelectOption(
                            value=item,
                            label=f"{item}",
                            description=ITEMS[item]['Description'][:100]) for item in ITEMS.keys()],
                        custom_id='i',
                        placeholder="Choose an item (Optional)",
                        max_values=1
                    ),
                    Button(label = f"Add Coromon", emoji='\U00002714', custom_id = "c", color=3),
                    Button(label = f"Cancel Entry ", emoji='\U00002716', custom_id = "x", color=4)
                ]
                attr_option = await ctx.reply(f"Create a set for {mon_name} (will timeout after 30 secs of no activity):",components=components_list)
                trait_sel = None
                skills_sel = None
                item_sel = None
                confirm_flag = True
                while True:
                    components_list = [
                        SelectMenu(
                                custom_id='t',
                                placeholder="Choose a trait",
                                options=[SelectOption(
                                    value=trait,
                                    label=trait,
                                    description=TRAITS[trait]['Description'][:100]) for trait in coromon['Traits']],
                                max_values=1
                        ),
                        SelectMenu(
                            custom_id='s',
                            placeholder="Choose up to 4 skills",
                            options=[SelectOption(
                                value=skill,
                                label=f"{skill} ({SKILLS[skill]['Type']})",
                                description=SKILLS[skill]['Description'][:100]) for skill in coromon['Skills']],
                            max_values=4
                        ),
                        SelectMenu(
                        custom_id='i',
                        placeholder="Choose an item (Optional)",
                        options=[SelectOption(
                            value=item,
                            label=f"{item}",
                            description=ITEMS[item]['Description'][:100]) for item in ITEMS.keys()],
                        max_values=1
                        ),
                        Button(custom_id = "c", label = f"Add Coromon", emoji='\U00002714', color=3),
                        Button(custom_id = "x", label = f"Cancel Entry ", emoji='\U00002716', color=4)
                    ]
                    await self.bot.wait_until_ready()
                    try:
                        done, pending = await asyncio.wait([
                            asyncio.create_task(attr_option.wait_for("select",self.bot,by=author),name='select'),
                            asyncio.create_task(attr_option.wait_for("button",self.bot,by=author),name='button')
                        ],timeout=30,return_when=FIRST_COMPLETED)
                        if not done:raise asyncio.TimeoutError
                    except asyncio.TimeoutError:
                        await attr_option.disable_components(True)
                        await attr_option.edit("Timed out")
                        break
                    
                    for task in pending:
                        try:
                            task.cancel()
                        except asyncio.CancelledError:
                            pass
                    
                    finished : asyncio.Task = list(done)[0]
                    f_result = finished.result()
                    await f_result.respond(ninja_mode=True)
                    
                    match f_result.custom_id:
                        case 't':
                            trait_sel = f_result.selected_values[0]
                        case 's':
                            skills_sel = f_result.selected_values
                        case 'i':
                            item_sel = f_result.selected_values[0]
                        case 'c':
                            if all([trait_sel,skills_sel]):
                                Trainer.addMon(mon_name,trait_sel,skills_sel,item_sel)
                                await attr_option.edit(f"{mon_name} was added! Use `.summary {Trainer.team[-1].slot}` to view your mon",components=None)
                                break
                            else:
                                await ctx.send("Make sure to select a trait and atleast one skill")
                        case 'x':
                            await attr_option.disable_components(True)
                            await attr_option.edit("Cancelled!")
                            break
                    
    @commands.command()
    async def remove(self, ctx, slot:int=None):
        '''
        Removes a coromon from your team. To specify a coromon, you must enter its slot in the team.
        For example the first coromon in your team is the 1st slot, the second is the 2nd slot, etc. 
        The command may also be used without any slot in which case a dropdown menu can be used to select any coromon to remove. 
        Example: '.remove 4' (removes the 4th coromon in your team) 
        '''
        await self.bot.wait_until_ready()
        author = ctx.message.author
        try:
            Trainer = self.bot.master[author.id]
        except KeyError:
            await ctx.send("You don't have a team yet! Use `.build` to start one.")
        else:
            if slot:
                try:
                    removed_mon = Trainer.removeMon(slot)
                except:
                    await ctx.send('An invalid slot was entered!')
                else:
                    await ctx.send(f"{removed_mon} was removed from your team!")
            else:
                msg = await ctx.send(
                    "Choose a coromon (or wait 10 secs to cancel): ", 
                    components=[SelectMenu(options=self.team_menu(Trainer.team), max_values=1)]
                    )
                try:
                    sel = await msg.wait_for("select", self.bot, by=author, timeout=10)
                except asyncio.TimeoutError:
                    msg.disable_components(True)
                    await msg.edit("Cancelled")
                except:
                    await ctx.send('Your team is empty! Use `.add` to add a coromon to your team.')
                else:
                    removed_mon = Trainer.removeMon(int(sel.selected_values[0]))
                    await sel.respond(f"{removed_mon} was removed from your team!")

    @commands.command()
    async def edit(self,ctx,slot:int):
        '''
        Edits a coromon's trait, skillset, and item. To specify a coromon, you must enter its slot in the team.
        For example the first coromon in your team is the 1st slot, the second is the 2nd slot, etc.
        This command can also be accessed via the '.summary' command. There is an edit button under the summary page that will run this command.
        Ex: '.edit 4' (will edit the 4th coromon in your team)
        '''
        author = ctx.message.author
        try:
            Trainer = self.bot.master[author.id]
        except KeyError:
            await ctx.send("You don't have a team yet! Use `.build` to start one.")
        else:
            try:
                Mon = Trainer.team[slot-1]
                coromon = MONS[Mon.name]
            except:
                await ctx.send("An ivalid slot was entered!")
            else:
                components_list = [
                    SelectMenu(
                            options=[SelectOption(
                                value=trait,
                                label=trait,
                                description=TRAITS[trait]['Description'][:100]) for trait in coromon['Traits']],
                            custom_id='t',
                            placeholder="Choose a trait",
                            max_values=1
                        ),
                    SelectMenu(
                        options=[SelectOption(
                            value=skill,
                            label=f"{skill} ({SKILLS[skill]['Type']})",
                            description=SKILLS[skill]['Description'][:100]) for skill in coromon['Skills']],
                        custom_id='s',
                        placeholder="Choose up to 4 skills",
                        max_values=4
                    ),
                    SelectMenu(
                        options=[SelectOption(
                            value=item,
                            label=f"{item}",
                            description=ITEMS[item]['Description'][:100]) for item in ITEMS.keys()],
                        custom_id='i',
                        placeholder="Choose an item (Optional)",
                        max_values=1
                    ),
                    Button(label=f"Edit Coromon",custom_id="c",emoji='\U00002714',color=3),
                    Button(label=f"Cancel Edit\a",custom_id="x",emoji='\U00002716',color=4)
                ]
                attr_option = await ctx.reply(
                    f"Edit {Mon.name}'s set (will timeout after 15 secs of no activity):",
                    components=self.lock(components_list,Mon.trait,Mon.skills,Mon.item)
                )
                trait_sel = Mon.trait
                skills_sel = Mon.skills
                item_sel = Mon.item
                while True:
                    components_list = [
                        SelectMenu(
                            options=[SelectOption(
                                value=trait,
                                label=trait,
                                description=TRAITS[trait]['Description'][:100]) for trait in coromon['Traits']],
                            custom_id='t',
                            placeholder="Choose a trait",
                            max_values=1
                        ),
                        SelectMenu(
                            options=[SelectOption(
                                value=skill,
                                label=f"{skill} ({SKILLS[skill]['Type']})",
                                description=SKILLS[skill]['Description'][:100]) for skill in coromon['Skills']],
                            custom_id='s',
                            placeholder="Choose up to 4 skills",
                            max_values=4
                        ),
                        SelectMenu(
                        options=[SelectOption(
                            value=item,
                            label=f"{item}",
                            description=ITEMS[item]['Description'][:100]) for item in ITEMS.keys()],
                        custom_id='i',
                        placeholder="Choose an item (Optional)",
                        max_values=1
                        ),
                        Button(label=f"Edit Coromon",custom_id="c",emoji='\U00002714',color=3),
                        Button(label=f"Cancel Edit\a",custom_id="x",emoji='\U00002716',color=4)
                    ]
                    await self.bot.wait_until_ready()
                    try:
                        done, pending = await asyncio.wait([
                            asyncio.create_task(attr_option.wait_for("select",self.bot,by=author),name='select'),
                            asyncio.create_task(attr_option.wait_for("button",self.bot,by=author),name='button')
                        ],timeout=15,return_when=FIRST_COMPLETED)
                        if not done: raise asyncio.TimeoutError
                    except asyncio.TimeoutError:
                        await attr_option.disable_components(True)
                        await attr_option.edit("Timed out")
                    
                    for task in pending:
                        try:
                            task.cancel()
                        except asyncio.CancelledError:
                            pass
                    
                    finished : asyncio.Task = list(done)[0]
                    f_result = finished.result()
                    await f_result.respond(ninja_mode=True)
                    
                    match f_result.custom_id:
                        case 't':
                            trait_sel = f_result.selected_values[0]
                        case 's':
                            skills_sel = f_result.selected_values
                        case 'i':
                            item_sel = f_result.selected_values[0]
                        case 'c':
                            Mon.edit(Trainer,trait=trait_sel,skills=skills_sel,item=item_sel)
                            await attr_option.edit(f"{Mon.name}'s set was edited! Use `.summary {Mon.slot}` to view it",components=None)
                            break
                        case 'x':
                            await attr_option.disable_components(True)
                            await attr_option.edit("Cancelled!")
                            break

    @commands.command()
    async def points(self, ctx, slot:int):
        '''
        Sets a potential points distribution for each coromon.
        To specify a coromon, you must enter its slot in the team.
        For example the first coromon in your team is the 1st slot, the second is the 2nd slot, etc.
        The commands will display the current spread and then two dropdowns to set points. 
        Note: Points aren't 'added' they are just set. So if you select HP and 60, it sets HP to 60. 
        There is currently no way to reset the spread, but there will be. The dropdowns dissappear after 15 secs of no activity
        Example: '.points 6' (set points for the 6th, or last, coromon in your team)
        '''
        author = ctx.message.author
        try:
            Trainer = self.bot.master[author.id]
        except KeyError:
            await ctx.send("You don't have a team yet! Use `.build` to start one.")
        else:
            try:
                Mon = Trainer.team[slot-1]
            except :
                await ctx.send("An invalid slot was entered!")
            else: 
                def stats_embed():
                    table = [['', 'Stats', 'Points','Base']]
                    ptotal,btotal = 0,0
                    for k,v, in Mon.raw.items():
                        table.append([k,sum(v),v[1],v[0]])
                        ptotal += v[1]
                        btotal += v[0]
                    
                    if ptotal > 126:
                        raise ValueError
                    else:
                        t1 = tabulate(table, headers='firstrow',tablefmt='presto',numalign='center',stralign='left')
                        t1 = t1.replace('+','-').replace('-','─').replace('|',' ')
                        t1 += '\n────────────────────────────────────\n'
                        t1 += f" {'Total':<5} {ptotal+btotal:^9} {ptotal:^10} {btotal:^8}"
                        return f"```ml\n{t1}```"
                           
                stats = discord.Embed(
                    title=f"{Mon.name}'s stats breakdown",
                    description=stats_embed(),
                    color=EMBED_COLOR  
                )
                stats.set_footer(text='Will timeout after 15 seconds of no activity')
                    
                potential = await ctx.send(
                    embed=stats,
                    components=[
                        SelectMenu(
                            options=[SelectOption(k,k) for k in Mon.stats.keys()],
                            custom_id='s',
                            placeholder='Stat:',
                            max_values=1  
                        ),
                        SelectMenu(
                            options=[SelectOption(str(i),str(i)) for i in range(0,61,6)],
                            custom_id='p',
                            placeholder='Points:',
                            max_values=1
                        )
                    ]
                )
                stat_sel = None
                points_sel = None
                while True:
                    await self.bot.wait_until_ready()
                    try:
                        sel = await potential.wait_for("select",self.bot,by=author,timeout=15)
                    except asyncio.TimeoutError:
                        stats.set_footer(text='')
                        await potential.edit(embed=stats,components=None)
                        break
                   
                    await sel.respond(ninja_mode=True)

                    if sel.custom_id == 's':
                        stat_sel = sel.selected_values[0]
                    else:
                        points_sel = sel.selected_values[0]
                    
                    if stat_sel and points_sel:
                        try:
                            Mon.set_potential(stat_sel,int(points_sel))
                            stats.description = stats_embed()
                        except ValueError:
                            await potential.edit("You can only have 126 potential points total!")
                        else:
                            await potential.edit(embed=stats)
                        finally:
                            stat_sel = None
                            points_sel = None
                    
    @commands.command()
    async def summary(self, ctx, slot:int=None):
        '''
        Displays a summary page of a specific coromon. To specify a coromon, you must enter its slot in the team.
        For example the first coromon in your team is the 1st slot, the second is the 2nd slot, etc. 
        This comand can be also be used with no input and a dropdown will be given to select a coromon from your team. 
        With the summary, a few buttons are given to navigate between coromon in your team as well as quickly delete or edit the coromon
        Example: '.summary 2' (will show summary for the 2nd coromon in your team)
        '''
        author = ctx.message.author
        try:
            Trainer = self.bot.master[author.id]
        except KeyError:
            await ctx.send("You don't have a team yet! Use `.build` to start one.")
        else:
            if slot:  
                try:
                    Mon = Trainer.team[slot-1]
                except:
                    await ctx.send('An invalid slot was entered!')
                else:
                    padd = '\u202F' * 2 # wack ass formatting strats
                    padd2 = '\u3000\u00A0' + '\u202F' * 4 # wack strats continued
                    embed = Mon.summary(Trainer)    
                    msg = await ctx.send(embed=embed,components=[
                        [Button(f"{padd2}⟵{padd2}","-1",color=2),
                        Button(f"{padd2}⟶{padd2}","1",color=2)],
                        [Button(f'Edit{padd}Set{padd}','e',emoji='\U0001F4DD',color=1),
                        Button('Remove'+'\u00A0'*3,'x',emoji='\U00002716',color=4)]
                    ])
                    try:
                        btn = await msg.wait_for("button", self.bot, by=author, timeout=20)
                    except asyncio.TimeoutError:
                        await msg.edit(components=None)
                    else:
                        await msg.edit(components=None)
                        if btn.custom_id == 'x':
                            await self.remove(ctx,Mon.slot)
                        elif btn.custom_id == 'e':
                            await self.edit(ctx,Mon.slot)
                        elif btn.custom_id == '1' and slot == Trainer.team_size:
                            await self.summary(ctx,1)
                        else:
                            await self.summary(ctx,slot + int(btn.custom_id))
            else:
                try:
                    msg = await ctx.send(
                    "Choose a coromon (or wait 10 secs to cancel): ", 
                    components=[SelectMenu(options=self.team_menu(Trainer.team), max_values=1)]
                    )
                    sel = await msg.wait_for("select", self.bot, by=author, timeout=10)
                except asyncio.TimeoutError:
                    msg.disable_components(True)
                    await msg.edit('Cancelled!')
                except:
                    await ctx.send("Your team is empty! Use `.add` to add a coromon to your team.")
                else:
                    await sel.respond(ninja_mode=True)
                    await self.summary(ctx,int(sel.selected_values[0]))
                    
    @commands.command()
    async def team(self,ctx):
        '''
        Displays an overall summary page of the team. Has no input.
        '''
        try:
            Trainer = self.bot.master[ctx.message.author.id]
        except:
            await ctx.send("You don't have a team yet! Use `.build` to start one.")
        else:
            await ctx.send(embed=Trainer.team_view())

    @commands.command()
    @commands.is_owner()
    async def test(self,ctx):
        "Dev only"
        print(self.bot.master)
    
    def team_menu(self,team):
        return [SelectOption(coromon.slot,coromon.name,f'{coromon.trait}, {coromon.item}') for coromon in team]
    
def setup(bot: commands.Bot):
    bot.add_cog(TeamBuild(bot))