import discord
import asyncio
from random import randint
from discord.ext import commands

bot = commands.Bot(command_prefix = "pot ", intents = discord.Intents.all())
loaded = False

@bot.event
async def on_ready():
    global loaded
    if not loaded:
        await bot.load_extension("cogs.teleport")
        await bot.load_extension("cogs.primle")
        await bot.load_extension("cogs.potato")
    loaded = True
    print("Ok")

bot.run('OTU4MjEyNDk2MTIzMTI5ODc2.YkKC7Q.hyzEAH1qR3oKUgLHth3gj_h6Coo')

