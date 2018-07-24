# -*- coding: utf-8 -*-
import discord
import random
import itertools
import time
import asyncio
import functools
import os
import html
import subprocess
import re
import logging
import collections
import copy
import math
import time
import inspect
from cogs.utils import checks
from xml.etree import ElementTree as ET
from random import choice, shuffle
from copy import deepcopy
from cogs.utils.dataIO import dataIO
from discord.ext import commands
import threading
from cogs.utils.chat_formatting import pagify
from urllib.parse import urlparse
from __main__ import send_cmd_help, settings
from json import JSONDecodeError
try:
    from imgurpython import ImgurClient
except:
    ImgurClient = False


CLIENT_ID = "1fd3ef04daf8cab"
CLIENT_SECRET = "f963e574e8e3c17993c933af4f0522e1dc01e230"
default_settings = {
    "VOTE_DURATION": 60
}




class Catbug_old:
    def __init__(self, bot):
        self.bot = bot
        self.stopwatches = {}
        self.vote_sessions = []
        self.imgur = ImgurClient(CLIENT_ID, CLIENT_SECRET)
        self.file_path = "data/catbug/sets.json"
        self.CatBug = dataIO.load_json(self.file_path)
        
    def save(self):
        dataIO.save_json(self.file_path, self.to_json())
    
    
    
    @commands.command(pass_context=True, name="invite")
    async def invite_bot(self, ctx):
        """Пригласить Монику на свой сервер."""
        await self.bot.say("Пригласить Монику на свой сервер можно по данной ссылке:\n http://kavbweur.website/invite")


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
        await self.bot.say("```" + "Сообщение после смены ракладки:\n" + text + "```")
         
    
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
        await self.bot.say("```" + "Сообщение после смены ракладки:\n" + text + "```")

    @commands.group(pass_context=True)
    async def vote(self, ctx):
        """Устроить голосование."""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    @vote.command(pass_context=True, no_pm=True)
    async def start(self, ctx, *text):
        """Начать/завершить голосование

        Пример использования:
        Начать голосование: [p]vote start Это голосование?;Да;Нет;Возможно
        Завершить голосование: vote stop"""
        message = ctx.message
        if len(text) == 1:
            if text[0].lower() == "stop":
                await self.endvote(message)
                return
        if len(text) == 1:
            if text[0].lower() == "vote":
                await self.votetime(message)
                return
        
        if not self.getVoteByChannel(message):
            check = " ".join(text).lower()
            if "@everyone" in check or "@here" in check:
                await self.bot.say("Я не настолько громкая, чтобы всех позвать на голосование.")
                return
            p = NewVote(message, self)
            if p.valid:
                self.vote_sessions.append(p)
                await p.start(ctx.message.server)
            else:
                await self.bot.say("Для того, чтобы начать голосование введите: вопрос?;вариант1;вариант2")
        else:
            await self.bot.say("Голосование уже проходит в данном текстовом канале.")
    async def endvote(self, message):
        if self.getVoteByChannel(message):
            p = self.getVoteByChannel(message)
            if p.author == message.author.id: # or isMemberAdmin(message)
                await self.getVoteByChannel(message).endVote()
            else:
                if message.author.id == settings.owner:
                    await self.getVoteByChannel(message).endVote()
                else:
                    await self.bot.say("Только создавший голосование или owner может остановить его.")
        else:
            await self.bot.say("Нельзя остановить голосование, если его нет.")
    
    def getVoteByChannel(self, message):
        for vote in self.vote_sessions:
            if vote.channel == message.channel:
                return vote
        return False

    async def check_vote_votes(self, message):
        if message.author.id != self.bot.user.id:
            if self.getVoteByChannel(message):
                    await self.getVoteByChannel(message).checkAnswer(message)

    def fetch_joined_at(self, user, server):
        """Just a special case for someone special :^)"""
        if user.id == "96130341705637888" and server.id == "133049272517001216":
            return datetime.datetime(2016, 1, 10, 6, 8, 4, 443000)
        else:
            return user.joined_at
    
    @vote.command(pass_context=True)
    @checks.admin_or_permissions(manage_server=True)
    async def time(self,ctx, *, text: int):
        """Установить время для голосования."""
        server = ctx.message.server
        if server.id not in self.CatBug:
            self.CatBug[server.id] = deepcopy(default_settings)
            dataIO.save_json(self.file_path, self.CatBug)
        self.CatBug[server.id]["VOTE_DURATION"] = text
        dataIO.save_json(self.file_path, self.CatBug)
        await self.bot.say("Время для голосований установлено.")
    
    @commands.command(pass_context=True, name="requirementinstall")
    @checks.is_owner()
    async def install_req(self, ctx, requirement: str):
        """Установка библиотек в обход консоли."""
        await self.bot.say(await self.bot.pip_install(requirement))
        
class NewVote:
    def __init__(self, message, main):
        server = message.server
        self.file_path = "data/catbug/sets.json"
        self.CatBug = dataIO.load_json(self.file_path)
        self.channel = message.channel
        self.author = message.author.id
        self.client = main.bot
        self.vote_sessions = main.vote_sessions
        msg = message.content[6:]
        msg = msg.split(";")
        if len(msg) < 2: # Needs at least one question and 2 choices
            self.valid = False
            return None
        else:
            self.valid = True
        self.already_voted = []
        self.question = msg[0]
        msg.remove(self.question)
        self.answers = {}
        i = 1
        for answer in msg: # {id : {answer, votes}}
            self.answers[i] = {"ANSWER" : answer, "VOTES" : 0}
            i += 1

    async def start(self, server):
        settings = self.CatBug[server.id]["VOTE_DURATION"]
        print(self.CatBug[server.id]["VOTE_DURATION"])
        msg = "**Голосование начинается!**\n\n{}\n\n".format(self.question)
        for id, data in self.answers.items():
            msg += "{}. *{}*\n".format(id, data["ANSWER"])
        msg += "\nВыберите свой вариант!"
        await self.client.send_message(self.channel, msg)
        await asyncio.sleep(settings)
        if self.valid:
            await self.endVote()

    async def endVote(self):
        self.valid = False
        msg = "**Голосование завершено!**\n\n{}\n\n".format(self.question)
        for data in self.answers.values():
            msg += "*{}* - {} голосов\n".format(data["ANSWER"], str(data["VOTES"]))
        await self.client.send_message(self.channel, msg)
        self.vote_sessions.remove(self)

    async def checkAnswer(self, message):
        try:
            i = int(message.content)
            if i in self.answers.keys():
                if message.author.id not in self.already_voted:
                    data = self.answers[i]
                    data["VOTES"] += 1
                    self.answers[i] = data
                    self.already_voted.append(message.author.id)
                    await self.client.delete_message(message)
        except ValueError:
            pass

    


def check_folders():
    if not os.path.exists("data/catbug"):
        print("Creating data/catbug folder...")
        os.makedirs("data/catbug")


def check_files():
    f = 'data/catbug/sets.json'
    if not dataIO.is_valid_json(f):
        print("Adding catbug sets.json...")
        dataIO.save_json(f)   
        
def setup(bot):
    check_folders()
    check_files()
    n = Catbug_old(bot)
    bot.add_listener(n.check_vote_votes, "on_message")
    bot.add_cog(n)
    
