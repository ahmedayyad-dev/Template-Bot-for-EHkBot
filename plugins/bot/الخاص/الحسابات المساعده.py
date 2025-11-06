# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.
import string
from os import environ
from random import randint, choices

from pyrogram import Client
from pyrogram.enums import SentCodeType
from pyrogram.errors import SessionPasswordNeeded
from pyrogram.types import Message, ReplyKeyboardMarkup

from ahmedyad.database import database
from ahmedyad.filters import text_command, subscription
from ahmedyad.userbots import userbot
from info import api_id, api_hash

@Client.on_message(text_command("اضافه مساعد", bot_owner=True, chats='pv') & subscription)
async def pNNNYN2NYA(client: Client, message: Message):
    message = await message.askWithReq("ارسل كود الجلسه او رقم الهاتف مع رمز الدوله")
    if message.text.replace('+','').isdigit():
        phone_number = message.text.replace('+','')
        msg = await message.reply('جاري انشاء الاتصال مع التليجرام')
        assbot = Client(f"assbot:{randint(1, 9999)}", api_id, api_hash, in_memory=True)
        await assbot.connect()
        await msg.edit('جاري ارسال الكود')
        code = await assbot.send_code(phone_number)
        code_type = {
            SentCodeType.APP: 'تطبيق التليجرام',
            SentCodeType.CALL: 'مكالمه صوتيه',
            SentCodeType.FLASH_CALL: 'مكالمه سريعه',
            SentCodeType.MISSED_CALL: 'مكالمه فائته',
            SentCodeType.SMS: 'رسائل الهاتف',
            SentCodeType.EMAIL_CODE: 'البريد الالكتروني',
            SentCodeType.FRAGMENT_SMS: 'رسائل مصنه فراجيمنت',
        }[code.type]
        message = await message.askWithReq(f"تم ارسال الكود عبر {code_type} اعد ارساله الي هنا بهذا الشكل 1.2.3.4.5", )
        phone_code = message.text
        try:
            await assbot.sign_in(phone_number, code.phone_code_hash, phone_code)
        except SessionPasswordNeeded:
            message = await message.askWithReq("ارسل كلمه المرور", )
            password = message.text
            while True:
                try:
                    await assbot.check_password(password)
                    break
                except Exception as e:
                    print(e)
                    msg = await message.askWithReq("كلمه المرور خطأ اعد ارسالها", )
                    password = msg.text
        userbot_session = await assbot.export_session_string()

        user_id = (await assbot.get_me()).id
        try:
            await assbot.set_username(f'{client.me.username}_{user_id}')
        except Exception as e:
            await msg.reply(str(e))
            code = ''.join(choices(string.ascii_lowercase + string.digits, k=4))
            await assbot.set_username(f'{client.me.username}_{user_id}_{code}')

        await assbot.update_profile(
            first_name=client.me.first_name,
            last_name="",
            bio=f'الحساب المساعد للبوت @{client.me.username}'
        )

        try:
            await assbot.set_profile_photo(photo=client.photo)
        except Exception as e:
            print(e)
        await assbot.disconnect()

    else:
        userbot_session = message.text
    await database.sadd(f'{client.me.id}:userbots', userbot_session)
    await msg.reply("تم حفظ الجلسه وجاري تشغيلها\n<code>{}</code>".format(userbot_session))
    await userbot.start(session_string=userbot_session)

@Client.on_message(text_command("حذف مساعد", bot_owner=True, chats='pv') & subscription)
async def pNNNYN6NYA(client: Client, message: Message):
    key = ReplyKeyboardMarkup([], resize_keyboard=True)
    for user in userbot._userbots_pool:
        key.keyboard.append([str(user.mtproto_client.me.id)])
    msg = await message.askWithReq("اختار ايدي الحساب", reply_markup=key)
    assbot = next((ub for ub in userbot._userbots_pool if ub.mtproto_client.me.id == int(msg.text)), None)
    await database.srem(f'{client.me.id}:userbots', assbot.mtproto_client.session_string)
    await msg.reply("تم حذف الحساب المساعد من قاعده البيانات\n<code>{}</code>".format(assbot.mtproto_client.session_string))


@Client.on_message(text_command("اعاده تشغيل الحسابات المساعده", bot_owner=True, chats='pv') & subscription)
async def pNNNYN9NYA(client: Client, message: Message):
    msg = await message.reply('جاري اعاده تشغيل الحسابات المساعده')
    await userbot.stop()
    await userbot.start()
    await msg.edit("تم اعاده تشغيل جميع الحسابات المساعده")




