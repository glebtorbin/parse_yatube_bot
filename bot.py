import logging
import os
import sys
import time
import telegram

import fake_useragent
from bs4 import BeautifulSoup
from telegram.ext import CommandHandler, Updater, MessageHandler, Filters
import requests
from dotenv import load_dotenv

import exceptions

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
AUTH_LINK = os.getenv('AUTH_LINK')
NEW_POST_LINK = os.getenv('NEW_POST_LINK')
PROFILE_LINK = os.getenv('PROFILE_LINK')

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
    context.bot.send_message(
        chat_id=chat.id,
        text=(f'Привет, {name}. Если хочешь сделать пост '
              'на моем сайте http://glebtorbin.pythonanywhere.com'
              ' напиши его ниже'),
    )
    context.bot.send_message(
        chat_id=chat.id,
        text=('Введите текст:'))


def post_count(update, context):
    '''подсчитывет количество постов'''
    chat = update.effective_chat
    try:
        logger.info('Собираем актуальную информацию...')
        context.bot.send_message(chat_id=chat.id,
                                 text='Собираем актуальную информацию...')
        responce = SESSION.get(PROFILE_LINK).text
        soup = BeautifulSoup(responce, 'lxml')
        block = soup.find('main')
        text = block.find('h3').text
    except exceptions.ConnectionError:
        logger.error('Сбой подключения')
    button = telegram.ReplyKeyboardMarkup([['/sendmessage'], ['/postcount']],
                                          resize_keyboard=True)
    context.bot.send_message(chat_id=chat.id, text=text,
                             reply_markup=button)


def send_message(update, context):
    '''Функция принимает текст для отправки на сайт'''
    chat = update.effective_chat
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
        SESSION.post(NEW_POST_LINK, data=data, headers=HEADER)
        update.message.reply_text('Сообщение успешно отправлено!')
        update.message.reply_text('Проверяй сайт')
        logger.info('Сообщение успешно отправлено!')
    except exceptions.ConnectionError:
        update.message.reply_text('Сбой подключения, попробуйте позже')
        logger.error('Сбой подключения к AUTH_LINK')
    button = telegram.ReplyKeyboardMarkup([['/sendmessage'], ['/postcount']],
                                          resize_keyboard=True)
    context.bot.send_message(
        chat_id=chat.id,
        text=('Отправить еще сообщение -  /sendmessage, '
              'Узнать, сколько постов сделал Bot Parser - /postcount'),
        reply_markup=button)


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
        updater.dispatcher.add_handler(CommandHandler('sendmessage', wake_up))
        updater.dispatcher.add_handler(CommandHandler('postcount', post_count))
        updater.dispatcher.add_handler(MessageHandler(Filters.text,
                                                      send_message))
        acc_login()
        updater.start_polling()
        updater.idle()
SESSION.get(PROFILE_LINK)
time.sleep(600)


if __name__ == '__main__':
    main()
