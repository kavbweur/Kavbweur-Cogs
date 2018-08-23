import discord
import itertools
import asyncio
import functools
from cogs.utils import checks
from random import choice, shuffle
from discord.ext import commands
from imgurpython import ImgurClient

CLIENT_ID = "1fd3ef04daf8cab"
CLIENT_SECRET = "f963e574e8e3c17993c933af4f0522e1dc01e230"

class Catbug_old:
    def __init__(self, bot):
        self.bot = bot
        self.imgur = ImgurClient(CLIENT_ID, CLIENT_SECRET)
    
    
    
    @commands.command(pass_context=True, name="invite")
    async def invite_bot(self, ctx):
        """Пригласить Монику на свой сервер."""
        await self.bot.say("Пригласить Монику на свой сервер можно перейдя на сайт Моники:\nhttp://kavbweur.website/invite")


    @commands.command(pass_context=True)
    async def catbug(self, ctx):
        """Картинки с котожуком (почти)."""
        task = functools.partial(self.imgur.gallery_search, "CatBug",
                                 advanced=None, sort='time',
                                 window='all', page=0)
        task = self.bot.loop.run_in_executor(None, task)
        try:
            results = await asyncio.wait_for(task, timeout=10)
        except asyncio.TimeoutError:
            await self.bot.say("Я не успела найти")
        else:
            if results:
                shuffle(results)
                msg = "Картиночки (почти) с котожуком:\n"
                for r in results[:5]:
                    msg += r.gifv if hasattr(r, "gifv") else r.link
                    msg += "\n"
                await self.bot.say(msg)
            else:
                await self.bot.say("Странно, котожуков больше нет.")
        
    @commands.command(pass_context=True)
    async def enru(self, ctx, *, text: str):
        """Перевод английской раскладки в русскую"""
        char = "`qwertyuiop[]asdfghjkl;'zxcvbnm,./"
        tran = "ёйцукенгшщзхъфывапролджэячсмитьбю."
        table = str.maketrans(char, tran)
        text = text.translate(table)
        char = char.upper()
        tran = tran.upper()
        table = str.maketrans(char, tran)
        text = text.translate(table)
        text = ''.join(c for c, _ in itertools.groupby(text))
        char = "`qwertyuiop[]asdfghjkl;'zxcvbnm,./"
        tran = "ёйцукенгшщзхъфывапролджэячсмитьбю."
        table = str.maketrans(char, tran)
        text = text.translate(table)
        char = char.upper()
        tran = tran.upper()
        table = str.maketrans(char, tran)
        text = text.translate(table)
        await self.bot.say("Сообщение после смены раскладки:\n``{}``".format(text))
         
    
    @commands.command(pass_context=True)
    async def ruen(self, ctx, *, text: str):
        """Перевод русской раскладки в английскую"""
        char = "ёйцукенгшщзхъфывапролджэячсмитьбю."
        tran = "`qwertyuiop[]asdfghjkl;'zxcvbnm,./"
        table = str.maketrans(char, tran)
        text = text.translate(table)
        char = char.upper()
        tran = tran.upper()
        table = str.maketrans(char, tran)
        text = text.translate(table)
        text = ''.join(c for c, _ in itertools.groupby(text))
        char = "ёйцукенгшщзхъфывапролджэячсмитьбю."
        tran = "`qwertyuiop[]asdfghjkl;'zxcvbnm,./"
        table = str.maketrans(char, tran)
        text = text.translate(table)
        char = char.upper()
        tran = tran.upper()
        table = str.maketrans(char, tran)
        text = text.translate(table)
        await self.bot.say("Сообщение после смены раскладки:\n``{}``".format(text))


    @commands.command(pass_context=True)
    @checks.is_owner()
    async def set_the_game(self, ctx):
        server = ctx.message.server
        game = "^help | MonikaBot.info"
        current_status = server.me.status if server is not None else None
        game = game.strip()
        await self.bot.change_presence(game=discord.Game(name=game),
                                       status=current_status)
        await self.bot.say("Выполнено.")
    
    @commands.command(pass_context=True, name="requirementinstall")
    @checks.is_owner()
    async def install_req(self, ctx, requirement: str):
        """Установка библиотек в обход консоли."""
        await self.bot.say(await self.bot.pip_install(requirement))
        
def setup(bot):
    n = Catbug_old(bot)
    bot.add_cog(n)
    
