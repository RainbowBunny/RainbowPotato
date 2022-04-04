import json
from discord.ext import tasks
import discord

# Init: 
# data = Reader()
# data.add_file("file_1.json")
# data.add_file("file_2.json")
# data.loop()

# Access file_1.json: data["file_1.json"]

class Utils:
    @staticmethod
    async def find_member(ctx, bot, name):
        if name.startswith("<@") and name.endswith(">"):
            id = name[2:-1]
            if id.isdigit(): 
                return ctx.guild.get_member(int(id))
        
        if name.startswith("<@!") and name.endswith(">"):
            id = name[3:-1]
            if id.isdigit(): 
                return ctx.guild.get_member(int(id))

        l = []
        for i in ctx.guild.members:
            if i.id == ctx.author.id: continue
            if i.bot: continue
            if name.lower() in str(i).lower() or (i.nick and name in i.nick.lower()) or name == str(i.id):
                l.append(i)

        if len(l) == 0: 
            await ctx.send("No user found!")
            return None
        elif len(l) == 1: return l[0]
        elif len(l) >= 10: 
            await ctx.send("Too many members with such name!")
            return None
        else: 
            embed = discord.Embed(title = "Choose a member from below:")
            d = "\n".join([f"{i + 1} - **{l[i]}**" for i in range(len(l))])
            embed.description = d
            await ctx.send(embed = embed)
            try:
                msg = await bot.wait_for("message", check = lambda m: m.author == ctx.author and m.channel == ctx.channel, timeout = 30.0)
                msg = msg.content
                try:
                    msg = int(msg)
                    if msg >= len(l) or msg <= 0: 
                        await ctx.send("Invalid number!")
                        return None
                    else:
                        return l[msg - 1] 
                except:
                    await ctx.send("Invalid number!")
                    return None
            except:
                await ctx.send("Timed out!")
                return None

class Reader:
    def __init__(self):
        self.data = {}
        self.files = []

    def add_file(self, name):
        self.files.append(name)
        with open(name, "r") as f:
            self.data[name] = json.load(f)

    @tasks.loop(seconds = 5)
    async def write(self):
        for file_name in self.files:
            with open(file_name, "w") as f:
                json.dump(self.data[file_name], f)
    
    def loop(self):
        self.write.start()

    def __getitem__(self, key):
        return self.data[key]