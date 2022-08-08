import requests, re
import fake_useragent
import logging
import os
import sys
import time
import telegram
from http import HTTPStatus
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters

import requests
from dotenv import load_dotenv

import exceptions

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
AUTH_LINK = os.getenv('AUTH_LINK')
NEW_POST_LINK = os.getenv('NEW_POST_LINK')

USERAGENT = fake_useragent.UserAgent().random
SESSION = requests.Session()

HEADER: dict = {
    'Referer': AUTH_LINK,
    'user-agent': USERAGENT
    }

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
    level=logging.INFO,
)

logger = logging.getLogger(__name__)
handler = logging.StreamHandler(sys.stdout)
logger.addHandler(handler)

def wake_up(update, context):
    '''Будим бота'''
    chat = update.effective_chat
    name = update.message.chat.first_name
    #button = telegram.ReplyKeyboardMarkup([['/sendmessage']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text=(f'Привет, {name}. Если хочешь сделать пост '
               'на моем сайте http://glebtorbin.pythonanywhere.com'
               ' напиши его ниже'),
        #reply_markup=button
    )

def send_message(update, context):
    '''Функция принимает текст для отправки на сайт'''
    message = update.message.text
    try:
        csrf_getting = SESSION.get(NEW_POST_LINK)
    except exceptions.ConnectionError:
        logger.error('Сбой подключения к NEW_POST_LINK')
    try:
        csrf_token = csrf_getting.cookies['csrftoken']
    except exceptions.CookieError:
        message = 'Не уалось получить cookie'
        logger.error(message)
        raise exceptions.CookieError(message)
    data = {
        'csrfmiddlewaretoken': csrf_token,
        'text': message
    }
    logger.info('Отправляем сообщение...')
    update.message.reply_text('Отправляем сообщение...')
    try:
        creating_post = SESSION.post(NEW_POST_LINK, data=data, headers=HEADER)
        update.message.reply_text('Сообщение успешно отправлено!')
        logger.info('Сообщение успешно отправлено!')
    except exceptions.ConnectionError:
        update.message.reply_text('Сбой подключения, попробуйте позже')
        logger.error('Сбой подключения к AUTH_LINK')
    return creating_post

def acc_login():
    '''Входит в аккаунт'''
    try:
        csrf_getting = SESSION.get(AUTH_LINK)
    except exceptions.ConnectionError:
        logger.error('Сбой подключения к AUTH_LINK')
    logger.info('Входим в аккаунт...')
    try:
        csrf_token = csrf_getting.cookies['csrftoken']
    except exceptions.CookieError:
        message = 'Не уалось получить cookie'
        logger.error(message)
        raise exceptions.CookieError(message)
    data = {
        'username': 'ParseBot',
        'password': 'ZrVjhzZ5Qn6CsjG',
        'csrfmiddlewaretoken': csrf_token
    }
    try:
        response = SESSION.post(AUTH_LINK, data=data, headers=HEADER)
    except exceptions.ConnectionError:
        logger.error('Сбой подключения к AUTH_LINK')
    return print(response)
    
def check_tokens():
    '''Проверяет переменные окружния'''
    return all([TELEGRAM_TOKEN, AUTH_LINK, NEW_POST_LINK, USERAGENT])

def main():
    '''Основная функция описывающия логику и работу бота'''
    if not check_tokens():
        msg = 'Проверьте все переменные окружения'
        logger.critical(msg)
        raise exceptions.ConstantError(msg)
    
    while True:
        updater = Updater(token=TELEGRAM_TOKEN)

        updater.dispatcher.add_handler(CommandHandler('start', wake_up))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, send_message))
        acc_login()
        updater.start_polling()
        updater.idle()
    
    
if __name__ == '__main__':
    main()
