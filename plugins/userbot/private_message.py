from pyrogram import Client, filters

from ahmedyad.yad import Bot


@Client.on_message(filters.private & ~filters.bot & ~filters.service & ~filters.me)
async def private_message(client, update):
    inline = await client.get_inline_bot_results(Bot.me.username, "inline_ass_by_ahmedyad")
    await client.send_inline_bot_result(
        update.chat.id,
        inline.query_id,
        inline.results[0].id,
    )
