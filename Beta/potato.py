import discord
from random import randint
from discord.ext import commands

bot = commands.Bot(command_prefix = "pot ", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print("Ok")

@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")

class player:
    def __init__(self):
        self.hp = "null"
        self.damage = "null"
        self.defense = "null"
        self.speed = "null"
        self.exp = "null"
    def create(self, hp, damage, defense, speed):
        self.hp = hp
        self.damage = damage
        self.defense = defense
        self.speed = speed
        self.exp = 0
    

class slime:
    def __init__(self):
        self.hp = 10
        self.damage = 2
        self.speed = 2
        self.exp = 5
        
@bot.command()
async def register(ctx):
    await ctx.send("your character has been created")
    global you
    you = player()
    you.create(20,3,2,3)

@bot.command()
async def status(ctx):
    await ctx.send("hp: {0}".format(you.hp))
    await ctx.send("atk: {0}".format(you.damage))
    await ctx.send("defense: {0}".format(you.defense))
    await ctx.send("speed: {0}".format(you.speed))

def fight(player, mob):
    time = 0
    block = 0
    while True:
        print("your hp:", player.hp)
        print("opponent's hp", mob.hp)
        if block < 0:
            block = 0
        time += 1
        if time%2==1:
            move = input("choose: attack/defense\n")
            if move[0].lower() == "a":
                print("you attack for {0} damage".format(player.damage))
                mob.hp -= player.damage
                if mob.hp <= 0:
                    print("You won and gained {0} exp".format(mob.exp))
                    player.exp += mob.exp
                    break
            elif move[0].lower() == "d":
                print("you decide to block the next attack")
                block += player.defense
        else:
            print("the mob attack you for {0} damage".format(mob.damage-block))
            player.hp -= (mob.damage-block)
            if player.hp <= 0:
                print("wasted")
#bob = slime()
#fight(you, bob)
"""
###

color = dict()

color['green'] = '🟩'
color['white'] = '⬜'
color['yellow'] = '🟨'

IsPrime = [1] * 100000

def Sieve():
    for i in range(2, 1000):
        if IsPrime[i]:
            for j in range(i * i, 100000, i):
                IsPrime[j] = 0

Sieve()

###

HiddenPrime = 0
CountTurn = 0
Started = 0
Ended = 1
Board = ''

ListOfPrime = []
for i in range(10000, 100000):
    if IsPrime[i]:
        ListOfPrime.append(i)

async def Check(ctx, Number):
    Position, HiddenDigit, NumberDigit = [''] * 5, [0] * 5, [0] * 5

    global HiddenPrime
    a = HiddenPrime
    b = Number
    for i in range(5):
        HiddenDigit[i] = a % 10
        NumberDigit[i] = b % 10
        a = a // 10
        b = b // 10
        if HiddenDigit[i] == NumberDigit[i]:
            Position[i] = color['green']

    for i in range(5):
        if Position[i] == color['green']:
            HiddenDigit.remove(NumberDigit[i])

    for i in range(5):
        if Position[i] == color['green']:
            continue
        if Position[i] == '' and HiddenDigit.count(NumberDigit[i]):
            Position[i] = color['yellow']
            HiddenDigit.remove(NumberDigit[i])
        else:
            Position[i] = color['white']

    Position.reverse()
    StringAns = ''
    for element in Position:
        StringAns += element
    return StringAns


@bot.command(name = "guess")
async def Guess(ctx, Number):
    global Ended, CountTurn, Board
    if Ended:
        await ctx.send("Game Ended")
        return
    try: 
        Number = int(Number)
        
        if Number >= 10 ** 4 and Number < 10 ** 5:
            StringAnswer = await Check(ctx, Number)
            CountTurn = CountTurn + 1
            if Board != '':
                Board += '\n'
            Board += StringAnswer
            Board += ' ' * 9
            Board += str(Number)

            await ctx.send('```' + Board + '```')

            if StringAnswer == "🟩🟩🟩🟩🟩":
                await ctx.send(f"You have destroyed the game in {CountTurn} years!")
                Ended = 1
                return
            
            if CountTurn == 6:
                await ctx.send("Guess Limit reached")
                Ended = 1
                return

    except ValueError:
        await ctx.send('Wrong format answer, please answer again!')



@bot.command(name = "start")
async def Start(ctx):
    global Started, HiddenPrime, CountTurn, Ended, Board
    if Started:
        await ctx.send('A game has already started')
        return
    HiddenPrime = ListOfPrime[randint(0, len(ListOfPrime) - 1)]
    CountTurn = 0
    Ended = 0
    await ctx.send('I have a number!')
    print(HiddenPrime)
"""



bot.run('OTU4MjEyNDk2MTIzMTI5ODc2.YkKC7Q.hyzEAH1qR3oKUgLHth3gj_h6Coo')

