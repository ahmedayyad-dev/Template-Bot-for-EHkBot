# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.
from pyrogram import Client, filters

from ahmedyad.database import database
from ahmedyad.filters import text_command



@Client.on_message(text_command('تفعيل الاشتراك الاجباري', bot_owner=True, chats='pv'))
async def SetChCheck(client, message):
    msg = await message.askWithReq('ارسل معرف الدردشه مع @ الان', )
    try:
        await client.telebot.get_chat_member(msg.text, client.me.id)
        ch = await client.telebot.get_chat(msg.text)
    except Exception as e:
        print(e)
        return await msg.reply('تاكد ان البوت مرفوع في القناه او الجروب')
    await database.set(f'{client.me.id}:ChCheck', ch.id)
    await msg.reply('تم تفعيل الاشتراك الاجباري')


@Client.on_message(text_command('تعطيل الاشتراك الاجباري', bot_owner=True, chats='pv'))
async def DelChCheck(client, message):
    await database.delete(f'{client.me.id}:ChCheck')
    await message.reply('تم تعطيل الاشتراك الاجباري')
