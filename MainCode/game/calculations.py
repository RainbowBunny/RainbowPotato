import math

def level_up(level: int) -> int:
    return int(10 * (1.3 ** (level - 1))) * 1000

def calculate_damage(player, target, skill: dict) -> int:
    phys_damage = skill["str"] * player.str 
    phys_damage = phys_damage * (100 / (100 + target.vit))

    magic_damage = skill["int"] * player.int
    magic_damage = magic_damage * (100 / (100 + target.vit))

    return math.ceil(phys_damage + magic_damage)
