# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

from pyrogram import Client
from pyrogram.types import Message

from ahmedyad.ChCheck import is_subscribed_and_notify
from ahmedyad.database import database
from ahmedyad.filters import text_command, subscription
from ahmedyad.keyboards import get_keyboard
from ahmedyad.yad import admin_users


@Client.on_message(text_command('start', command=True, chats='pv'))
async def start(client: Client, message: Message):
    if message.from_user.id in admin_users:
        await message.reply_text('اهلا عزيزي مالك البوت',reply_markup=get_keyboard('admin'))
    elif is_subscribed_and_notify(client, message):
        await message.reply_photo(
            client.photo,
            caption="• اهلا بك عزيزي .\n• يمڪنني تشغيل الموسيقى في الاتصال .\n• ادعم التشغيل في المجموعات والقنوات .\n• ⎯ ⎯ ⎯ ⎯\n",
            reply_markup=get_keyboard()
        )
        await message.reply("كسم اسرائيل",reply_markup=get_keyboard(1))


@Client.on_message(text_command("الاحصائيات", bot_owner=True, chats='pv') & subscription)
async def pNNNYN2NYA(client: Client, message: Message):
    await message.reply(
        "• عدد المشتركين ⦂ {}\n• عدد المجموعات ⦂ {}\n• عدد القنوات ⦂ {}".format(
            await database.scard(f'{client.me.id}:private'),
            await database.scard(f'{client.me.id}:group'),
            await database.scard(f'{client.me.id}:channel')
        )
    )


@Client.on_message(
    text_command(['خاص', 'جروبات', 'قنوات'], bot_owner=True, command=True, chats='pv', prefixes='اذاعه ') & subscription)
async def BroadCast(client: Client, message: Message):
    msg = await message.askWithReq('ارسل الرساله الان')
    await msg.reply_text('جاري عمل الاذاعه')
    for chat in await database.smembers(f'{client.me.id}:'+ {'خاص': 'private','جروبات':'group','قنوات': 'channel'}[message.command[0]]):
        await client.telebot.copy_message(int(chat), msg.chat.id, msg.id)
    await msg.reply('تم عمل الاذاعه')
