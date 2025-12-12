import os
from dotenv import load_dotenv
import requests
from urllib.parse import urlparse


def is_shorten_link(link):
    if 'vk.cc/' in link:
        return True


def shorten_link(token, link):
    params = {
        'access_token': token,
        'v': 5.199,
        'url': link,
        'private': 0
    }
    url = 'https://api.vk.ru/method/utils.getShortLink'
    response = requests.get(url, params=params)
    response.raise_for_status()
    api_response = response.json()
    if 'error' in api_response:
        error_msg = api_response['error']['error_msg']
        if 'url' in error_msg:
            raise Exception(f'Некорректная ссылка {link}.')
        else:
            raise Exception(f'VK API {error_msg}')
    short_link = api_response['response']['short_url']
    return short_link


def count_clicks(token, link):
    parsed_link = urlparse(link)
    key = parsed_link.path.lstrip('/')
    params = {
        'access_token': token,
        'v': 5.199,
        'key': key,
        'interval': 'forever',
        'extended': 0
    }
    url = 'https://api.vk.ru/method/utils.getLinkStats'
    response = requests.get(url, params=params)
    response.raise_for_status()
    stat_response = response.json()
    if 'error' in stat_response:
        error_msg = stat_response['error']['error_msg']
        raise Exception(f'VK API {error_msg}')
    views_response = stat_response['response']['stats']
    stat = views_response[0]
    return stat['views']


def main():
    load_dotenv()
    token = os.getenv('VK_TOKEN')
    if not token:
        print('VK_TOKEN не найден в переменных окружения')
        return
    link = input('Введите ссылку: ')
    try:
        if is_shorten_link(link):
            clicks = count_clicks(token, link)
            print('Вы ввели короткую ссылку')
            print('Количество кликов по ссылке: ', clicks)
        else:
            print('Введена длинная ссылка, сокращаю...')
            short_link = shorten_link(token, link)
            print('Сокращенная ссылка: ', short_link)
    except requests.exceptions.HTTPError as err:
        print(f'Сетевая ошибка: {err}')
    except Exception as err:
        print(f'Ошибка: {err}')


if __name__ == '__main__':
    main()
