# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

from ahmedyad.keyboards import play_keyboard
from ahmedyad.queues import get_queue, pop_an_item,clear_queue
from ahmedyad.userbots import userbot
from ahmedyad.yad import Bot

async def skip(chat_id: int, ub: userbot = None, num = 1):
    if ub is None:
        ub = await userbot.get(chat_id)
    chat_queue = get_queue(chat_id)
    if len(chat_queue) <= num:
        await ub.leave_call()
        clear_queue(chat_id)
        return 1
    else:
        await ub.play(chat_queue[num][0])
        photo = caption = None
        try:
            photo = chat_queue[num][1]
            caption = chat_queue[num][2]
        except:
            pass
        pop_an_item(chat_id)
        if photo and caption:
            await Bot.send_photo(chat_id, photo, caption, reply_markup=play_keyboard)
        return 2
