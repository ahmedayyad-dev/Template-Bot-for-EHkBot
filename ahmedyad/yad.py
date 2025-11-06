# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.
from os import environ
from typing import Optional

from pyrogram import Client
from pyrogram.types import User
from telebot.async_telebot import AsyncTeleBot

from ahmedyad.database import database
from info import bot_owner_id, token, Fowner_id, FBotToken,api_id, api_hash
from os import path
from tempfile import gettempdir

downloads_path = path.join(gettempdir(), 'downloads')

Bot = Client(
    "AhmedAyyadBot",
    api_id,
    api_hash,
    plugins=dict(root="plugins/bot"),
    bot_token=token,
    ipv6=False,
)

Bot.telebot = AsyncTeleBot(token)
Bot.Ftelebot = AsyncTeleBot(FBotToken)

Bot.photo = 'https://drive.google.com/uc?id=10cuxPvT9QhZRvHc44cuNuC0-P2nYNQPJ'
# Bot.me =
admin_users = [944353237, bot_owner_id,Fowner_id]

async def log_chat(text='', *args, only_is_set=False, **kwargs):
    if not text:
        if await database.get(f'{Bot.me.id}:logChat'):
            chat = await database.get(f'{Bot.me.id}:logChat')
        else:
            chat = bot_owner_id
        return int(chat)
    else:
        try:
            if only_is_set and not await database.get(f'{Bot.me.id}:logChat'):
                return 'The log chat is not set'
            return await Bot.send_message(await log_chat(), text, *args, **kwargs)
        except Exception as e:
            print(f"send to log chat {e}")

def format_duration(seconds):
    if not isinstance(seconds, (int, float)):
        return seconds
    seconds = int(seconds)
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60

    if hours > 0:
        return f"{hours}:{minutes:02}:{seconds:02}"
    else:
        return f"{minutes}:{seconds:02}"


class CommandCancel(Exception):
    pass
