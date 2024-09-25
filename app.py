import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile
from aiogram import types

from modules.filters import TextEqualsFilter
from modules.settings import get_settings
from modules.keyboards import Buttons, get_channel_markup, get_ready_markup
from modules import functions
from modules import states

bot_settings = get_settings()

buttons = Buttons()

dp = Dispatcher()
bot = Bot(
    token=bot_settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)


@dp.message(CommandStart())
async def command_start_handler(message: Message, command: CommandObject) -> None:
    if message.chat.id in bot_settings.ADMINS:
        await message.answer(
            "Admin panelga xush kelibsiz",
            reply_markup=buttons.main_markup_admin,
        )
        return

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
            reply_markup=get_channel_markup(command.args),
        )


@dp.callback_query()
async def check_subs_callback(callback: types.CallbackQuery):
    if callback.data.startswith("subscribed"):
        is_subscribed = await bot.get_chat_member(
            chat_id=bot_settings.CHANNEL, user_id=callback.message.chat.id
        )

        if is_subscribed.status == "left":
            await callback.message.delete()
            await callback.message.answer(
                "Avvalo kanalga obuna bo'lishingiz kerak",
                reply_markup=get_channel_markup(callback.message.chat.id),
            )
        else:
            if len(callback.data.split(":")) == 2:
                friend_id = callback.data.split(":")[1]
                if not functions.invite_friend(
                    friend_id,
                    str(callback.message.chat.id),
                    callback.message.chat.full_name,
                ):
                    functions.add_people(
                        str(callback.message.chat.id), callback.message.chat.full_name
                    )
                else:
                    people = functions.get_people(friend_id)
                    await bot.send_message(
                        friend_id,
                        f"Sizning <strong>{callback.message.chat.full_name}</strong> do'stingiz botga qo'shildi.",
                    )
                    if (
                        len(people["invited_friends"]) >= 50
                        and people["has_gift_50"] is False
                    ):
                        await bot.send_message(
                            friend_id,
                            f"Tabriklaymiz siz 50 ta taklif qilgansiz va sizga sovg'a bor. ",
                        )
                        functions.add_gift_50(friend_id)
            else:
                functions.add_people(
                    str(callback.message.chat.id), callback.message.chat.full_name
                )

            await callback.message.answer(
                f"""
🇬🇧Yaqinlaringiz til o'rganishiga sababchi bo'ling va sovg'alarni yutib oling🤩

O'yin sharti : Ingliz tiliga qiziqqan do'stlaringizni INTENSIVga taklif qilish.

📌G'oliblarni taklif qilgan do'stlar soniga ko'ra aniqlaymiz.

🔥SOVG'ALAR bilan tanishing 🤩

🔰10 ta taklif : 
- IELTS 7+ uchun STUDY PLAN qo'llanmasi

🔰20 ta taklif : 
- IELTS 7+ uchun STUDY PLAN qo'llanmasi
- Sheriksiz SPEAKING chiqarish usullari darsi

🔰50 ta taklif :
- IELTS 7+ uchun STUDY PLAN qo'llanmasi
- Sheriksiz SPEAKING chiqarish usullari darsi
- Samarali LUG'AT yodlash metodikasi

🔰100 ta taklif :

- IELTS 7+ uchun STUDY PLAN qo'llanmasi
- Sheriksiz SPEAKING chiqarish usullari darsi
- Samarali LUG'AT yodlash metodikasi
- Ibrat Farzandlari loyihasidan maxsus sovg'a 


🔰200 ta taklif :
- IELTS 7+ uchun STUDY PLAN qo'llanmasi
- Sheriksiz SPEAKING chiqarish usullari darsi
- Samarali LUG'AT yodlash metodikasi
- Iskandar Komoldinov bilan JONLI UCHRASHUV va NONUSHTA 

🔰300 ta taklif :

- IELTS 7+ uchun STUDY PLAN qo'llanmasi
- Sheriksiz SPEAKING chiqarish usullari darsi
- Samarali LUG'AT yodlash metodikasi
- English BOOTCAMP kursida qatnashish

🔰500 ta taklif :

 - IELTS 7+ uchun STUDY PLAN qo'llanmasi
- Sheriksiz SPEAKING chiqarish usullari darsi
- Samarali LUG'AT yodlash metodikasi
- Iskandar Komoldinov bilan JONLI UCHRASHUV va NONUSHTA 
- Iskandar Komoldinov tomonidan Londondan sovg'a 


❗️DIQQAT : Sovg'alar INTENSIVdan so'ng egalariga topshiriladi☺️

Sovg'ali o'yinda qatnashish uchun MAXSUS havola olishingiz kerak. Boshlashga tayyormisiz ?
                """,
                reply_markup=get_ready_markup(),
            )

    elif callback.data == "ready":
        with open("assets/iskandar_komoldinov.jpg", "rb") as photo:
            buff_photo = BufferedInputFile(
                file=photo.read(), filename="assets/iskandar_komoldinov.jpg"
            )
            await callback.message.answer_photo(
                buff_photo,
                f"""
Do'stim, sizga sovg'am bor🎁

🇬🇧Bilaman, ingliz tiliga qiziqasiz. O'rganishni boshlab yuborgansiz ham!

• Ingliz tili grammatikani yodlaysizu, ishlatolmaysiz.

• Speaking qilishga qo'rqasiz yoki ko'p xato qilasiz. 

• Talaffuzingiz bo'lsa, inglizlarnikidek chiqmaydi. Bu sizni uyaltiradi.

O'zgarish vaqti keldi❗️

🇺🇿Hoziroq Ibrat Farzandlari loyihasining JONLI INTENSIV DARSLARIGA qo'shiling va ingliz tilingizni yangi darajaga olib chiqing📈

Biz shu yerdamiz: https://t.me/ibratintensiv_bot?start={callback.message.chat.id}
                """,
                reply_markup=buttons.main_markup,
            )
            await callback.message.answer(
                """
⬆️ Yuqorida sizning linkingiz qo'shilgan taklifnoma!

🇬🇧Uni ingliz tiliga qiziqqan do'stlaringizga, yaqinlaringizga va barcha guruhlarga jo'nating❗️

O'z sovg'angizni qo'lga kiritishingizga omad tilaymiz🔥
            """
            )


@dp.message(TextEqualsFilter("🔗 Havola olish"))
async def get_link(message: Message):
    with open("assets/iskandar_komoldinov.jpg", "rb") as photo:
        buff_photo = BufferedInputFile(
            file=photo.read(), filename="assets/iskandar_komoldinov.jpg"
        )
        await message.answer_photo(
            buff_photo,
            f"""
Do'stim, sizga sovg'am bor🎁

🇬🇧Bilaman, ingliz tiliga qiziqasiz. O'rganishni boshlab yuborgansiz ham!

• Ingliz tili grammatikani yodlaysizu, ishlatolmaysiz.

• Speaking qilishga qo'rqasiz yoki ko'p xato qilasiz. 

• Talaffuzingiz bo'lsa, inglizlarnikidek chiqmaydi. Bu sizni uyaltiradi.

O'zgarish vaqti keldi❗️

🇺🇿Hoziroq Ibrat Farzandlari loyihasining JONLI INTENSIV DARSLARIGA qo'shiling va ingliz tilingizni yangi darajaga olib chiqing📈

Biz shu yerdamiz: https://t.me/ibratintensiv_bot?start={message.chat.id}
        """,
            reply_markup=buttons.main_markup,
        )


@dp.message(TextEqualsFilter("📄 Shaxsiy kabinet"))
async def dashboard(message: Message):
    people = functions.get_people(str(message.chat.id))
    msg = ""
    msg += f'Ism familiya: {people["name"]}\n'
    msg += f'Taklif qilgan do\'stlar soni: {len(people["invited_friends"])}'
    for key, value in enumerate(people["invited_friends"]):
        msg += f"\n{key + 1}: {value['name']}"
    await message.answer(
        msg,
        reply_markup=buttons.main_markup,
    )


@dp.message(TextEqualsFilter("📊 Statistika"))
async def statistics(message: Message):
    if message.chat.id not in bot_settings.ADMINS:
        return

    people = functions.get_stats()["people"]
    msg = ""
    for key, value in enumerate(people):
        msg = f"{key + 1}: {value['name']} - {len(value['invited_friends'])} ta taklif qilgan"

    await message.answer(
        msg,
        reply_markup=buttons.main_markup_admin,
    )


@dp.message(TextEqualsFilter("### Post yuborish"))
async def send_post(message: Message, state: FSMContext):
    if message.chat.id not in bot_settings.ADMINS:
        return

    await message.answer("Post matnini kiriting")
    await state.set_state(states.PostSendState.post_text)


@dp.message(states.PostSendState.post_text)
async def send_post(message: Message, state: FSMContext):
    if message.chat.id not in bot_settings.ADMINS:
        return

    people_ids = functions.get_people_ids()
    await message.answer("Post yuborilmoqda...")
    try:
        for people_id in people_ids.values():
            await message.send_copy(people_id)

    except Exception as e:
        await message.answer(f"Post yuborishda xatolik: {e}")

    await state.clear()


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        stream=sys.stdout,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    asyncio.run(main())
