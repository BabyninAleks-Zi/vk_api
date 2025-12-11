import os
from dotenv import load_dotenv
import requests
from urllib.parse import urlparse


def is_shorten_link(link):
    if len(link) < 25:
        return True
    return False


def shorten_link(token, link):
    params = {
        'access_token': token,
        'v': 5.199,
        'url': link,
        'private': 0
    }
    url = 'https://api.vk.ru/method/utils.getShortLink'
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data_link = response.json()
        if 'error' in data_link:
            error_msg = data_link['error']['error_msg']
            if 'url' in error_msg:
                return f'Ошибка: некорректная ссылка {link}.\
                         Введите корректную ссылку'
            else:
                return f'Ошибка VK API {error_msg}'
        short_link = data_link['response']['short_url']
        return short_link
    except requests.exceptions.HTTPError:
        return 'Сетевая ошибка'


def count_clicks(token, *args):
    parsed = urlparse(*args)
    key = parsed.path.lstrip('/')
    params = {
        'access_token': token,
        'v': 5.199,
        'key': key,
        'interval': 'forever',
        'extended': 0
    }
    url = 'https://api.vk.ru/method/utils.getLinkStats'
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data_count = response.json()
        if 'error' in data_count:
            error_msg = data_count['error']['error_msg']
            return f'Ошибка VK API {error_msg}'
        stats_list = data_count['response']['stats']
        stat = stats_list[0]
        return stat['views']
    except requests.exceptions.HTTPError:
        return 'Сетевая ошибка'


def generate_link():
    load_dotenv()
    token = os.getenv('VK_TOKEN')
    if not token:
        print('Ошибка: VK_TOKEN не найден в переменных окружения')
        return
    link = input('Введите ссылку: ')
    if is_shorten_link(link):
        clicks = count_clicks(token, link)
        print('Вы ввели короткую ссылку')
        print('Количество кликов по ссылке: ', clicks)
    else:
        print('Введена длинная ссылка, сокращаю...')
        short_link = shorten_link(token, link)
        print('Сокращенная ссылка: ', short_link)
        clicks = count_clicks(token, short_link)
        print('Количество кликов по ссылке: ', clicks)


if __name__ == '__main__':
    generate_link()
