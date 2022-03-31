from multiprocessing import managers
import discord

from discord.ext import commands

bot = commands.Bot(command_prefix = "pot ", intents = discord.Intents.all())

RegionList = []
RegionList.append('region 1')
RegionList.append('region 2')

@bot.event
async def on_ready():
    print("Ok")

@bot.command("goto")
@commands.has_permissions(manage_roles = True)
async def GoTo(ctx, *, area):
    if area.lower() not in RegionList:
        await ctx.send('There is no such region.')
        return

    for discordrole in ctx.author.roles:
        if discordrole.name.lower() in RegionList:
            if discordrole.name.lower() == area.lower():
                await ctx.send("You are already in this region.")
                return
            await ctx.author.remove_roles(discordrole)
    for ServerRole in ctx.guild.roles:
        if ServerRole.name.lower() == area.lower():
            await ctx.author.add_roles(ServerRole)
    await ctx.send(f"Moved to {area.lower()}")



bot.run('OTU4MjEyNDk2MTIzMTI5ODc2.YkKC7Q.hyzEAH1qR3oKUgLHth3gj_h6Coo')