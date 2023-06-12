from aiogram import types, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from pequest.api_request import api_film_found, api_film_id, api_film_about
from user.user_keyboards import choices_kb, main_kb
from pequest.sql_request import insert_into_id
from pequest.excel_request import id_in_excel
from config import ADMIN_ID


class Form(StatesGroup):
    find_film = State()
    film_det = State()
    film_det_id = State()

async def start_handler(message: Message, bot: Bot):
    await insert_into_id(message.from_user.id, message.from_user.username)
    try:
        await id_in_excel(message.from_user.id, message.from_user.username)
    except:
        print('Закройте таблицу')
    if message.from_user.id == ADMIN_ID:
        await message.answer('Привет админ, чтобы включить админ панель введи /admin', reply_markup=main_kb)
    else:
        await message.answer('Привет, тут ты можешь узнать про фильмы и сериалы.\n', reply_markup=main_kb)

async def film_find(message: Message, state: FSMContext):
    await state.set_state(Form.find_film)
    await message.answer('Введи <b>название</b> и тебе покажеться все фильмы и сериалы с <strong>похожим названием</strong> и их id')

async def film_found(message: Message, state: FSMContext):
    await state.clear()
    await message.answer('Вот все фильмы и сериалы с похожим названием и их id')
    await api_film_found(message)

async def detected_film(message: Message, state: FSMContext):
    await message.answer('Выбери как узнать про фильм\n', reply_markup=choices_kb)

async def film_id_about(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Вот вся информация про фильм или сериал c id <b>{message.text.strip()}</b>")
    film_info = await api_film_about(message.text.strip(), message)

    if isinstance(film_info, dict):
        Age_limit = f"<b>{film_info.get('ratingAgeLimits', '')}+</b>"
        Age_limit = Age_limit.replace("age", "")
        Kinopoisk_rate = f"<b>{film_info.get('ratingKinopoisk', 'Не оценен')}</b>"
        Imdb_rate = f"<b>{film_info.get('ratingImdb', 'Не оценен')}</b>"
        Cratko = f"{film_info.get('shortDescription', 'Не найдено')}"
        Description = f"{film_info.get('description', '')}"

        if film_info['ratingAgeLimits'] is None:
            Age_limit = '<b>Нету</b>'

        if film_info['ratingKinopoisk'] is None:
            Kinopoisk_rate = '<b>Не оценен</b>'

        if film_info['ratingImdb'] is None:
            Imdb_rate = '<b>Не оценен</b>'

        if film_info['shortDescription'] is None:
            Cratko = "Не найдено"

        if film_info['description'] is None:
            Description = "Нету"

        if len(Description +
                str(Age_limit) +
                Kinopoisk_rate +
                Imdb_rate +
                Cratko +
                film_info['nameRu'] +
                film_info['webUrl'] +
                str(film_info['year'])) > 1024:
            await message.answer_photo(photo=film_info['posterUrl'], caption='')
            await message.answer(f"Название: <a href='{film_info['webUrl']}'>{film_info['nameRu']}</a> ({film_info['year']})\n\n"
                                 f"Кратко: {Cratko}\n\n"
                                 f"Описание: {Description}\n\n"
                                 f"Рейтинг Кинопоиска: {Kinopoisk_rate}\n"
                                 f"Рейтинг Imdb: {Imdb_rate}\n\n"
                                 f"Возрастное ограничение: {Age_limit}+\n\n",
                                 disable_web_page_preview=True)
        else:
            await message.answer_photo(photo=film_info['posterUrl'], caption=
                                    f"Название: <a href='{film_info['webUrl']}'>{film_info['nameRu']}</a> ({film_info['year']})\n\n"
                                    f"Кратко: {Cratko}\n\n"
                                    f"Описание: {Description}\n\n"
                                    f"Рейтинг Кинопоиска: {Kinopoisk_rate}\n"
                                    f"Рейтинг Imdb: {Imdb_rate}\n\n"
                                    f"Возрастное ограничение: {Age_limit}\n\n", disable_web_page_preview=True)
    else:
        await message.answer('Фильма или сериала с таким id не было найдено')

async def film_about(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(f"Вот вся информация про фильм или сериал <b>{message.text}</b>")
    film_id = await api_film_id(message, message.text)
    film_info = await api_film_about(film_id, message)

    if isinstance(film_info, dict):
        Age_limit = f"<b>{film_info.get('ratingAgeLimits', '')}+</b>"
        Age_limit = Age_limit.replace("age", "")
        Kinopoisk_rate = f"<b>{film_info.get('ratingKinopoisk', 'Не оценен')}</b>"
        Imdb_rate = f"<b>{film_info.get('ratingImdb', 'Не оценен')}</b>"
        Cratko = f"{film_info.get('shortDescription', 'Не найдено')}"
        Description = f"{film_info.get('description', '')}"

        if film_info['ratingAgeLimits'] is None:
            Age_limit = '<b>Нету</b>'

        if film_info['ratingKinopoisk'] is None:
            Kinopoisk_rate = '<b>Не оценен</b>'

        if film_info['ratingImdb'] is None:
            Imdb_rate = '<b>Не оценен</b>'

        if film_info['shortDescription'] is None:
            Cratko = "Не найдено"

        if film_info['description'] is None:
            Description = "Нету"

        if len(Description +
               str(Age_limit) +
               Kinopoisk_rate +
               Imdb_rate +
               Cratko +
               film_info['nameRu'] +
               film_info['webUrl'] +
               str(film_info['year'])) > 1024:
            await message.answer_photo(photo=film_info['posterUrl'], caption='')
            await message.answer(f"Название: <a href='{film_info['webUrl']}'>{film_info['nameRu']}</a> ({film_info['year']})\n\n"
                                 f"Кратко: {Cratko}\n\n"
                                 f"Описание: {Description}\n\n"
                                 f"Рейтинг Кинопоиска: {Kinopoisk_rate}\n"
                                 f"Рейтинг Imdb: {Imdb_rate}\n\n"
                                 f"Возрастное ограничение: {Age_limit}+\n\n",
                                 disable_web_page_preview=True)

        else:
            await message.answer_photo(photo=film_info['posterUrl'], caption=
            f"Название: <a href='{film_info['webUrl']}'>{film_info['nameRu']}</a> ({film_info['year']})\n\n"
            f"Кратко: {Cratko}\n\n"
            f"Описание: {Description}\n\n"
            f"Рейтинг Кинопоиска: {Kinopoisk_rate}\n"
            f"Рейтинг Imdb: {Imdb_rate}\n\n"
            f"Возрастное ограничение: {Age_limit}\n\n", disable_web_page_preview=True)

    else:
        await message.answer('Фильма или сериала с таким названием не было найдено')
