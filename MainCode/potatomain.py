import discord
from random import randint
from discord.ext import commands

bot = commands.Bot(command_prefix = "pot ", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print("Ok")

bot.load_extension("cogs.role_editor")
bot.load_extension("cogs.test")
bot.run('OTU4MjEyNDk2MTIzMTI5ODc2.YkKC7Q.hyzEAH1qR3oKUgLHth3gj_h6Coo')