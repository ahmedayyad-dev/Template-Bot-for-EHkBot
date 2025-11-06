# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

from pyrogram import Client
from pyrogram.types import Message

from ahmedyad.filters import text_command, subscription


@Client.on_message(text_command('تعيين مجموعه السجل', bot_owner=True, chats='pv') & subscription)
async def pv_set_group_log(client: Client, message: Message):
    await message.reply_text("ارسل هذا الامر في المجموعه\n/set_group_log")

