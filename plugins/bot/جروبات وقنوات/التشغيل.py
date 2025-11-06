# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.
from ayyad_apis import YouTubeAPI
from pyrogram import Client, filters
from pyrogram.types import Message, Audio
from youtubesearchpython.__future__ import VideosSearch

from ahmedyad.filters import text_command, subscription
from ahmedyad.keyboards import play_keyboard, play_text
from ahmedyad.queues import get_queue, add_to_queue, add_list_to_queue
from ahmedyad.userbots import userbot
from ahmedyad.yad import downloads_path, format_duration
from cover import generate_cover
from info import rapidapi_key


@Client.on_message(text_command(["شغل", "تشغيل", "فيديو"], command=True, prefixes='') & subscription)
async def Play(client: Client, message: Message):
    media_play = 'video' if message.text.split(None, 1)[0] == "فيديو" else 'audio'
    msg = await message.reply_text('جاري الحصول علي الحساب المساعد للمجموعه')
    chat_userbot = await userbot.get(message.chat.id)
    thumbnail_path = None
    view_count = 0
    if not message.reply_to_message or len(message.command) >= 2:
        if len(message.command) < 2:
            await msg.edit('ارسل الان ما تريد تشغيله')
            message = await client.wait_for_message(message.chat.id, filters=filters.user(message.from_user.id if message.from_user else message.chat.id))
            query = message.text
            use = message.reply_text
        else:
            query = message.text.split(maxsplit=1)[1]
            use = msg.edit
        msg = await use("جاري البحث عن ({})".format(query))
        search_result = await VideosSearch(query, limit=1).next()
        view_count = search_result['result'][0]['viewCount']['short']
        await msg.edit("جاري تحميل ({})".format(search_result['result'][0]['title']))
        async with YouTubeAPI(rapidapi_key) as api:
            api_result = await api.youtube_to_telegram(search_result['result'][0]['id'],media_play)
            media_msg = await client.get_messages(api_result.telegram.chat_username, int(api_result.telegram.message_id))
    else:
        await msg.edit("جاري تحميل")
        media_msg = message.reply_to_message
    media: Audio = getattr(media_msg, media_msg.media.name.lower())
    if media.thumbs:
        thumbnail_path = await client.download_media(media.thumbs[0].file_id,file_name=f'{downloads_path}/{media.thumbs[0].file_id}.png')
    file_path = await media_msg.download("{}/{}".format(downloads_path,media.file_name))
    if not get_queue(message.chat.id):
        await msg.edit('جاري التشغيل')
        await chat_userbot.play(file_path)
        pos = add_to_queue(message.chat.id, file_path)
        thumb = await generate_cover(format_duration(media.duration) or 1,thumbnail_path,view_count,"PLAYING NOW") if thumbnail_path else "cover/start_stream_photo.png"
        await client.send_photo(
            message.chat.id,
            thumb,
            play_text.format("Play started",media.title or media.file_name, format_duration(media.duration) or 1),
            reply_markup=play_keyboard
        )
    else:
        pos = add_to_queue(message.chat.id, file_path)
        thumb = await generate_cover(format_duration(media.duration) or 1,thumbnail_path,view_count,f"Add to queue {pos}") if thumbnail_path else "cover/added_photo.png"
        await client.send_photo(
            message.chat.id,
            thumb,
            play_text.format(f"Add to queue {pos}",media.title or media.file_name, format_duration(media.duration) or 1),
            reply_markup=play_keyboard
        )
    add_list_to_queue(message.chat.id, pos,[thumb, play_text.format("Play started",media.title or media.file_name, format_duration(media.duration) or 1)])
    await msg.delete()
