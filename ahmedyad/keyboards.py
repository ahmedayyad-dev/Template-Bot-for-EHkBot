# Copyright (c) 2025 Ahmed Ayyad (ahmedyad200)
# Licensed under Custom Proprietary License
# Redistribution and resale are prohibited.

from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

from ahmedyad.yad import Bot, admin_users
from info import channel, bot_owner_id

play_text = """
{}
title: {}
duration: {}
"""

play_keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("‹ تخطي ›", callback_data=f"skip"),
                InlineKeyboardButton("‹ انهاء ›", callback_data=f"stop"),
            ],
            [
                InlineKeyboardButton("‹ توقف ›", callback_data=f"pause"),
                InlineKeyboardButton("‹ استئناف ›", callback_data=f"resume"),
            ],
            [
                InlineKeyboardButton("‹ قناة السورس ›", url=f"https://t.me/{channel}"),
            ],
        ]
    )


cancel_key = ReplyKeyboardMarkup(
    [
        ["الغاء ورجوع"],
    ],
    resize_keyboard=True
)


def get_keyboard(user_id=None):
    if user_id in admin_users or user_id == 'admin':
        return ReplyKeyboardMarkup(
        [
                ["الاحصائيات", "تعيين مجموعه السجل"],
                ["اذاعه قنوات","اذاعه جروبات","اذاعه خاص"],
                ["تعطيل الاشتراك الاجباري", "تفعيل الاشتراك الاجباري"],
                ["حذف مساعد", "اضافه مساعد"],
                ["اعاده تشغيل الحسابات المساعده"],
            ],
            True,True
        )
    elif user_id == 1:
        return ReplyKeyboardMarkup(
        [
                ["مالك البوت"],
                ["التحميل من جميع المواقع"],
        ],
            True,True
        )
    else:
        return InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("اضغط لاضافه البوت لمجموعتك", url=f"https://t.me/{Bot.me.username}?startgroup=true"),
                ],
                [
                    InlineKeyboardButton("‹ قناة السورس ›", url=f"https://t.me/{channel}"),
                    InlineKeyboardButton("‹ مالك البوت ›", user_id=bot_owner_id),
                ],
            ]
        )
