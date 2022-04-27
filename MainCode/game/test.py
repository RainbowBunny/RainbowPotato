from unicodedata import name
from pyparsing import null_debug_action

from game.data_loader import get_skill


class Skill:
    def __init__(self, name, skills_data):
        self.skill_name = name
    def read_skill(self):
        skill = get_skill(self.skill_name)
        for key, value in skill.items():
            setattr(self, key, value)
    