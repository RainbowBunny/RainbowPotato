import discord
import asyncio
from game import data_loader as GameData

class SkillButton(discord.ui.Button):
    def __init__(self, row, skill, player):
        super().__init__(style = discord.ButtonStyle.primary, label = skill["name"] if skill else "\u200b", row = row)
        
        self.player = player
        
        if not skill: self.disabled = True
        self.skill = skill

    async def callback(self, interaction: discord.Interaction):
        await interaction.channel.send(f"You used {self.skill['name']}")

        self.disabled = True
        await interaction.response.edit_message(content = "amongus?", view = self.view)
        
        await asyncio.sleep(self.skill["cooldown"])
        
        self.disabled = False
        await interaction.edit_original_message(content = "amongus?", view = self.view)

class PlayerAttackView(discord.ui.View):
    def __init__(self, player):
        super().__init__()
        
        cur = 0
        self.player = player
        
        for i in player.active_skills:
            if cur >= 5: self.add_item(SkillButton(2, GameData.get_skill(i), player))
            else: self.add_item(SkillButton(1, GameData.get_skill(i), player))
            cur += 1

class Creature:
    def __init__(self, stats, ctx):
        for stat, value in stats.items():
            setattr(self, stat, value)
        self.ctx = ctx

class Player(Creature):
    def bind_member(self, member: discord.Member):
        self.member = member

    async def attack(self, msg):
        pass

class Mob(Creature):
    async def attack(self, view):
        pass
    
