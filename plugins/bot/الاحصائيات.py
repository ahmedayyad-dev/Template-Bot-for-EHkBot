from pyrogram import Client
from pyrogram.enums import ChatMembersFilter, ChatMemberStatus, MessageServiceType
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from ahmedyad.database import database
from ahmedyad.yad import log_chat


@Client.on_message(group=-3)
async def yNNNYY1NNA(client, update):
    if hasattr(update, 'service') and update.service:
        if update.service == MessageServiceType.LEFT_CHAT_MEMBERS:
            if update.left_chat_member.is_self:
                return
    text = ''
    if update.chat.id < 0:
        info = (update.chat.title,update.chat.id,f"@{update.chat.username}" if update.chat.username else "لا يوجد")
        if update.chat.type == ChatType.CHANNEL:
            if await database.sadd(f'{client.me.id}:channel', update.chat.id):
                text = "• تم دخول قناة جديدة ⦂\n• اسم القناة ⦂ {}\n• ايدي القناة ⦂ {}\n• معرف القناة ⦂ {}".format(*info)
        else:
            if await database.sadd(f'{client.me.id}:group', update.chat.id):
                text = "• تم دخول مجموعة جديدة ⦂\n• اسم المجموعة ⦂ {}\n• ايدي المجموعة ⦂ {}\n• معرف المجموعة ⦂ {}".format(*info)
        if text:
            await database.delete(f'{client.me.id}:{update.chat.id}:admins')
            try:
                async for member in update.chat.get_members(filter=ChatMembersFilter.ADMINISTRATORS):
                    await database.sadd(f'{client.me.id}:{update.chat.id}:admins', member.user.id)
                await log_chat(text)
            except Exception as e:
                print(e)
                await database.srem(f'{client.me.id}:group', update.chat.id)
                await database.srem(f'{client.me.id}:channel', update.chat.id)
    else:
        if await database.sadd(f'{client.me.id}:private', update.chat.id):
            text = (
                "• تم دخول عضو جديد ⦂\n• اسمه ⦂ {} {}\n• معرفه ⦂ {}\n• الايدي ⦂ {}\n• منشن ⦂ {}".format(
                    update.from_user.first_name,
                    update.from_user.last_name if update.from_user.last_name else "",
                    f"@{update.from_user.username}" if update.from_user.username else "لا يوجد",
                    update.chat.id,
                    update.from_user.mention
                )
            )
            await log_chat(text, reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("فتح البروفايل", user_id=update.from_user.id)]]))


@Client.on_chat_member_updated(group=-3)
async def yNNNYY2NNA(client, update):
    if (
        update.old_chat_member
        and update.old_chat_member.user
        and update.old_chat_member.user.id == client.me.id
        and (
            not update.new_chat_member
            or update.new_chat_member.status != ChatMemberStatus.ADMINISTRATOR
        )
    ):

        if update.chat.type == ChatType.CHANNEL:
            text = "• تم طرد البوت من قناة ⦂\n• اسم القناة ⦂ {}\n• ايدي القناة ⦂ {}\n• معرف القناة ⦂ {}"
            await database.srem(f'{client.me.id}:channel', update.chat.id)
        else:
            text = "• تم طرد البوت من مجموعة ⦂\n• اسم المجموعة ⦂ {}\n• ايدي المجموعة ⦂ {}\n• معرف المجموعة ⦂ {}"
            await database.srem(f'{client.me.id}:group', update.chat.id)
            await client.leave_chat(update.chat.id)

        text = text.format(
            update.chat.title,
            update.chat.id,
            f"@{update.chat.username}" if update.chat.username else "لا يوجد"
        )

        await log_chat(text)
