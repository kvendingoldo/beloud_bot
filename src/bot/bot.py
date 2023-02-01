# -*- coding: utf-8 -*-

import prettytable as pt
import telebot
import sys
import logging
import time

from utils import config as cfg_utils
from db import utils as db_utils
from models import state
from constants import common

from telebot.types import ReplyKeyboardRemove

sys.path.append('../resources/')
config = cfg_utils.load("../resources/config.yml")

bot = telebot.TeleBot(config["telegram"]["token"])
telebot.logger.setLevel(logging.INFO)

state_repo = db_utils.get_repos(config)

text_messages = {
    'start': u'{name}, привет! 🎉 Выбери необходимое действие в меню ✨',

    'state_1': 'Оцени свое состояние по 10ти балльной шкале',
    'state_2': 'Время высказаться! Ты можешь сделать это голосовым сообщением, текстом или видео-кружочком. Данные я не сохраняю 🙅‍ (у меня на это банально нет ресурсов 🙂)',
    'state_3': 'Очень здорово, что высказался! Полегчало? Пожалуйста, оцени свое состояние еще раз',
    'state_4': 'Круто, спасибо за практику, {name}! Не забывай ее делать регулярно, ведь я для этого и существую',

    'show_history': 'Ваша история: \n',

    'help': 'Я - бот, который дает тебе возможность высказаться. Просто нажми /start и скажи все, что у тебя держалось внутри. 💥 До и после того как ты выскажешься (это может быть текст, голосовое или видео-кружочек) я спрошу тебя про твои ощущения по десятибалльной шкале. Не волнуйся, я не собираю данные 🙅‍, у меня банально нет денег, чтобы их хранить :) \n\nУ меня есть следующие команды: \n/start - начать высказываться \n/help - показать данную подсказку',

    'wrong_msg': 'Похоже что-то пошло не так. Пожалуйста, воспользуйтесь подсказкой через /help или начните заного через /start'
}


@bot.message_handler(commands=['help'])
def handler_help(message):
    try:
        bot.send_message(
            message.from_user.id,
            text_messages['help'],
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception as ex:
        logging.error(ex)


@bot.message_handler(commands=['start'])
def handler_start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('выговориться', 'посмотреть историю', 'помощь')

    try:
        msg = bot.send_message(
            message.from_user.id,
            text_messages['start'].format(name=message.from_user.first_name),
            reply_markup=markup
        )
        bot.register_next_step_handler(msg, handler_l1)
    except Exception as ex:
        logging.error(ex)


@bot.message_handler(content_types=['text'])
def handler_l1(message):
    if message.text == 'выговориться':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣')
        markup.row('6️⃣', '7️⃣️', '8️⃣', '9️⃣', '🔟')

        try:
            msg = bot.send_message(
                message.from_user.id,
                text_messages['state_1'],
                reply_markup=markup
            )
            bot.register_next_step_handler(msg, handler_state_1)
        except Exception as ex:
            logging.error(ex)

    elif message.text == 'посмотреть историю':
        try:
            states = state_repo.list(spec={"uid": message.from_user.id})
            table = pt.PrettyTable(['дата', 'оценка до', 'оценка после', 'результат'])
            for state in states:
                s_bfr = state.r_bfr
                s_afr = state.r_afr

                if state.r_afr > state.r_bfr:
                    result = "🙂"
                    s_afr = f"{s_afr}"
                elif state.r_afr >= state.r_bfr:
                    result = "😐"
                else:
                    result = "😔"
                    s_bfr = f"{s_bfr}"

                table.add_row([
                    state.tmst_created,
                    s_bfr,
                    s_afr,
                    result
                ])
            try:
                bot.send_message(
                    message.from_user.id,
                    text_messages["show_history"] + f'\n\n```{table}```',
                    parse_mode='MarkdownV2',
                    reply_markup=ReplyKeyboardRemove()
                )
            except Exception as ex:
                logging.error(ex)
        except Exception as ex:
            logging.error(ex)
    elif message.text == 'помощь':
        try:
            msg = bot.send_message(
                message.from_user.id,
                text_messages["help"],
                reply_markup=ReplyKeyboardRemove()
            )
            bot.register_next_step_handler(msg, handler_start)
        except Exception as ex:
            logging.error(ex)

    else:
        bot.send_message(
            message.from_user.id,
            text_messages["wrong_msg"],
            reply_markup=ReplyKeyboardRemove()
        )


@bot.message_handler(content_types=['text'])
def handler_state_1(message):
    try:
        state_repo.add(state.State(
            uid=message.from_user.id,
            username=message.from_user.username,
            r_bfr=common.emoji2int[message.text]
        ))
    except Exception as ex:
        logging.error(ex)

    try:
        msg = bot.send_message(
            message.from_user.id,
            text_messages["state_2"],
            reply_markup=ReplyKeyboardRemove()
        )
        bot.register_next_step_handler(msg, handler_state_2)
    except Exception as ex:
        logging.error(ex)


@bot.message_handler(content_types=['text', 'voice', 'video', 'video_note'])
def handler_state_2(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row('1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣')
    markup.row('6️⃣', '7️⃣️', '8️⃣', '9️⃣', '🔟')

    try:
        msg = bot.send_message(
            message.from_user.id,
            text_messages['state_3'].format(name=message.from_user.first_name),
            reply_markup=markup
        )
        bot.register_next_step_handler(msg, handler_state_3)
    except Exception as ex:
        logging.error(ex)


@bot.message_handler(content_types=['text'])
def handler_state_3(message):
    try:
        n_state = state_repo.get_latest_by_uid(message.from_user.id)
        n_state.r_afr = common.emoji2int[message.text]
        state_repo.update(n_state)
    except Exception as ex:
        logging.error(ex)

    try:
        bot.send_message(
            message.from_user.id,
            text_messages['state_4'].format(name=message.from_user.first_name),
            reply_markup=ReplyKeyboardRemove()
        )
    except Exception as ex:
        logging.error(ex)


def run():
    while True:
        try:
            bot.polling(non_stop=True, interval=0, timeout=10)
        except Exception as ex:
            logging.info("[telegram] Failed: %s" % ex)
            time.sleep(3)
