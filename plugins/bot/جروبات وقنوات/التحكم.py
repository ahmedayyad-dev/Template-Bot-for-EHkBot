# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

from pyrogram import Client, filters
from pyrogram.types import Message, CallbackQuery

from ahmedyad.filters import text_command, play_filter, subscription
from ahmedyad.queues import clear_queue
from ahmedyad.skip import skip
from ahmedyad.userbots import userbot


@Client.on_message(text_command('تخطي') & filters.create(play_filter) & subscription)
async def skip_play_message(client: Client, message: Message):
    msg = await message.reply_text("جاري تخطي التشغيل الحالي")
    if await skip(msg.chat.id) == 1:
        await msg.edit("تم انهاء التشغيل لا يوجد شيئ في القائمه")
    else:
        await msg.edit("تم تخطي التشغيل الحالي")


@Client.on_callback_query(text_command('skip', chats='all') & filters.create(play_filter))
async def skip_play_callbackqueyy(client: Client, callbackqueyy: CallbackQuery):
    if await skip(callbackqueyy.message.chat.id) == 1:
        await callbackqueyy.answer("تم انهاء التشغيل لا يوجد شيئ في القائمه",show_alert=True)
    else:
        await callbackqueyy.answer("تم تخطي التشغيل الحالي",show_alert=True)


@Client.on_message(text_command(["انهاء", "ايقاف"]) & filters.create(play_filter) & subscription)
async def leave_call_play_message(client: Client, message: Message):
    msg = await message.reply("جاري انهاء التشغيل")
    ub = await userbot.get(message.chat.id, only_userbot=True)
    await ub.leave_call()
    clear_queue(message.chat.id)
    await msg.edit("تم انهاء التشغيل")


@Client.on_callback_query(text_command('stop', chats='all') & filters.create(play_filter))
async def leave_call_callbackqueyy(client: Client, callbackqueyy: CallbackQuery):
    ub = await userbot.get(callbackqueyy.message.chat.id, only_userbot=True)
    await ub.leave_call()
    clear_queue(callbackqueyy.message.chat.id)
    await callbackqueyy.answer("تم انهاء التشغيل",show_alert=True)


@Client.on_message(text_command('توقف') & filters.create(play_filter) & subscription)
async def pause_play_message(client: Client, message: Message):
    msg = await message.reply("جاري ايقاف التشغيل مؤقتا")
    ub = await userbot.get(message.chat.id, only_userbot=True)
    await ub.pause()
    await msg.edit("تم ايقاف التشغيل مؤقتا")


@Client.on_callback_query(text_command('pause', chats='all') & filters.create(play_filter))
async def pause_play_callbackqueyy(client: Client, callbackqueyy: CallbackQuery):
    ub = await userbot.get(callbackqueyy.message.chat.id, only_userbot=True)
    await ub.pause()
    await callbackqueyy.answer("تم ايقاف التشغيل مؤقتا",show_alert=True)



@Client.on_message(text_command('استئناف') & filters.create(play_filter) & subscription)
async def resume_play_message(client: Client, message: Message):
    msg = await message.reply("جاري استئناف التشغيل")
    ub = await userbot.get(message.chat.id, only_userbot=True)
    await ub.resume()
    await msg.edit("تم استئناف التشغيل")


@Client.on_callback_query(text_command('resume', chats='all') & filters.create(play_filter))
async def resume_play_callbackqueyy(client: Client, callbackqueyy: CallbackQuery):
    ub = await userbot.get(callbackqueyy.message.chat.id, only_userbot=True)
    await ub.resume()
    await callbackqueyy.answer("تم استئناف التشغيل",show_alert=True)

