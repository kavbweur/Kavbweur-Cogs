from discord.ext import commands
from cogs.utils import checks
from .utils.dataIO import dataIO
from random import choice, shuffle
from __main__ import send_cmd_help, settings
import os
import aiohttp
import random
import discord
import asyncio

speech = [
'Монолог I (Бог)',
'Монолог II (Смерть)',
'Монолог III (Хмурые дни)',
'Монолог IV (Сон)',
'Монолог V (Смерть Саёри)',
'Монолог VI (Япония)',
'Монолог VII (Депрессия)',
'Монолог VIII (Смысл жизни)',
'Монолог X (Твиттер)',
'Монолог XI (Книга Юри)',
'Монолог XII (Вегетерианство)',
'Монолог XIII (Интроверт)',
'Монолог XV (Любимый цвет)',
'Монолог XVII (Слушатель)']

class Monika():
    """Monika"""
    def __init__(self, bot):
        self.bot = bot

    @commands.group(pass_context=True)
    async def monologue(self, ctx):
        """Монологи из игры Doki Doki Literature Club."""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @monologue.command(pass_context=True)
    async def list(self, ctx):
        """Посмотреть список доступных монологов."""
        await self.bot.say(speech)
    

    @commands.cooldown(1, 120, commands.BucketType.user)
    @monologue.command(pass_context=True)
    async def start(self, ctx, user: discord.Member = None):
        """Запустить случайный монолог."""
        if ctx.message.author.bot:
            return await self.bot.say("Прости, но с другими ботами говорить не хочу.")
        self.stopMonika = False
        text_in_path = 'data/monika/' + random.choice(speech) + '.txt'
        await self.bot.say("Ура, ты готов меня послушать!")
        f = open(text_in_path, encoding='utf-8')
        username = ctx.message.author.name
        while True:
            if self.stopMonika:
                break
            else:
                for line in f:
                    if self.stopMonika:
                        break
                    line
                    await self.bot.say('**' + username + '**' + ', ' + line)
                    await asyncio.sleep(10)
        await self.bot.say("Монолог закончен.")

    @monologue.command(pass_context=True)
    async def stop(self, user: discord.Member = None):
        """Остановить монолог Моники."""
        self.stopMonika = True
        await self.bot.say("Но, ведь ты меня так хорошо слушал.")



def setup(bot):
    bot.add_cog(Monika(bot))