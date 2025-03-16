import logging
import os
import random
import re

import requests
import telebot
from bs4 import BeautifulSoup
from dotenv import load_dotenv


class ReqException(Exception):
    pass


def req(page: int, line: int):
    if page > 66:
        page = 66
    elif page < 1:
        page = 1
    res = requests.get(
        "https://www.marxists.org/russkij/marx/1867/capital_vol1/"
        f"{page:02d}.htm"
    )
    html = BeautifulSoup(res.content, "lxml")
    lst = []
    i = 2
    for element in html.find_all("p"):
        if i > 0:
            i -= 1
            continue
        if element.text == "\xa0":
            continue
        lst.append(element.text)
    line -= 1
    if line < 0:
        line = 0
    elif line > len(lst):
        line = len(lst) - 1
    if len(lst[line]) > 4090:
        lst[line] = lst[line][0:4090]
    return lst[line]


load_dotenv()
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))


@bot.message_handler(commands=["random"])
def random_prophet_cmd(message):
    try:
        bot.send_message(
            message.chat.id, req(random.randint(1, 66), random.randint(0, 100))
        )
    except Exception as ex:
        logging.error(f"exception at req: {ex}")
        bot.send_message(message.chat.id, "Будущее туманно")


@bot.message_handler(commands=["prophet"])
def prophet_cmd(message):
    text = re.findall("[0-9]*", message.text)
    try:
        line = int(text[11])
        page = int(text[9])
        bot.send_message(message.chat.id, req(page, line))
    except ReqException:
        bot.send_message(
            message.chat.id,
            "Боюсь, на эту часть книги пролили кофе"
        )
    except Exception as ex:
        logging.error(f"exception at prophet: {ex}")
        bot.send_message(message.chat.id, "Запрос задан неверно")


@bot.message_handler(commands=["help"])
def help_cmd(message):
    bot.send_message(
        message.chat.id,
        "/prophet {глава} {строка}\n\n"
        " - введите после названия команды 2 числа через пробел: "
        "номер главы и номер строки\n"
        "Некоторые строки являются таблицами, "
        "поэтому предсказание осуществимо не всегда!\n\n"
        "/random\n"
        " - даёт вам случайную строку",
    )


@bot.message_handler(commands=["start"])
def start_cmd(message):
    bot.send_message(
        message.chat.id,
        'Этот бот гадает на "Капитале" К. Маркса'
    )
    help_cmd(message=message)


if __name__ == "__main__":
    bot.polling(none_stop=True)
