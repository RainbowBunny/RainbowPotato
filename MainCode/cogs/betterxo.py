import discord
import asyncio

from discord.ext import commands

class BetterXO(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Occupied = []
        self.Inbattle = []

    @commands.command(name = 'challenge')
    async def challenge(self, ctx, user:discord.Member):
        firstplayer = ctx.author
        secondplayer = user
        
        if firstplayer in self.Occupied:
            await ctx.send('You have already challenging someone!')
            return
        
        if firstplayer in self.Inbattle:
            await ctx.send('You have already in a match!')
            return

        if secondplayer in self.Occupied:
            await ctx.send('This person has already challenging someone!')
            return

        if secondplayer in self.Inbattle:
            await ctx.send('This person has already in a match')
            return

        await ctx.send('A challenger has appeared!')
        self.Occupied.append(firstplayer)
        self.Occupied.append(secondplayer)        
        def CheckMessage(message):
            if message.author.id == secondplayer.id:
                string = message.content.lower()
                return string.startswith('accept') or string.startswith('deny')
            elif message.author.id == firstplayer.id:
                string = message.content.lower()
                return string.startswith('cancel')
            else:
                return False

        try:
            Message = await self.bot.wait_for('message', check = CheckMessage, timeout = 60.0)
            string = Message.content.lower()
            if string.startswith('deny') or string.startswith('cancel'):
                await ctx.send('The battle has been canceled.')
                self.Occupied.remove(firstplayer)
                self.Occupied.remove(secondplayer)
                return
        except asyncio.TimeoutError:
            await ctx.send('The battle has been canceled.')
            self.Occupied.remove(firstplayer)
            self.Occupied.remove(secondplayer)
            return
        
        await ctx.send(f'Challenge accepted between {ctx.author.mention} and {user.mention}!')
        self.Inbattle.append(firstplayer)
        self.Inbattle.append(secondplayer)
        self.Occupied.remove(firstplayer)
        self.Occupied.remove(secondplayer)
        


def setup(bot):
    bot.add_cog(BetterXO(bot))