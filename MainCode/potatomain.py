from os import environ
import discord
from discord.ext import commands
from dotenv import load_dotenv

bot = commands.Bot(command_prefix = "pot ", intents = discord.Intents.all())
loaded = False

@bot.event
async def on_ready():
    global loaded
    if not loaded:
        bot.load_extension("cogs.teleport")
        bot.load_extension("cogs.primle")
        bot.load_extension("cogs.potato")
    loaded = True
    print("Ok")

if __name__ == '__main__':
    load_dotenv()
    bot.run(environ.get('BOT_TOKEN'))

