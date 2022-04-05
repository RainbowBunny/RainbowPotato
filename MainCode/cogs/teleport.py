import discord
from discord.ext import commands

RegionList = []
RegionList.append('region 1')
RegionList.append('region 2')

class Move(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name = "travel", help = "- Travel to a place")
    @commands.has_permissions(manage_roles = True)
    async def GoTo(self, ctx, *, area):
        area = area.lower()

        if area not in RegionList:
            await ctx.send('There is no such region.')
            return

        for discordrole in ctx.author.roles:
            if discordrole.name.lower() in RegionList:
                if discordrole.name.lower() == area:
                    await ctx.send("You are already in this region.")
                    return
                await ctx.author.remove_roles(discordrole)

        for ServerRole in ctx.guild.roles:
            if ServerRole.name.lower() == area:
                await ctx.author.add_roles(ServerRole)
        
        await ctx.send(f"Moved to {area}")

def setup(bot):
    bot.add_cog(Move(bot))
