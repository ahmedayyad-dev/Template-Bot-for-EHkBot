# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.
import os
import re

from ayyad_apis import YouTubeAPI, YouTubeAPIResponseError
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from youtubesearchpython.__future__ import VideosSearch

from ahmedyad.filters import text_command, subscription
from ahmedyad.yad import downloads_path
from info import rapidapi_key

platforms = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("YouTube", callback_data="ddddddddd"),
        ],
        [
            InlineKeyboardButton("Facebook", callback_data="ddddddddd"),
        ],
        [
            InlineKeyboardButton("TikTok", callback_data="ddddddddd"),
        ],
        [
            InlineKeyboardButton("Instagram", callback_data="ddddddddd"),
        ],
        [
            InlineKeyboardButton("X", callback_data="ddddddddd"),
        ],
        [
            InlineKeyboardButton("soundcloud", callback_data="ddddddddd"),
        ],
    ]
)

@Client.on_message(text_command(['تحميل', "فيد", "التحميل من جميع المواقع"], command=True, chats='all', prefixes='') & subscription)
@Client.on_callback_query(text_command('ddddddddd',chats='all'))
async def Download(client: Client, message: Message):
    if isinstance(message, Message):
        media_play = 'video' if message.text.split(None, 1)[0] == "فيد" else 'audio'
        if message.text == "التحميل من جميع المواقع":
            return await message.reply("اختار الموقع الي تريد تحمل منه",reply_markup=platforms)
        if len(message.command) < 2:
            message = await message.askWithReq('ارسل الان ما تريد تحميله')
            query = message.text
        else:
            query = message.text.split(None, 1)[1]
    elif isinstance(message, CallbackQuery):
        await message.message.edit('ارسل الرابط الان')
        message = await client.wait_for_message(message.message.chat.id, filters=filters.user(message.from_user.id))
        query = message.text
        media_play = 'audio'

    is_youtube = query.startswith('http') and bool(re.search(r"(?:youtube\.com|youtu\.be)", query))
    extra_info = {}
    files_to_delete = []
    try:
        async with YouTubeAPI(rapidapi_key) as api:
            if not query.startswith('http'):
                msg = await message.reply("جاري البحث عن ({})".format(query))
                search_result = await VideosSearch(query, limit=1).next()
                await msg.edit("جاري تحميل ({})".format(search_result['result'][0]['title']))
                file_path = (await api.youtube_to_telegram(search_result['result'][0]['id'], media_play)).telegram.file_url

            elif is_youtube:
                msg = await message.reply("جاري التحميل...")
                file_path = (await api.youtube_to_telegram(query, media_play)).telegram.file_url

            else:
                msg = await message.reply("جاري التحميل...")
                data = await api.video_info(query)

                for format_item in data.formats:
                    if format_item.get("video_ext" if media_play == 'video' else "audio_ext", "none") != "none":
                        file_path = (await api.download_file(
                            format_item.get("url"),
                            f'{downloads_path}/{data.id}.{"mp4" if media_play == "video" else "m4a"}'
                        )).file_path
                        files_to_delete.append(file_path)

                        extra_info = {'duration': int(data.duration_seconds)}
                        if media_play == 'audio':
                            extra_info['title'] = data.title
                            if data.uploader_info:
                                extra_info['performer'] = data.uploader_info.get("name")

                        if data.thumbnail:
                            extra_info['thumb'] = (await api.download_file(data.thumbnail, f'{downloads_path}/{data.id}_thumb.jpg')).file_path
                            files_to_delete.append(extra_info['thumb'])
                        break
                else:
                    return await msg.edit("⚠️ لم يتم العثور على صيغة مناسبة للتحميل")
    except YouTubeAPIResponseError as e:
        return await msg.edit(str(e.message))

    await (message.reply_audio if media_play == 'audio' else message.reply_video)(
        file_path, caption="➤ @{}".format(client.me.username), **extra_info
    )

    for file in files_to_delete:
        try:
            os.remove(file)
        except:
            pass

    await msg.delete()



