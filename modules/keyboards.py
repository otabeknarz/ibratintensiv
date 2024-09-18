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
                [KeyboardButton(text="📄 Shaxsiy kabinet")],
            ],
            resize_keyboard=True,
        )

        self.main_markup_admin = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="🔗 Havola olish")],
                [KeyboardButton(text="📄 Shaxsiy kabinet")],
                [KeyboardButton(text="📊 Statistika")],
            ],
            resize_keyboard=True,
        )


def get_channel_markup(friend_id: str | int | None) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
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
                    callback_data=(
                        f"subscribed:{friend_id}" if friend_id else "subscribed"
                    ),
                )
            ],
        ]
    )


def get_ready_markup():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Tayyorman", callback_data="ready")]
        ]
    )
