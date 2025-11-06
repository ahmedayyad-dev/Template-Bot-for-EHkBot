# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message

from ahmedyad.filters import text_command
from info import bot_owner_id


@Client.on_message(text_command(['مطور', "المطور", "مالك البوت"],chats='all'))
async def yNNNYY1NNY(client: Client, message: Message):
    sudo_info = await client.get_chat(bot_owner_id)
    bio = sudo_info.bio or "لا يوجد"

    if sudo_info.birthday:
        birthday_day = str(sudo_info.birthday.day)
        birthday_month = str(sudo_info.birthday.month)
        birthday_year = str(sudo_info.birthday.year)
        if birthday_month or birthday_year:
            birthday_day += '/'
        if birthday_year:
            birthday_month += '/'
        birthday = f"{birthday_day}{birthday_month}{birthday_year}"
    else:
        birthday = "لا يوجد"

    if sudo_info.usernames:
        usernames = ''
        for Username in sudo_info.usernames:
            usernames += f'@{Username.username} -'
        usernames = usernames[:-2]
    elif sudo_info.username:
        usernames = f'@{sudo_info.username}'
    else:
        usernames = "لا يوجد"
    caption = (
        "\n• الاسم ⦂ {}\n• أسماء المستخدمين ⦂ {}\n• السيرة الذاتية ⦂ {}\n• تاريخ الميلاد ⦂ {}\n".format(
            f"{sudo_info.first_name} {sudo_info.last_name or ''}",
            usernames,
            bio,
            birthday
        )
    )
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton(f"{sudo_info.first_name} {sudo_info.last_name or ''}", user_id=sudo_info.id)]]
    )
    if sudo_info.personal_chat:
        reply_markup.inline_keyboard.append([InlineKeyboardButton(sudo_info.personal_chat.title,
                                                                  url=f"https://t.me/{sudo_info.personal_chat.username}")])

    if sudo_info.photo:
        async for photo in client.get_chat_photos(sudo_info.id, 1):
            return await message.reply_photo(photo.file_id, caption=caption, reply_markup=reply_markup)
    else:
        await message.reply(caption, reply_markup=reply_markup)

