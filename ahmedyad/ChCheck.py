from pyrogram import Client
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telebot.asyncio_helper import ApiTelegramException

from ahmedyad.database import database


async def send_subscription_message(message: Message, chat_id, user_id, telebot):
    ch = await telebot.get_chat(chat_id)
    link = f"https://t.me/{ch.username}" if ch.username else ch.invite_link
    markup = InlineKeyboardMarkup([[InlineKeyboardButton(ch.title, url=link)]])
    msg = (
        "⌯︙عذࢪاَ حبيبي \n"
        "⌯︙عـليك الاشـتࢪاك في قنـاة البـوت اولآ\n"
        "ꔹ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ ┉ꔹ"
    )
    await message.reply_text(msg, reply_markup=markup)


async def is_user_subscribed(chat_id, user_id, telebot):
    try:
        member = await telebot.get_chat_member(chat_id, int(user_id))
        return member.status != 'left'
    except:
        return False


async def is_subscribed_and_notify(client: Client, message: Message) -> bool:
    if message.chat.type == ChatType.CHANNEL:
        return True

    user_id = message.from_user.id

    try:
        if not await database.sismember(f"{client.Ftelebot.bot_id}:Bots:Subscription", client.me.id):
            channel_id = await database.get(f"{client.Ftelebot.bot_id}:ChCheckToBots")
            if channel_id and not await is_user_subscribed(channel_id, user_id, client.Ftelebot):
                await send_subscription_message(message, channel_id, user_id, client.Ftelebot)
                return False
    except Exception as e:
        print(e)

    chid = await database.get(f"{client.me.id}:ChCheck")
    if chid:
        try:
            if not await is_user_subscribed(chid, user_id, client.telebot):
                await send_subscription_message(message, chid, user_id, client.telebot)
                return False
        except ApiTelegramException as e:
            if 'member list is inaccessible' in str(e):
                await database.delete(f"{client.me.id}:ChCheck")

    return True


async def check_user_subscription(_, client: Client, message: Message):
    return await is_subscribed_and_notify(client, message)

