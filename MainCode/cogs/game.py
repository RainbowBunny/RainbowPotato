import discord
from discord.ext import commands
from utils import Reader
import asyncio

data_reader = Reader()
data_reader.add_file("data.json")
data_reader.loop()
data = data_reader["data.json"]
stats_list = ["hp", "mp", "str", "vit", "agi", "dex", "int"]

class Game:
    @staticmethod
    def check_registered(user_id):
        if str(user_id) in data:
            return True
        return False

    @staticmethod
    def show_stats(stats) -> discord.Embed:
        embed = discord.Embed(title = "Stats")
        desc = []
        for i in stats_list:
            line = f"**{i.upper()}**: {stats[i]}"
            desc.append(line)
        desc.append(f"Remaining stat points: {stats['points']}")

        embed.description = '\n'.join(desc)
        return embed

    @staticmethod
    async def add_stats(bot, user_id):
        id, user_id = user_id, str(user_id)
        user = bot.get_user(id)
        stats = data[user_id]
        if stats["points"] == 0:
            return 0
        await user.send(f"""
        You currently have {data[user_id]["points"]} stat points, you can now freely add points to your base stats.
You should type messages in the following format:
`<stat name> <amount to add>`
with `<stat name>` in `{stats_list}`.
Note: `<amount to add>` can be negative
To confirm your base stats, type `end`
        """)

        stats_msg = await user.send(embed = Game.show_stats(stats))
        
        while True:
            try:
                msg = await bot.wait_for("message", check = lambda m: m.author.id == id and m.guild == None, timeout = 60.0)
            except asyncio.TimeoutError:
                await user.send("You haven't replied for too long, stat adjustment timed out")
                return 1

            d = msg.content.split()
            d = [i for i in d if i != '']
            if len(d) == 1 and d[0].lower() == 'end':
                break

            check = True
            try:
                d[1] = int(d[1])
            except:
                check = False

            if len(d) != 2 or d[0].lower() not in stats_list or not check:
                await user.send("Wrong format!", delete_after = 5)
                continue

            if d[1] <= stats["points"] and stats[d[0]] + d[1] >= 0: 
                stats[d[0]] += d[1]
                stats["points"] -= d[1]
                await stats_msg.edit(embed = Game.show_stats(stats))
            else:
                await user.send("Invalid amount of points!", delete_after = 5)

        data[user_id] = stats
        return 2

    @staticmethod
    async def register(user_id):
        id, user_id = user_id, str(user_id)
        if Game.check_registered(id):
            return 0

        stats = {i: 10 for i in stats_list}
        stats["points"] = 100
        data[user_id] = stats

class Potato(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
    async def profile(self,ctx):
        user_id = str(ctx.author.id)
        stats = data[user_id]
        embed = Game.show_stats(stats)
        embed.set_author(name = str(ctx.author), icon_url = ctx.author.avatar_url)
        #pfp = message.server.get_member(user_id).avatar_url
        #embed.set_image(url=(pfp))
        embed.set_image(url = ctx.author.avatar_url)
        await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Potato(bot))
