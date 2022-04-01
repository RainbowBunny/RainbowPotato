import discord

from discord.ext import commands

bot = commands.Bot(command_prefix = "pot ", intents = discord.Intents().all())

"""

class Primle:

    def __init__(self):
"""

@bot.event
async def on_ready():
    print("Ready")


@bot.command(name = "potato")
async def potato(ctx):
    message = await ctx.send("Potato?")

    def c(m):
        return m.content == 'a'
    
    msg = await bot.wait_for('message', check = c)
    await ctx.send('Hello')

bot.run('OTU4MjEyNDk2MTIzMTI5ODc2.YkKC7Q.hyzEAH1qR3oKUgLHth3gj_h6Coo')
