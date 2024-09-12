import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, CommandObject
from aiogram.types import Message, BufferedInputFile
from aiogram import types

from modules.filters import TextEqualsFilter
from modules.settings import get_settings
from modules.keyboards import Buttons, InlineButtons
from modules import functions

bot_settings = get_settings()

buttons = Buttons()
inline_buttons = InlineButtons()

dp = Dispatcher()
bot = Bot(
    token=bot_settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)


@dp.message(CommandStart())
async def command_start_handler(message: Message, command: CommandObject) -> None:
    caption = f"""
    Assalomu alaykum, <strong>{message.chat.full_name}</strong>!

    Tushunishimcha, siz "2 KUNLIK JONLI INTENSIV DARSLAR"da qatnashib, ingliz tilidagi 
    muommolaringiz yechimini topib, darajangizni oshirmoqchisiz📈

    ❗️INTENSIV'da qatnashish uchun pastdagi "KANALGA O'TISH" tugmasini bosing va kanalga obuna bo'ling.
    
    So'ng “✅ Obuna bo'ldim” tugmasini bosing shunda shartlarni to'liq bajargan bo'lasiz!
    """

    with open("assets/iskandar_komoldinov.jpg", "rb") as photo:
        buff_photo = BufferedInputFile(
            file=photo.read(), filename="assets/iskandar_komoldinov.jpg"
        )
        await bot.send_photo(
            message.chat.id,
            buff_photo,
            caption=caption,
        )

    await message.answer(
        f"""
    🇬🇧Yaqinlaringiz til o'rganishiga sababchi bo'ling va sovg'alarni yutib oling🤩


    O'yin sharti : Ingliz tiliga qiziqqan do'stlaringizni INTENSIVga taklif qilish.
    
    📌G'oliblarni taklif qilgan do'stlar soniga ko'ra aniqlaymiz.
    
    🔥SOVG'ALAR bilan tanishing : 
    
    🔰1000 ta taklif - Iskandar Kamoliddonov tomonidan Londondan sovg'a 
    
    🔰750 ta taklif - Ibrat Farzandlari qoshidagi loyihalarda volontyorlik imkoniyati
    
    🔰500 ta taklif - Iskandar Kamoliddonov bilan JONLI UCHRASHUV va NONUSHTA 
    
    🔰300 ta taklif - Ibrat Farzandlari futbolkasi
    
    🔰200 ta taklif - Ibrat Farzandlari maxsus sovg'asi (daftar, ruchka, kepka)
    
    🔰100 ta taklif - Ibrat Farzandlari loyihasi ofisiga  tur
    
    🔰50 ta taklif : IELTS 7+ uchun STUDY PLAN qo'llanmasi
    
    
    ❗️DIQQAT : Sovg'alar intensivdan so'ng egalariga topshiriladi.
    
    Sovg'ali o'yinda qatnashish uchun MAXSUS havola olishingiz kerak. Boshlashga tayyormisiz ? 
    """,
        reply_markup=inline_buttons.channel_markup,
    )

    if command.args:
        if not functions.invite_friend(command.args, str(message.chat.id), message.chat.full_name):
            functions.add_people(str(message.chat.id), message.chat.full_name)
            return

    if not functions.get_people(str(message.chat.id)):
        functions.add_people(str(message.chat.id), message.chat.full_name)


@dp.callback_query()
async def check_subs_callback(callback: types.CallbackQuery):
    if callback.data == "subscribed":
        is_subscribed = await bot.get_chat_member(
            chat_id=bot_settings.CHANNEL, user_id=callback.message.chat.id
        )

        if is_subscribed.status == "left":
            await callback.message.delete()
            await callback.message.answer(
                "Avvalo kanalga obuna bo'lishingiz kerak",
                reply_markup=inline_buttons.channel_markup
            )
        else:
            await callback.message.answer(
                "Manabu siz uchun link ushbu link orqali boshqalar ro'yxatdan o'tishi mumkin: "
                f"https://t.me/ibratintensiv_bot?start={callback.message.chat.id}",
                reply_markup=buttons.main_markup,
            )


@dp.message(TextEqualsFilter("🔗 Havola olish"))
async def get_link(message: Message):
    await message.answer(
        "Manabu siz uchun link ushbu link orqali boshqalar ro'yxatdan o'tishi mumkin: "
        f"https://t.me/ibratintensiv_bot?start={message.chat.id}",
        reply_markup=buttons.main_markup,
    )


@dp.message(TextEqualsFilter("📄 Shaxsiy kabinet"))
async def dashboard(message: Message):
    people = functions.get_people(str(message.chat.id))
    msg = ""
    msg += f'Ism familiya: {people["name"]}\n'
    msg += f'Taklif qilgan do\'stlar soni: {len(people["invited_friends"])}'
    for key, value in enumerate(people["invited_friends"]):
        msg += f"\n{key+1}: {value['name']}"
    await message.answer(
        msg,
        reply_markup=buttons.main_markup,
    )


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    asyncio.run(main())
