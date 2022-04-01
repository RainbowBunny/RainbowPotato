import discord
from random import randint

from discord.ext import commands

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
                await ctx.send('Wrong Format Output!')
                continue
            
            try:
                Number = int(MessageList[1])
            except ValueError:
                await ctx.send('Wrong Format Output!')
                continue
            if Number >= 10 ** 5 or Number < 10 ** 4:
                await ctx.send('Wrong Format Output!')
                continue
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