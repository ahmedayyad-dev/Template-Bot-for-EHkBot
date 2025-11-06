# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

from ahmedyad.userbots import userbot
from pytgcalls import filters as call_filters, PyTgCalls
from pytgcalls.types import ChatUpdate, Update

from ahmedyad.skip import skip


@userbot.on_update(call_filters.chat_update(ChatUpdate.Status.LEFT_CALL))
async def kicked_handler(client: PyTgCalls, update: Update):
    userbot1 = await userbot.get(update.chat_id, only_userbot=True, userbot_id=client.mtproto_client.me.id)
    await userbot1.leave_call(update.chat_id)

@userbot.on_update(call_filters.stream_end())
async def on_end_handler(client: PyTgCalls, update: Update):
    userbot1 = await userbot.get(update.chat_id, only_userbot=True, userbot_id=client.mtproto_client.me.id)
    await skip(update.chat_id, userbot1)

