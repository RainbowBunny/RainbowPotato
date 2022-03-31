import json
from discord.ext import tasks

# Init: 
# data = Reader()
# data.add_file("file_1.json")
# data.add_file("file_2.json")
# data.loop()

# Access file_1.json: data["file_1.json"]

class Reader:
    def __init__(self):
        self.data = {}
        self.files = []

    def add_file(self, name):
        self.files.append(name)
        with open(name, "r") as f:
            self.data[name] = json.load(f)

    @tasks.loop(minutes = 5)
    async def write(self):
        for file_name in self.files:
            with open(file_name, "w") as f:
                json.dump(self.data[file_name], f)
    
    def loop(self):
        self.write.start()

    def __getitem__(self, key):
        return self.data[key]