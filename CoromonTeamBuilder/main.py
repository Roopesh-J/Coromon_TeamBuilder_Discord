import os
import traceback
import pickle
from discord.ext import commands
from discord_ui import UI

bot = commands.Bot(command_prefix='.')
ui = UI(bot)

@bot.event
async def on_ready():
    with open('Master/master.pkl','rb') as f:
        try:
            bot.master = pickle.load(f)
            print('Master successfully loaded')
        except:
            trace_why = traceback.format_exc()
            print(f'Failed to load:\n{trace_why}')
            bot.master = {}
    print(f'{bot.user} is online!')

@bot.event
async def on_disconnect():
    with open('Master/master.pkl','wb') as f:
        try:
            pickle.dump(bot.master,f)
            print('Master succesfully dumped')
        except:
            trace_why = traceback.format_exc()
            print(f'Failed to dump:\n{trace_why}')
    print(f'{bot.user} is offline!')
    
@bot.command()
@commands.is_owner()
async def load(ctx,ext):
    '''Loads cogs (dev only)'''
    try:
        bot.load_extension(f'cogs.{ext}')
    except:
        trace_why = traceback.format_exc()
        await ctx.send(f"```Failed to load:{ext}.py\n\n{trace_why}```")
    else:
        await ctx.send(f"```Loaded:{ext}.py```")

@bot.command()
@commands.is_owner()
async def unload(ctx,ext):
    '''Unloads cogs (dev only)'''
    try:
        bot.unload_extension(f'cogs.{ext}')
    except:
        trace_why = traceback.format_exc()
        await ctx.send(f"```Failed to unload:{ext}.py\n\n{trace_why}```")
    else:
        await ctx.send(f"```Unloaded:{ext}.py```")

@bot.command()
@commands.is_owner()
async def reload(ctx):
    '''Reloads all cogs (dev only)'''
    summary = ''
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            try:
                bot.unload_extension(f'cogs.{filename[:-3]}')
                bot.load_extension(f'cogs.{filename[:-3]}')
            except Exception as err:
                summary += f'Failed to reload:{filename}\n-{err}\n\n'
            else:
                summary += f'Reloaded:{filename}\n\n'
    await ctx.send(f"```diff\n{summary}```")

@bot.command()
@commands.is_owner()
async def off(ctx):
    '''Toaster baths the bot (dev only)'''
    await bot.close()

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

bot.run("ODk5Mzg0MzM0MzI5NDcwOTk2.YWx-7w.Ya4ETgkYHccgawIpD55X63nVsYg")