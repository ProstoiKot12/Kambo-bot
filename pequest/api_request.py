import requests

async def api_film_found(message):
    url = 'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword'
    headers = {
        'X-API-KEY': '03867684-72dd-41f1-9301-508b8f8272c3'
    }
    params = {
        'keyword': message.text
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # if response.status_code == 200:
    #     films = data['films']
    #     message_text = ""
    #     for film in films:
    #         message_text += f"<b>{film['nameRu']}</b>, id = {film['filmId']}\n\n"
    #     await message.answer(message_text)
    # else:
    #     await message.answer('Произошла ошибка')

    if response.status_code == 200:
        if 'films' in data:
            films = data['films']
            if films:
                message_text = ""
                for film in films:
                    if 'nameRu' in film and 'filmId' in film:
                        message_text += f"<b>{film['nameRu']}</b>, id = <code>{film['filmId']}</code>\n\n"
                if message_text:
                    await message.answer(message_text)
                else:
                    await message.answer('Нет информации о фильмах')
            else:
                await message.answer('Нет фильмов по данному запросу')
        else:
            await message.answer('Некорректный ответ от API')
    else:
        await message.answer('Произошла ошибка при выполнении запроса')

async def api_film_id(message, title):
    url = 'https://kinopoiskapiunofficial.tech/api/v2.1/films/search-by-keyword'
    headers = {
        'X-API-KEY': '03867684-72dd-41f1-9301-508b8f8272c3'
    }
    params = {
        'keyword': title
    }

    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    if response.status_code == 200:
        films = data['films']
        if films:
            return films[0]['filmId']
    else:
        await message.answer('Произошла ошибка')

async def api_film_about(film_id, message):
    url = f'https://kinopoiskapiunofficial.tech/api/v2.2/films/{film_id}'
    headers = {
        'X-API-KEY': '03867684-72dd-41f1-9301-508b8f8272c3'
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if response.status_code == 200:
        film_info = data
        return film_info
    else:
        return 'Ошибка при выполнении запроса'



