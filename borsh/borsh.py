# Cookie was created by Redjumpman for Redbot and edited to borsh
# Design credit to discord user Yukirin for commissioning this project

# Standard Library
import asyncio
import os
import random
import time
from operator import itemgetter

# Discord and Red
import discord
from .utils import checks
from __main__ import send_cmd_help
from .utils.dataIO import dataIO
from discord.ext import commands


class PluralDict(dict):
    """This class is used to plural strings

    You can plural strings based on the value input when using this class as a dictionary.
    """
    def __missing__(self, key):
        if '(' in key and key.endswith(')'):
            key, rest = key.split('(', 1)
            value = super().__getitem__(key)
            suffix = rest.rstrip(')').split(',')
            if len(suffix) == 1:
                suffix.insert(0, '')
            return suffix[0] if value <= 1 else suffix[1]
        raise KeyError(key)


class Borsh:
    """Все любят борщ, и выможете украсть у кого-нибудь для себя!"""
    def __init__(self, bot):
        self.bot = bot
        self.file_path = "data/KavbweurCogs/borsh/borsh.json"
        self.system = dataIO.load_json(self.file_path)

    @commands.group(pass_context=True, no_pm=True)
    async def setborsh(self, ctx):
        """Настройка модуля Борщ."""

        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @setborsh.command(name="stealcd", pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _stealcd_heist(self, ctx, cooldown: int):
        """Установить время спустя которое будет доступно воровство борща."""
        server = ctx.message.server
        settings = self.check_server_settings(server)
        if cooldown >= 0:
            settings["Config"]["Steal CD"] = cooldown
            dataIO.save_json(self.file_path, self.system)
            msg = "Ограничение по времени установлено: {}".format(cooldown)
        else:
            msg = "Ограничение должно быть больше, чем 0."
        await self.bot.say(msg)

    @setborsh.command(name="borshcd", pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def _borshcd_heist(self, ctx, cooldown: int):
        """Установить ограничение по времени для получения борща от Котожука."""
        server = ctx.message.server
        settings = self.check_server_settings(server)
        if cooldown >= 0:
            settings["Config"]["Borsh CD"] = cooldown
            dataIO.save_json(self.file_path, self.system)
            msg = "Ограничение по времени для выдачи борща установлено: {}".format(cooldown)
        else:
            msg = "Ограничение по времени должно быть больше, чем 0."
        await self.bot.say(msg)





    @commands.command(pass_context=True, no_pm=True)
    async def give(self, ctx, user: discord.Member, borshs: int):
        """Передать другому свои тарелки с борщем."""
        author = ctx.message.author
        settings = self.check_server_settings(author.server)
        if user.bot:
            return await self.bot.say("Хорошая попытка, но ботам нельзя отдать борщ.")
        if author.id == user.id:
            return await self.bot.say("Ты не можешь дать самому себе борщ, ведь он уже твой.")
        self.account_check(settings, author)
        self.account_check(settings, user)
        sender_borsh = settings["Players"][author.id]["Borshs"]
        if 0 < borshs <= sender_borsh:
            settings["Players"][author.id]["Borshs"] -= borshs
            settings["Players"][user.id]["Borshs"] += borshs
            dataIO.save_json(self.file_path, self.system)
            if 1 == borshs:
                plate = "тарелку"
            if 1 < borshs < 5:
                plate = "тарелки"
            if 4 < borshs:
                plate = "тарелок"
            if 20 < borshs:
                remainder = borshs % 10
                if 1 == remainder:
                    plate = "тарелку"
                if 1 < remainder < 5:
                    plate = "тарелки"
                if 4 < remainder:
                    plate = "тарелок"
            msg = "Ты дал **{}** {} с борщем {}".format(borshs, plate, user.name)
        else:
            msg = "У тебя недостаточно тарелок борща для этого."

        await self.bot.say(msg)

    @commands.command(pass_context=True, no_pm=True)
    async def borsh(self, ctx):
        """Получить случайное количество тарелок с борщем. 12h ограничение по времени."""
        author = ctx.message.author
        server = ctx.message.server
        action = "Borsh CD"
        settings = self.check_server_settings(server)
        self.account_check(settings, author)
        if await self.check_cooldowns(author.id, action, settings):
            weighted_sample = [1] * 152 + [x for x in range(49) if x > 1]
            borshs = random.choice(weighted_sample)
            settings["Players"][author.id]["Borshs"] += borshs
            dataIO.save_json(self.file_path, self.system)
            if 1 == borshs:
                plate = "тарелку"
            if 1 < borshs < 5:
                plate = "тарелки"
            if 4 < borshs:
                plate = "тарелок"
            if 20 < borshs:
                remainder = borshs % 10
                if 1 == remainder:
                    plate = "тарелку"
                if 1 < remainder < 5:
                    plate = "тарелки"
                if 4 < remainder:
                    plate = "тарелок"
            await self.bot.say(" ༼ つ ◕\_◕ ༽つ <:borschtsch:255796379186757642>\nТы получил {} "
                               "{} борща от Котожука <:borschtsch:255796379186757642><:CatBug:259254144328663040>! Туттуру<:17:258882495586500608>!".format(borshs, plate))

    @commands.command(pass_context=True, no_pm=False, ignore_extra=False)
    async def fridge(self, ctx):
        """Посмотреть как много тарелок с борщем в твоём холодильнике."""
        author = ctx.message.author
        server = ctx.message.server
        settings = self.check_server_settings(server)
        self.account_check(settings, author)
        borshs = settings["Players"][author.id]["Borshs"]
        if 1 == borshs:
            plate = "тарелку"
        if 1 < borshs < 5:
            plate = "тарелки"
        if 4 < borshs:
            plate = "тарелок"
        if 20 < borshs:
            remainder = borshs % 10
            if 1 == remainder:
                plate = "тарелку"
            if 1 < remainder < 5:
                plate = "тарелки"
            if 4 < remainder:
                plate = "тарелок"
        await self.bot.whisper("Моника ищет в твоём холодильнике <:refrigerator:470613165563052054> тарелки с борщем и находит там **{}** {}. "
                               "<:CatBug:259254144328663040><:borschtsch:255796379186757642><:CatBug:259254144328663040>".format(borshs, plate))

    @commands.command(pass_context=True, no_pm=True)
    async def steal(self, ctx, user: discord.Member=None):
        """Украсть борщ у другого человека. 2h ограничение по времени."""
        author = ctx.message.author
        server = author.server
        action = "Steal CD"
        settings = self.check_server_settings(author.server)
        self.account_check(settings, author)

        if user is None:
            user = self.random_user(settings, author, server)

        if user == "Fail":
            pass
        elif user.bot:
            return await self.bot.say("Воровство не удалось, так как ваша цель бот.\nТы "
                                      "можешь ещё раз попытаться своровать.")

        if await self.check_cooldowns(author.id, action, settings):
            msg = self.steal_logic(settings, user, author)
            await self.bot.say("*Моника пытается своровать немного борща.* <:borschtsch:255796379186757642>")
            await asyncio.sleep(4)
            await self.bot.say(msg)

    async def check_cooldowns(self, userid, action, settings):
        path = settings["Config"][action]
        if abs(settings["Players"][userid][action] - int(time.perf_counter())) >= path:
            settings["Players"][userid][action] = int(time.perf_counter())
            dataIO.save_json(self.file_path, self.system)
            return True
        elif settings["Players"][userid][action] == 0:
            settings["Players"][userid][action] = int(time.perf_counter())
            dataIO.save_json(self.file_path, self.system)
            return True
        else:
            s = abs(settings["Players"][userid][action] - int(time.perf_counter()))
            seconds = abs(s - path)
            remaining = self.time_formatting(seconds)
            await self.bot.say("Это действие ограничено по частоте использования. Ты сможешь попытаться ещё раз через:\n{}".format(remaining))
            return False

    def steal_logic(self, settings, user, author):
        success_chance = random.randint(1, 100)
        if user == "Fail":
            msg = "Ну вот, я не смогла найти у него борщ :с"
            return msg

        if user.id not in settings["Players"]:
            self.account_check(settings, user)

        if settings["Players"][user.id]["Borshs"] == 0:
            msg = ("Моника просит прощения, но она не нашла ничего кроме пустых тарелок"
                   "<:borschtsch:255796379186757642> в холодильнике!")
        else:
            if success_chance <= 90:
                borsh_fridge = settings["Players"][user.id]["Borshs"]
                borsh_stolen = int(borsh_fridge * 0.75)

                if borsh_stolen == 0:
                    borsh_stolen = 1

                stolen = random.randint(1, borsh_stolen)
                settings["Players"][user.id]["Borshs"] -= stolen
                settings["Players"][author.id]["Borshs"] += stolen
                dataIO.save_json(self.file_path, self.system)
                if 1 == borshs:
                    plate = "тарелку"
                if 1 < borshs < 5:
                    plate = "тарелки"
                if 4 < borshs:
                    plate = "тарелок"
                if 20 < borshs:
                    remainder = borshs % 10
                    if 1 == remainder:
                        plate = "тарелку"
                    if 1 < remainder < 5:
                        plate = "тарелки"
                    if 4 < remainder:
                        plate = "тарелок"
                msg = ("<:borschtsch:255796379186757642>\nТы украл {} {} борща у "
                       "{}!".format(stolen, plate, user.name))
            else:
                msg = "Моника ничего не нашла. <:refrigerator:470613165563052054>"
        return msg

    def random_user(self, settings, author, server):
        filter_users = [server.get_member(x) for x in settings["Players"]
                        if hasattr(server.get_member(x), "name")]
        legit_users = [x for x in filter_users if x.id != author.id and x is not x.bot]

        users = [x for x in legit_users if settings["Players"][x.id]["Borshs"] > 0]

        if not users:
            user = "Fail"
        else:
            user = random.choice(users)
            if user == user.bot:
                users.remove(user.bot)
                settings["Players"].pop(user.bot)
                dataIO.save_json(self.file_path, self.system)
                user = random.choice(users)
            self.account_check(settings, user)
        return user

    def account_check(self, settings, userobj):
        if userobj.id not in settings["Players"]:
            settings["Players"][userobj.id] = {"Borshs": 0,
                                               "Steal CD": 0,
                                               "borsh CD": 0}
            dataIO.save_json(self.file_path, self.system)

    def time_formatting(self, seconds):
        # Calculate the time and input into a dict to plural the strings later.
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        data = PluralDict({'hour': h, 'minute': m, 'second': s})
        if h > 0:
            fmt = "{hour} hour{hour(s)}"
            if data["minute"] > 0 and data["second"] > 0:
                fmt += ", {minute} minute{minute(s)}, and {second} second{second(s)}"
            if data["second"] > 0 == data["minute"]:
                fmt += ", and {second} second{second(s)}"
            msg = fmt.format_map(data)
        elif h == 0 and m > 0:
            if data["second"] == 0:
                fmt = "{minute} minute{minute(s)}"
            else:
                fmt = "{minute} minute{minute(s)}, and {second} second{second(s)}"
            msg = fmt.format_map(data)
        elif m == 0 and h == 0 and s > 0:
            fmt = "{second} second{second(s)}"
            msg = fmt.format_map(data)
        elif m == 0 and h == 0 and s == 0:
            msg = "None"
        return msg

    def check_server_settings(self, server):
        if server.id not in self.system["Servers"]:
            self.system["Servers"][server.id] = {"Players": {},
                                                 "Config": {"Steal CD": 5,
                                                            "Borsh CD": 5}
                                                 }
            dataIO.save_json(self.file_path, self.system)
            print("Creating default heist settings for Server: {}".format(server.name))
            path = self.system["Servers"][server.id]
            return path
        else:
            path = self.system["Servers"][server.id]
            return path


def check_folders():
    if not os.path.exists("data/KavbweurCogs/borsh"):
        print("Creating data/KavbweurCogs/borsh folder...")
        os.makedirs("data/KavbweurCogs/borsh")


def check_files():
    default = {"Servers": {}}

    f = "data/KavbweurCogs/borsh/borsh.json"
    if not dataIO.is_valid_json(f):
        print("Creating default borsh.json...")
        dataIO.save_json(f, default)


def setup(bot):
    check_folders()
    check_files()
    bot.add_cog(Borsh(bot))
