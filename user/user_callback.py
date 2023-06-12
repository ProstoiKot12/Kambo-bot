from aiogram import Bot
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from user.user_handlers import Form

async def get_name_cal(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Введите название фильма')
    await state.set_state(Form.film_det)

async def get_id_cal(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.answer()
    await callback.message.answer('Введите id фильма')
    await state.set_state(Form.film_det_id)