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
    async def register(bot, user_id):
        id, user_id = user_id, str(user_id)
        if Game.check_registered(id):
            return 0

        stats = {i: 10 for i in stats_list}
        stats["points"] = 100
        user = bot.get_user(id)

        await user.send(f"""
        You currently have 70 stat points, you can now freely add points to your base stats.
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
                await user.send("You haven't replied for too long, cancelling registration")
                return 2

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

        return 1

class Potato(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        help = "Register your player."
    )
    async def register(self, ctx):
        error_code = await Game.register(self.bot, ctx.author.id)
        if error_code == 0:
            await ctx.send("You have already been registered!")
        elif error_code == 1:
            await ctx.send(f"Successfully registered user {ctx.author.mention}.")
        else:
            await ctx.send("Registration failed.")

def setup(bot):
    bot.add_cog(Potato(bot))