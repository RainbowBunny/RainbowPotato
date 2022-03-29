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

#Game Primle

color = dict()

color['green'] = '🟩'
color['white'] = '⬜'
color['yellow'] = '🟨'

#Init Game
IsPrime = [1] * 100000

def Sieve():
    for i in range(2, 1000):
        if IsPrime[i]:
            for j in range(i * i, 100000, i):
                IsPrime[j] = 0

Sieve()

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
    global Ended, COuntTurn, Board
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




bot.run('OTU4MjEyNDk2MTIzMTI5ODc2.YkKC7Q.hyzEAH1qR3oKUgLHth3gj_h6Coo')

