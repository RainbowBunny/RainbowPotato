import discord
import random
import time
from discord.ext import commands
from utils import Reader
import asyncio
import json
from game.objects import *
from game import data_loader as GameData
from game import calculations as Calc
import math

data_reader = Reader()

data_reader.add_file("data.json")
data_reader.loop()

data = data_reader["data.json"]

stats_list = ["hp", "mp", "str", "vit", "agi", "dex", "int"]

def get_stats(user_id):
    if isinstance(user_id, int): user_id = str(user_id)
    return data[user_id]

async def test_attack_view(ctx):
    player = Player(data[str(ctx.author.id)], ctx)
    player.bind_member(ctx.author)
    await ctx.send("attack view?", view = PlayerAttackView(player))

def add_skill(user_id, skill_name):
    user_id = str(user_id)
    if skill_name not in data[user_id]["skills"]:
        data[user_id]["skills"].append(skill_name)

def set_skill_slot(user_id, slot, skill_name):
    user_id = str(user_id)
    data[user_id]["active_skills"][slot - 1] = skill_name

async def battle(user, embed, channel):
    await channel.send(embed = embed)
    await channel.send(f"{user.mention}, prepare for battle")
    
async def spawn_mob(bot, channel: discord.TextChannel):
    spawns = GameData.get_spawns(channel.id)
    if spawns:
        r = random.random()
        s = 0
        to_spawn = None
        for mob, rate in spawns.items():
            s += rate
            if r <= s:
                to_spawn = mob
                break
        
        if to_spawn:
            mob_data = GameData.get_mob(to_spawn)
            mob_embed = discord.Embed(title = f"A {to_spawn} has emerged!", color = random.randint(0, 16777215))
            mob_embed.set_image(url = mob_data["img"])
            msg = await channel.send(embed = mob_embed)
            await msg.add_reaction("⚔")
            try:
                reaction, user = await bot.wait_for("reaction_add", check = lambda reaction, user : str(reaction.emoji) == "⚔" and reaction.message.id == msg.id and user.id != bot.user.id, timeout = 30.0)
            except asyncio.TimeoutError:
                await msg.clear_reaction("⚔")
                await channel.send(f"The {to_spawn} has escaped")
                return
            
            await channel.send(f"{user} has yoinked the {to_spawn}!")
            await user.add_roles(discord.utils.get(reaction.message.guild.roles, name = "battle-1"))
            await msg.clear_reaction("⚔")
            
            battle_channel = discord.utils.get(reaction.message.guild.channels, name = "battle-1")
            await battle(user, mob_embed, battle_channel)
            return
            
def check_registered(user_id) -> bool:
    if str(user_id) in data:
        return True
    return False

def show_stats(user, stats) -> discord.Embed:

    embed = discord.Embed(title = "", color = random.randint(0, 16777215))
    try:
        embed.set_author(name = str(user), icon_url = user.avatar.url)
    except AttributeError:
        embed.set_author(name = str(user), icon_url = user.default_avatar.url)

    level_up = Calc.level_up(stats["level"])

    desc = []
    desc.append(f"Level: `{stats['level']}`")
    # 🟦 ⬜  `

    exp_bar = ""
    ratio = math.ceil(stats['exp'] / level_up * 10)

    for i in range(ratio): exp_bar += '🟦'
    for i in range(10 - ratio): exp_bar += '⬜'

    desc.append(f"Experience: `{exp_bar}` `({stats['exp']}/{level_up})`")
    desc.append(f"DEX: `{stats['dex']}`")
    
    embed.description = "\n".join(desc)

    embed.add_field(name = "Defensive abilities", value = f"""
    HP: `{stats['hp']}`
    VIT: `{stats['vit']}`
    AGI: `{stats['agi']}`
    """, inline = True)

    embed.add_field(name = "Offensive abilities", value = f"""
    MP: `{stats['mp']}`
    STR: `{stats['str']}`
    INT: `{stats['int']}`
    """, inline = True)

    embed.set_footer(text = f"Remaining stat points: {stats['points']}")

    return embed

async def add_stats(bot, user_id) -> int:
    id, user_id = user_id, str(user_id)
    user = bot.get_user(id)
    stats = data[user_id]
    if stats["points"] == 0:
        return 0
    await user.send(embed = discord.Embed(title = "", description = f"""
You should add points by typing messages in the following format:
`<stat name> <amount to add>`
with `<stat name>` in `{stats_list}`.
Note: `<amount to add>` should be a positive integer
To confirm your base stats, type `end`
    """, color = random.randint(0, 0xffffff)))

    stats_msg = await user.send(embed = show_stats(user, stats))
    
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

        if d[1] > 0 and d[1] <= stats["points"] and stats[d[0]] + d[1] >= 0: 
            stats[d[0]] += d[1]
            stats["points"] -= d[1]
            await stats_msg.edit(embed = show_stats(user, stats))
        else:
            await user.send("Invalid amount of points!", delete_after = 5)

    data[user_id] = stats
    return 2
        
async def register(user_id):
    id, user_id = user_id, str(user_id)
    if check_registered(id):
        return 0

    stats = {"race": "human", "level": 1, "exp": 0}

    for i in range(0, len(stats_list)):
        stats[stats_list[i]] = 10

    stats["points"] = 100
    stats["skills"] = []
    stats["active_skills"] = [None] * 10
    data[user_id] = stats  
