import discord
from discord.ext import commands

class ChallengeView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.result = 2

    @discord.ui.button(label = 'Accept', style = discord.ButtonStyle.green)
    async def accept(self, inter: discord.Interaction, button: discord.ui.Button):
        self.result = 1
        self.stop()

    @discord.ui.button(label = 'Decline', style = discord.ButtonStyle.red)
    async def decline(self, inter: discord.Interaction, button: discord.ui.Button):
        self.result = 0
        self.stop()

class PVP(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def duel(self, ctx: commands.Context, player2: discord.Member) -> None:
        confirm_view = ChallengeView()
        await ctx.send(f"{ctx.author.mention} challenged {player2.mention}!", view = confirm_view)
        await confirm_view.wait()

        await ctx.send(f"{player2.mention} {['declined', 'accepted', 'did not answer'][confirm_view.result]}!")

    @duel.error
    async def duel_error(self, ctx: commands.Context, error: commands.CommandError):
        if isinstance(error, commands.BadArgument):
            return await ctx.send("Cannot found such user!")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(PVP(bot))