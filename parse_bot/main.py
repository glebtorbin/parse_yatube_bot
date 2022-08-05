import requests, re
import fake_useragent
import logging
import os
import sys
import time
import telegram
from http import HTTPStatus

import requests
from dotenv import load_dotenv

import exceptions

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
AUTH_LINK = os.getenv('AUTH_LINK')
NEW_POST_LINK = os.getenv('NEW_POST_LINK')

USERAGENT = fake_useragent.UserAgent().random
SESSION = requests.Session()

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    level=logging.INFO,
)

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

def text_accepting():
    '''Функция принимает текст для отправки на сайт'''
    pass

def acc_login():
    '''Входит в аккаунт'''
    try:
        csrf_getting = SESSION.get(AUTH_LINK)
    except exceptions.ConnectionError:
        logger.error('Сбой подключения к AUTH_LINK')
    try:
        csrf_token = csrf_getting.cookies['csrftoken']
    except exceptions.CookieError:
        message = 'Не уалось получить cookie'
        logger.error(message)
        raise exceptions.CookieError(message)
    header = {
    'Referer': AUTH_LINK,
    'user-agent': USERAGENT
    }
    data = {
        'username': 'ParseBot',
        'password': 'ZrVjhzZ5Qn6CsjG',
        'csrfmiddlewaretoken': csrf_token
    }
    try:
        response = SESSION.post(AUTH_LINK, data=data, headers=header)
    except ConnectionError:
        logger.error('Сбой подключения к AUTH_LINK')
    return print(response)
    


def new_post():
    '''Создает новый пост'''
    pass

def check_tokens():
    '''Проверяет переменные окружния'''
    pass

def main():
    '''Основная функция описывающия логику и работу бота'''
    pass


if __name__ == '__main__':
    main()

acc_login()