import discord
from discord.ext import commands
from utils import Reader

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = Reader()
        self.data.add_file("data.json")
        self.data.loop()
    
    @commands.command(name = "profile")
    async def abc(self, ctx):
        self.data["data.json"][str(ctx.author.id)] = {"hp": 100}

def setup(bot):
    bot.add_cog(Test(bot))