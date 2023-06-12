from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.keyboard import ReplyKeyboardBuilder

choices_button = [
    [InlineKeyboardButton(text='🆔По id', callback_data='id_choices_cal')],
    [InlineKeyboardButton(text='📜По названию', callback_data='name_choices_cal')]
]
choices_kb = InlineKeyboardMarkup(inline_keyboard=choices_button)

main_builder = ReplyKeyboardBuilder().add(KeyboardButton(text='❓Найти фильм'), KeyboardButton(text='❗Узнать про фильм'))

main_kb = main_builder.as_markup(resize_keyboard=True)
