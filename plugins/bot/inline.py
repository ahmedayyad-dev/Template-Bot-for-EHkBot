from pyrogram import Client
from pyrogram.types import (
    InlineQueryResultArticle,
    InputTextMessageContent
)
from youtubesearchpython.__future__ import VideosSearch

from ahmedyad.keyboards import get_keyboard


@Client.on_inline_query()
async def yYNNYY1NYm(client: Client, update):
    if update.query == "inline_ass_by_ahmedyad":
        await update.answer(
            results=[
                InlineQueryResultArticle(
                    title="ahmedyad200",
                    input_message_content=InputTextMessageContent(
                        "• اهلا عزيزي انا الحساب المساعد لبوت ↫ @{}".format(client.me.username),
                    ),
                    reply_markup=get_keyboard()
                )
            ],
            cache_time=1
        )
    elif update.query == "":
        await update.answer(
            results=[
                InlineQueryResultArticle(
                    "• أعطني شيئاً للبحث عنه على يوتيوب.",
                    InputTextMessageContent("• أعطني شيئاً للبحث عنه على يوتيوب."),
                    thumb_url='https://telegra.ph/file/5c05740138e192d06388c.png',
                ),
                InlineQueryResultArticle(
                    "• اضغط لارسال معرف البوت",
                    InputTextMessageContent(f"@{client.me.username}"),
                ),
            ],
            cache_time=1
        )
    else:
        search_results = await VideosSearch(update.query, limit=25).next()
        answers = []
        for result in search_results["result"]:
            answers.append(
                InlineQueryResultArticle(
                    title=result['title'],
                    input_message_content=InputTextMessageContent("• العنوان : <code>{}</code>\n• الرابط : {}\n".format(result['title'], result['link'])),
                    thumb_url=result['thumbnails'][0]['url']
                ),
            )

        await update.answer(results=answers)
