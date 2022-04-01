import discord
from random import randint

from discord.ext import commands

bot = commands.Bot(command_prefix = "pot ", intents = discord.Intents().all())

"""

class Primle:

    def __init__(self):
"""

@bot.event
async def on_ready():
    print("Ready")


@bot.command(name = "potato")
async def potato(ctx):
    message = await ctx.send("Potato?")

    def c(m):
        return m.content == 'a'
    
    msg = await bot.wait_for('message', check = c)
    await ctx.send('Hello')


"""

color['green'] = '🟩'
color['white'] = '⬜'
color['yellow'] = '🟨'



def Sieve():
    for i in range(2, 1000):
        if IsPrime[i]:
            for j in range(i * i, 100000, i):
                IsPrime[j] = 0
        color['green'] = '🟩'
        color['white'] = '⬜'
        color['yellow'] = '🟨'
Sieve()

"""

class Primle(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = dict()
        self.IsPrime = [1] * 100000
        self.PrimeList = []
        self.ColorInit()
        self.Sieve()

    def ColorInit(self):
        self.color['green'] = '🟩'
        self.color['white'] = '⬜'
        self.color['yellow'] = '🟨'
    
    def Sieve(self):
        for i in range(2, 1000):
            if self.IsPrime[i]:
                for j in range(i * i, 100000, i):
                    self.IsPrime[j] = False

        for i in range(10000, 100000):
            if self.IsPrime[i]:
                self.PrimeList.append(i) 

    def Check(self, HiddenPrime, Number):
        Position, HiddenDigit, NumberDigit = [''] * 5, [0] * 5, [0] * 5
        a = HiddenPrime
        b = Number
        for i in range(5):
            HiddenDigit[i] = a % 10
            NumberDigit[i] = b % 10
            a = a // 10
            b = b // 10
            if HiddenDigit[i] == NumberDigit[i]:
                Position[i] = self.color['green']

        for i in range(5):
            if Position[i] == self.color['green']:
                HiddenDigit.remove(NumberDigit[i])

        for i in range(5):
            if Position[i] == self.color['green']:
                continue
            if Position[i] == '' and HiddenDigit.count(NumberDigit[i]):
                Position[i] = self.color['yellow']
                HiddenDigit.remove(NumberDigit[i])
            else:
                Position[i] = self.color['white']

        Position.reverse()
        StringAns = ''
        for element in Position:
            StringAns += element
        return StringAns

    @commands.command(name = "start")
    async def StartGame(self, ctx):
        await ctx.send("I have a number!")
        HiddenPrime = self.PrimeList[randint(0, len(self.PrimeList) - 1)]
        CountTurn, Board = 0, ''

        while CountTurn < 6:
            def CheckMessage(message):
                return message.content.startswith('guess') and ctx.author == message.author and ctx.channel == message.channel

            msg = await self.bot.wait_for('message', check = CheckMessage)
            MessageList = msg.content.split()

            if len(MessageList) < 2:
                print('Wrong Format Output!')
                return
            
            Number = int(MessageList[1])
            print(Number)
            if Number >= 10 ** 5 or Number < 10 ** 4:
                print('Wrong Format Output!')
                return
            StringAnswer = self.Check(HiddenPrime, Number)
            CountTurn = CountTurn + 1
            if Board != '':
                Board += '\n'
            Board += StringAnswer
            Board += ' ' * 9
            Board += str(Number)

            await ctx.send('```' + ctx.author.name + '\n' + Board + '```')

            if StringAnswer == "🟩🟩🟩🟩🟩":
                await ctx.send(f"You have destroyed the game in {CountTurn} years!")
                return
            
            if CountTurn == 6:
                await ctx.send("Guess Limit reached")
                return


def setup(bot):
    bot.add_cog(Primle(bot))
