from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import ReplyKeyboardBuilder

admin_builder = ReplyKeyboardBuilder().add(KeyboardButton(text='📤Рассылка пользователям'),
                                           KeyboardButton(text='🟥Отключить'))

admin_keyboard = admin_builder.as_markup(resize_keyboard=True)