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

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
AUTH_LINK = os.getenv('AUTH_LINK')
NEW_POST_LINK = os.getenv('NEW_POST_LINK')

def text_accepting():
    '''Функция принимает текст для отправки на сайт'''
    pass

def login():
    '''Входит в аккаунт'''
    pass

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

