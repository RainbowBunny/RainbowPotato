import discord
import asyncio
from game import data_loader as GameData
from game import calculations as Calc
import random
import math

battles = dict()

class Battle:
    # battlers: list of Creature
    def __init__(self, battlers, channel):
        self.battlers = battlers
        for i in range(len(self.battlers)): 
            self.battlers[i].id = i
            self.battlers[i].base_hp = self.battlers[i].hp

        self.channel = channel

        self.id = ""
        for i in range(30): self.id += str(random.randint(0, 9))
        battles[self.id] = self

    def get_battle_status(self):
        embed = discord.Embed(title = "Battle status:", color = random.randint(0, 16777215))
        for i in self.battlers:
            name = i.user.name if isinstance(i, Player) else i.name

            remaining_hp = self.battlers[i.id].hp
            base_hp = self.battlers[i.id].base_hp
            
            bar = ""
            ratio = math.ceil(remaining_hp / base_hp * 10)

            for i in range(ratio): bar += '🟦'
            for i in range(10 - ratio): bar += '⬜'

            embed.add_field(name = name, value = f"HP: `{bar}` `({remaining_hp}/{base_hp})`", inline = False)
        
        return embed

    async def start(self):
        self.message = await self.channel.send(embed = self.get_battle_status(), view = BattleView(self.battlers, self.id))

    # attacker and defender are ids
    async def attack(self, attacker: int, skill):
        defender = attacker ^ 1 # because 1v1 :(
        damage = Calc.calculate_damage(self.battlers[attacker], self.battlers[defender], skill)
        self.battlers[defender].hp -= damage
        print(attacker, skill, "DAMAGE", damage)
        await self.update_battlers_status()

    async def update_battlers_status(self):
        await self.message.edit(embed = self.get_battle_status())

class SkillButton(discord.ui.Button):
    def __init__(self, row, skill, player, battle_id):
        super().__init__(style = discord.ButtonStyle.primary, label = skill["name"] if skill else "\u200b", row = row)
        
        self.player = player
        self.battle_id = battle_id

        if not skill: self.disabled = True
        self.skill = skill

    async def callback(self, interaction: discord.Interaction):
        # await interaction.channel.send(f"You used {self.skill['name']}")
        await battles[self.battle_id].attack(self.player.id, self.skill)

        self.disabled = True
        await interaction.response.edit_message(view = self.view)
        
        await asyncio.sleep(self.skill["cooldown"])
        
        self.disabled = False
        await interaction.edit_original_message(view = self.view)

class PlayerAttackView(discord.ui.View):
    def __init__(self, player, battle_id):
        super().__init__()
        
        cur = 0
        self.player = player
        
        for i in player.active_skills:
            if cur >= 5: self.add_item(SkillButton(2, GameData.get_skill(i), player, battle_id))
            else: self.add_item(SkillButton(1, GameData.get_skill(i), player, battle_id))
            cur += 1

class BattleView(discord.ui.View):
    def __init__(self, battlers, battle_id):
        super().__init__()

        self.battlers = battlers
        self.players = {i.user.id: i for i in battlers if isinstance(i, Player)}
        self.player_views = dict()
        self.battle_id = battle_id

    @discord.ui.button(label = "Open skill view")
    async def open(self, interaction: discord.Interaction, button: discord.ui.Button):
        user = interaction.user

        if user.id in self.players:
            embed = discord.Embed(title = "Skill view", color = random.randint(0, 16777215))
            
            if user.id in self.player_views:
                await self.player_views[user.id].edit_original_message(content = "Disabled.", embed = None, view = None)

            await interaction.response.send_message(embed = embed, view = PlayerAttackView(self.players[user.id], self.battle_id), ephemeral = True)
            self.player_views[user.id] = interaction
        else:
            await interaction.response.send_message("This is not your battle?")

class Creature:
    def __init__(self, stats):
        for stat, value in stats.items():
            setattr(self, stat, value)

class Player(Creature):
    def __init__(self, user: discord.User):
        # print(GameData.get_player(user.id))
        super().__init__(GameData.get_player(user.id))
        self.user = user

class Mob(Creature):
    pass
