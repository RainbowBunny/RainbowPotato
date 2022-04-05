import discord
from discord.ext import commands

class PVP(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def duel(self, ctx: commands.Context, player2: discord.Member) -> None:
        await ctx.send(f"{ctx.author.mention} is challenging {player2.mention}! (To be added)")

    @duel.error
    async def duel_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.BadArgument):
            return await ctx.send("Cannot found such user!")

def setup(bot: commands.Bot) -> None:
    bot.add_cog(PVP(bot))