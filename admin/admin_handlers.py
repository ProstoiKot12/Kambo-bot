from aiogram import types, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import ReplyKeyboardRemove

from config import ADMIN_ID
from admin.admin_keyboards import admin_keyboard
from pequest.sql_request import get_user_id


class Admin(StatesGroup):
    spam_user_form = State()
    admin_panel = State()
    film_det_id = State()

remove_kb = ReplyKeyboardRemove()

async def admin_welcome(message: Message, state: FSMContext):
    if message.from_user.id == ADMIN_ID:
        await state.set_state(Admin.admin_panel)
        await message.answer('Админ панель включена', reply_markup=admin_keyboard)

async def admin_panel(message: Message, state: FSMContext):
    if message.text == '📤Рассылка пользователям':
        await state.set_state(Admin.spam_user_form)
        await message.answer('Введите текст сообщения')
    elif message.text == '🟥Отключить':
        await state.clear()
        await message.answer('Админ панель выключена', reply_markup=remove_kb)
    else:
        await message.answer('Отключите админ панель либо используйте админ панель!')

async def mes_always_user_end(message: Message, state: FSMContext, bot: Bot):
    user_id = await get_user_id()
    for z in range(len(user_id)):
        await bot.send_message(user_id[z][0], message.text)
    await state.set_state(Admin.admin_panel)
    await message.answer('Сообщение было разослано всем пользователям')