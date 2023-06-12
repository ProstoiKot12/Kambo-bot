import asyncio
import logging

from aiogram import Bot, Dispatcher, F, Router
from aiogram.filters import Command, Filter, CommandStart
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN, ADMIN_ID
from user.user_handlers import start_handler, film_find, film_found, detected_film, film_about, film_id_about, Form
from user.user_callback import get_name_cal, get_id_cal
from utils.commands import set_commands
from pequest.sql_request import create_table
from admin.admin_handlers import admin_welcome, mes_always_user_end, admin_panel, Admin


router = Router()

async def start_bot(bot: Bot):
    await set_commands(bot)
    await create_table()
    await bot.send_message(ADMIN_ID, text='Бот запущен!')

async def main() -> None:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s - "
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    bot = Bot(TOKEN, parse_mode="HTML")

    dp.startup.register(start_bot)

    dp.message.register(start_handler, Command('start'))
    dp.message.register(admin_welcome, Command('admin'))

    dp.message.register(film_find, F.text == '❓Найти фильм')
    dp.message.register(detected_film, F.text == '❗Узнать про фильм')

    dp.message.register(film_found, Form.find_film)
    dp.message.register(film_about, Form.film_det)
    dp.message.register(film_id_about, Form.film_det_id)
    dp.message.register(admin_panel, Admin.admin_panel)
    dp.message.register(mes_always_user_end, Admin.spam_user_form)

    dp.callback_query.register(get_name_cal, F.data.startswith('name_choices_cal'))
    dp.callback_query.register(get_id_cal, F.data.startswith('id_choices_cal'))

    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())