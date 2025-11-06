from pyrogram import Client
from pyrogram.types import Message

from ahmedyad.filters import text_command
from ahmedyad.database import database

@Client.on_message(text_command('set_group_log', bot_owner=True, command=True))
async def gr_set_group_log(client: Client, message: Message):
    await database.set(f'{client.me.username}:logChat',message.chat.id)
    await message.reply('تم حفظ مجموعه السجل بنجاح')

