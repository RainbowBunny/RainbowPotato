import discord
import asyncio

from random import randint
from utils import Utils
from discord.ext import commands

class Player(discord.Member):
    pass
        
class Board:
    def __init__(self):
        self.board = []
        for i in range(10):
            self.board.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.char = [1, 2, 4, 3]
    
    

    def __repr__(self):
        def print_num(number):
            string = str(number)
            if number < 10:
                string = ' ' + string
            return string
        string = "```\n 0  0 "
        for i in range(0, 10):
            string += print_num(i + 1) + " "
        string += '\n'
        string += " 0  0"
        for i in range(10):
            sum = 0
            for j in range(10):
                sum += self.board[j][i]
            string += " "
            string += print_num(sum)
        string += "\n"
        for i in range(len(self.board)):
            sum = 0
            for j in range(10):
                sum += self.board[i][j]
            string += print_num(sum)
            string += ' '
            string += print_num(i + 1)
            for j in range(len(self.board[i])):
                string += ' '
                string += print_num(self.board[i][j])
            string += '\n'
        string += "```"
        return string

    def valid_move(self, pos):
        x, y = pos
        if x < 0 or y < 0 or x >= len(self.board) or y >= len(self.board[0]):
            return False
        if self.board[x][y]:
            return False
        return True

    def move(self, pos, turn):
        x, y = pos
        self.board[x][y] = self.char[turn]

    def status(self):
        for i in range(10):
            sumrow, countrow = 0, 0
            sumcol, countcol = 0, 0
            for j in range(10):
                if self.board[i][j]:
                    sumrow += self.board[i][j]
                    countrow += 1
                if self.board[i][j]:
                    sumcol += self.board[i][j]
                    countcol += 1
            if sumrow % 5 == 0 and countrow >= 5:
                return 1
            if sumcol % 5 == 0 and countcol >= 5:
                return 1
        return 0




class BetterXO(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.Occupied = []
        self.Inbattle = []

    async def Play(self, ctx, player_list):
        board = Board()
        turn = randint(0, 1)
        if turn:
            player_list[0], player_list[1] = player_list[1], player_list[0]

        for i in range(2):
            player_list.append(player_list[i])

        await ctx.send(f'{player_list[0].mention} go first!')

        for i in range(100):
            curplayer = i % 4
            await ctx.send(f"It's {player_list[curplayer].mention}\n")
            await ctx.send(board)

            def check(message):
                msg = message.content.split()
                if len(msg) < 2:
                    return False
                try:
                    msg[0], msg[1] = int(msg[0]), int(msg[1])
                    return board.valid_move([msg[0] - 1, msg[1] - 1])
                except ValueError:
                    return False

            message = await self.bot.wait_for('message', check = check)
            msg = message.content.split()
            board.move([int(msg[0]) - 1, int(msg[1]) - 1], curplayer)

            if board.status():
                await ctx.send(f"{player_list[curplayer]} wins!")
                await ctx.send(board)
                return       



    @commands.command(name = 'challenge')
    async def challenge(self, ctx, *, name):
        player_list = []
        player_list.append(ctx.author)
        player_list.append(await Utils.find_member(ctx, self.bot, name))
        if not player_list[1]:
            await ctx.send('Invalid User!')
        
        await ctx.send(f'{player_list[0].mention} is challenging {player_list[1].mention}!')
        def check(message):
            return message.author.id == player_list[1].id and 'accept' in message.content
        
        try:
            await self.bot.wait_for('message', check = check, timeout = 60)
        except TimeoutError:
            await ctx.send('The battle is canceled!')
            return
        await ctx.send(f'A battle is starting between {player_list[0].mention} and {player_list[1].mention}!')

        await self.Play(ctx, player_list)


def setup(bot):
    bot.add_cog(BetterXO(bot))