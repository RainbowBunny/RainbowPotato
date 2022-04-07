import json
from utils import Reader

with open("data/mobs.json") as f:
    mobs = json.load(f)
with open("data/maps.json") as f:
    maps_data = json.load(f)
with open("data/skills.json") as f:
    skills_data = json.load(f)

data_reader = Reader()

data_reader.add_file("data.json")
data_reader.loop()

def get_player(id) -> dict:
    return data_reader["data.json"][str(id)]

_id_to_map = {}
_map_to_id = {}
# map channel_id => mobs
_spawns = {}

for regions in maps_data:
    for map, map_data in maps_data[regions].items():
        id = map_data['channel_id']
        _id_to_map[id] = map
        _map_to_id[map] = id
        _spawns[id] = map_data['spawns']

def get_map(id: int) -> str:
    return _id_to_map.get(id, None)

def get_id(map: str) -> int:
    return _map_to_id.get(map, None)

def get_spawns(id: int) -> list:
    return _spawns.get(id, None)

def get_skill(skill_name: str) -> dict:
    return skills_data.get(skill_name, None)

def get_mob(name: str) -> dict:
    return mobs.get(name, None)
