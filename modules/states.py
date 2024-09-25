from aiogram.filters.state import State, StatesGroup


class PostSendState(StatesGroup):
    post_text = State()
