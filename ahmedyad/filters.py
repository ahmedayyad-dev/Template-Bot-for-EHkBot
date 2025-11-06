# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.
from typing import Union, List

from pyrogram import filters
from pyrogram.types import Message, CallbackQuery

from ahmedyad.ChCheck import check_user_subscription
from ahmedyad.queues import get_queue
from ahmedyad.yad import admin_users


def text_command(texts: Union[str, List[str]], bot_owner=False, command=False, chats=None, prefixes='/'):

    if command:
        text_filter = filters.command(texts, prefixes=prefixes)
    else:
        if isinstance(texts, str):
            text_filter = filters.regex(rf"^{texts}$")
        else:
            text_filter = filters.regex(rf"^({'|'.join(texts)})$")


    if chats == 'pv':
        chat_filter = filters.private
    elif chats == 'all':
        chat_filter = filters.all
    else:
        chat_filter = filters.group | filters.channel


    owner_filter = filters.user(admin_users) if bot_owner else filters.all

    return text_filter & chat_filter & owner_filter

async def play_filter(_, __, mq: Union[Message, CallbackQuery]):
    if isinstance(mq, CallbackQuery):
        if not get_queue(mq.message.chat.id):
            await mq.answer('لا يوجد تشغيل حالي', show_alert=True)
            return False
    else:
        if not get_queue(mq.chat.id):
            await mq.reply('لا يوجد تشغيل حالي')
            return False
    return True

subscription = filters.create(check_user_subscription)