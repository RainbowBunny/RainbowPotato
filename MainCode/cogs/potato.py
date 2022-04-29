import discord
import random
import time
import asyncio

from discord.ext import commands
from utils import Reader

from game import game_handler as Game
from game import objects

class Potato(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_message = dict()

    @commands.command(
        help = "add skill command for admin ?"
    )
    async def addskill(self, ctx, member: discord.Member, skill):
        Game.add_skill(member.id, skill)
        await ctx.send(f"**{member}** has acquired skill **{skill}** from thin air!")
    
    @commands.command(
        help = "test player attack view"
    )
    async def testattackview(self, ctx):
        await Game.test_attack_view(ctx)

    # @commands.command(
    #     help = "- Show your skills."
    # )
    #async def skills(self, ctx):
        #waterlemon

    @commands.command(
        help = "- Register your player."
    )
    async def register(self, ctx):
        error_code = await Game.register(ctx.author.id)
        if error_code == 0:
            await ctx.send("You have already been registered!")
        else:
            await ctx.send(f"Congratulation on creating your character, {ctx.author.mention}. Try using the command `pot add_stats` to use your stat points")

    @commands.command(
        help = "- Use your stat points."
    )
    async def add_stats(self, ctx):
        await ctx.send("Stat adjusting in process")
        error_code = await Game.add_stats(self.bot, ctx.author.id)
        if error_code == 0:
            await ctx.send("You don't have any stat points to spend, try leveling up and get some!")
        elif error_code == 1:
            await ctx.send("Stat adjustment timed out, your changes were not saved...")
        else:
            await ctx.send("Stat successfully adjusted!")

    @commands.command(
        help = "- Display your profile."
    )
    async def profile(self, ctx):
        user_id = str(ctx.author.id)
        stats = Game.get_stats(user_id)
        embed = Game.show_stats(ctx.author, stats)
        await ctx.send(embed = embed)
        
    @commands.Cog.listener("on_message")
    async def mob_spawner(self, message):
        if message.author.bot: return

        cur_time = time.time()
        
        if cur_time > self.last_message.get(message.channel.id, 0) + 5:
            if random.randint(1, 100) <= 101:
                await Game.spawn_mob(self.bot, message.channel)
            self.last_message[message.channel.id] = cur_time

    @commands.command(
        help = "- Display the skill tree"
    )
    async def display_skill_tree(self, ctx):
        embed = ""
        for root_skill in objects.skills:
            if objects.skills[root_skill].parent == None:
                dfs_stack = []
                dfs_stack.append([root_skill, 0])
                while dfs_stack:
                    current_skill, depth = dfs_stack[-1][0], dfs_stack[-1][1]
                    dfs_stack.pop()
                    embed += "       " * depth
                    embed += current_skill
                    embed += "\n"
                    for son_skill in objects.skills:
                        if objects.skills[son_skill].parent == current_skill:
                            dfs_stack.append([son_skill, depth + 1])
        await ctx.send(f"```\n{embed}\n```")

async def setup(bot):
    await bot.add_cog(Potato(bot))
