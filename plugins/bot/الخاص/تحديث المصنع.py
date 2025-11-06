# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

from os import execle, environ
from sys import executable

from pyrogram import Client

from ahmedyad.ahmedgit import update_bot
from ahmedyad.filters import text_command


@Client.on_message(text_command('تحديث البوت', bot_owner=True, chats='pv'))
async def update_files(client, message):
    m = await message.reply('جاري تحديث البوت')
    res = update_bot()
    if res:
        await m.edit(f"جاري اعاده تشغيل اليوت")
        args = [executable, "main.py"]
        execle(executable, *args, environ)
    else:
        await m.edit("حدث خطأ ما")