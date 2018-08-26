import discord
import asyncio
from discord.ext import commands
from cogs.utils import checks
from random import randint
from random import choice




class Fun:
    """Простые команды, возможно весёлые."""

    def __init__(self, bot):
        self.bot = bot
    
    async def _answer_user(self, ctx, msg: str):
        await self.bot.say(msg)
        msg = await self.bot.wait_for_message(author=ctx.message.author, channel=ctx.message.channel)
        if msg:
            if msg.content == 'Да':
                msg = 'Yes'
            elif msg.content == 'Нет':
                msg = 'No'
        return msg

    @commands.command(pass_context=True)
    async def sword(self, ctx, *, user: discord.Member):
        """Битва за Святой Грааль!"""
        servant_class = ["Saber", "Lancer", "Archer", "Rider", "Caster", "Assassin", "Berserker"]
        print(servant_class)
        author = ctx.message.author
        servant = choice(servant_class)
        enemy_servant = choice(servant_class)
        if servant == enemy_servant:
            enemy_servant = choice(servant_class)
        winner = choice([author.name, user.name])
        loser = choice([author.name, user.name])
        if winner == loser:
            loser = choice([author.name, user.name])
        await self.bot.say("**Вы участвуете в войне за Святой Грааль.**")
        await self.bot.say("*идёт призыв случайного слуги*")
        await asyncio.sleep(2)
        await self.bot.say("Вы призвали слугу класса: **{}**".format(servant))
        answer = await self._answer_user(ctx, "Хотите продолжить? Ответьте Да или Нет.")
        if answer == 'Yes':
            await self.bot.say("Вы храбрый маг, поэтому можете продолжать войну за Святой Грааль.")
        elif answer == 'No':
            await self.bot.say('Вас находит **{}** и спокойно убивает.\nhttps://i.imgur.com/HfhVSZO.gifv'.format(enemy_servant))
            return
        else:
            await self.bot.say("Вы не можете читать.")
            return
        if user.id == self.bot.user.id:
            await asyncio.sleep(5)
            await self.bot.say("Вы вызвали Монику на битву.\n**МОНИКА ИСПОЛЬЗУЕТ НЕБЕСНЫЙ ФАНТАЗМ**\nВы и Ваш слуга погибаете, вы не можете продолжать свой участие в войне за святой грааль.\nhttps://i.imgur.com/HfhVSZO.gifv")
            return
        if user.id == author.id:
            await asyncio.sleep(5)
            await self.bot.say("Вы приказали вашему слуге атаковать себя командным заклинанием.\n***слуга умирает, проклиная вас***\nВы не можете больше продолжить своё участие в войне за Святой Грааль.\nhttps://i.imgur.com/g9hZaZ4.gifv")
            return
        await asyncio.sleep(5)
        await self.bot.say("Вы встретили врага, класс его слуги: **{}**".format(enemy_servant))
        await asyncio.sleep(2)
        await self.bot.say("**НАЧИНАЕТСЯ БИТВА МЕЖДУ СЛУГАМИ**\nhttps://i.imgur.com/u76vtsP.gifv")
        await asyncio.sleep(5)
        if winner == author.name:
            await self.bot.say("Побеждает: **{}** со своим слугой **{}**.".format(winner, servant))
        else:
            await self.bot.say("Побеждает: **{}** со своим слугой **{}**.".format(winner, enemy_servant))


    @commands.command(pass_context=True)
    async def love(self, ctx, user: discord.Member):
        """Найдём твою истинную любовь?"""
        author = ctx.message.author
        if user.id == self.bot.user.id:
            await self.bot.say("Я знаю, что ты меня любишь, нет необходимости проверять это." )
            return
        if user.id == author.id:
            await self.bot.say("Я не могу сказать насколько сильно ты любишь себя.")
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
    async def roll(self, ctx, dice : str):
        """Бросить кубики. Пример: 1d20"""
        s = 0
        twised = dice.split('d')
        dice = twised[0]
        try:
            modifier = twised[1]
        except IndexError:
            await self.bot.say("Вы неправильно ввели команду. Пример: 1d20")
            return
        numbers = []
        author = ctx.message.author
        dice = int(dice)
        modifier = int(modifier)
        dice2 = dice
        for dice in range(dice):
            n = int(randint(1,modifier))
            s = int(s) + int(n)
            numbers.append(n)
        try:
            await self.bot.say("{}, *бросаю кубики* :game_die: {}d{} - {} = **{}** :game_die:".format(author.name, dice2, modifier, numbers, s))
        except:
            await self.bot.say("Не удалось отправить сообщение, так как оно было слишком длинным.")


def setup(bot):
    n = Fun(bot)
    bot.add_cog(n)
