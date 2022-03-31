class Player:
    # id, name
    def __init__(self):
        self.id = -1
        self.name = "No name"

    def get_id(self):
        return self.id

    def change_id(self, ID):
        self.id = ID

a = Player()
b = Player()

print(a.get_id(), b.get_id())
a.change_id(2), b.change_id(4)

print(a.get_id(), b.get_id())
