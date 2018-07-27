import discord
from discord.ext import commands
from cogs.utils import checks
from random import randint
from random import choice




class Fun:
    """ПРостые команды."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def sword(self, ctx, *, user: discord.Member):
        """Дуэль на мечах!"""
        author = ctx.message.author
        if user.id == self.bot.user.id:
            await self.bot.say("Ты не можешь сражаться со мной.")
        else:
            await self.bot.say(author.mention + " и " + user.mention + " сражались " + str(randint(2, 120)) +
                               " многочисленных часов! Это было долго, потно, но " +
                               choice([author.mention, user.mention]) + " стал(а) победителем!\nhttps://i.imgur.com/u76vtsP.gifv")

    @commands.command(pass_context=True)
    async def love(self, ctx, user: discord.Member):
        """Найдём твою истинную любовь?"""
        author = ctx.message.author
        if user.id == self.bot.user.id:
            await self.bot.say("Я люблю себя на 100%" )
        else:
            await self.bot.say("Возможность того, что " + author.mention + " ❤любит❤ " + user.mention + " примерно " +
                               str(randint(0, 100)) + "%!")

    @commands.command(pass_context=True)
    async def pizza(self, ctx):
        """Как много кусочков пиццы сегодня ты съел(а)?"""
        author = ctx.message.author
        await self.bot.say(author.mention + " съел(а) " + str(randint(2, 120)) + " кусочков пиццы. 🍕")

    @commands.command(name="commands")
    async def _commands(self):
        """Командовать ботом"""
        await self.bot.say("Не говори мне что делать!")
    @commands.command(pass_context=True)
    async def elpsy(self, ctx):
        """Эл псай Ойшидесу!"""
        hello = "**El Psy Oishīdesu**\n<:17:258882495586500608><:borschtsch:255796379186757642><:CatBug:259254144328663040>"
        em = discord.Embed(description=hello, colour=ctx.message.author.colour)
        await self.bot.say(embed=em)

    @commands.command(pass_context=True)
    async def roll(self, ctx, dice : int = 1, modifier : int = 20):
        """Бросить кубики. Не вводить более, чем 410 410."""
        s = 0
        numbers = ""
        author = ctx.message.author
        dice2 = dice
        for dice in range(dice):
            n = str(randint(0,modifier))
            s = int(s) + int(n)
            numbers = numbers + str(n) + ", "
        await self.bot.say("{}, *бросаю кубики* :game_die: {}d{} - [{}] = **{}** :game_die:".format(author.name, dice2, modifier, numbers, s))


def setup(bot):
    n = Fun(bot)
    bot.add_cog(n)
