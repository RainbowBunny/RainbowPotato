import discord
import asyncio
from random import randint
from discord.ext import commands

bot = commands.Bot(command_prefix = "pot ", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print("Ok")

bot.load_extension("cogs.teleport")
bot.load_extension("cogs.pvp")
#bot.load_extension("cogs.test")
bot.load_extension("cogs.primle")
bot.load_extension("cogs.game")
bot.run('OTU4MjEyNDk2MTIzMTI5ODc2.YkKC7Q.hyzEAH1qR3oKUgLHth3gj_h6Coo')

