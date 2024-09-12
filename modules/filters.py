from aiogram.filters import Filter
from aiogram.types import Message


class TextEqualsFilter(Filter):
    def __init__(self, message: str):
        self.message = message

    async def __call__(self, message: Message):
        return message.text == self.message
