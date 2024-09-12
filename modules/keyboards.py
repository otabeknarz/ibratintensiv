from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)


class Buttons:
    def __init__(self):
        self.main_markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🔗 Havola olish")],
                [KeyboardButton(text="📄 Shaxsiy kabinet")]
            ],
            resize_keyboard=True
        )


class InlineButtons:
    def __init__(self):
        self.channel_markup = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="KANALGA O'TISH",
                        url="https://t.me/+dAUHD6dKTrxmMGEy",
                        callback_data="channel",
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="Tekshirish",
                        callback_data="subscribed",
                    )
                ]
            ]
        )
