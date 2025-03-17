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


def Req(_page: int, _line: int):
    if (_page > 66):
        _page = 66
    elif (_page < 1):
        _page = 1
    try:
        res = requests.get(
            "https://www.marxists.org/russkij/marx/1867/capital_vol1/"
            f"{_page:02d}.htm"
        )
        html = BeautifulSoup(res.content, "lxml")
        lst = []
        i = 2
        for element in html.find_all("p"):
            if (i > 0):
                i -= 1
                continue
            if (element.text == "\xa0"):
                continue
            lst.append(element.text)
        _line -= 1
        if (_line < 0):
            _line = 0
        elif (_line > len(lst)):
            _line = len(lst) - 1
        if (len(lst[_line]) > 4090):
            lst[_line] = lst[_line][0:4090]
        logging.info("request resolved")
        return lst[_line]
    except Exception as ex:
        logging.error(f"request failed: {ex}")
        raise ReqException(ex)


load_dotenv()
bot = telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
log_level = os.getenv("LOG_LEVEL")
logging.basicConfig(
    level=log_level,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


@bot.message_handler(commands=["random"])
def RandomProphetCmd(_message):
    try:
        bot.send_message(
            _message.chat.id, Req(random.randint(1, 66), random.randint(0, 100))
        )
        logging.info("/random executed")
    except Exception as ex:
        bot.send_message(_message.chat.id, "Будущее туманно")
        logging.error(f"/random failed: {ex}")


@bot.message_handler(commands=["prophet"])
def ProphetCmd(_message):
    text = re.findall("[0-9]*", _message.text)
    try:
        line = int(text[11])
        page = int(text[9])
        bot.send_message(_message.chat.id, Req(page, line))
        logging.info("/prophet executed")
    except ReqException as rex:
        bot.send_message(
            _message.chat.id,
            "Боюсь, на эту часть книги пролили кофе"
        )
        logging.error(f"/prophet failed at request: {rex}")
    except Exception as ex:
        bot.send_message(_message.chat.id, "Запрос задан неверно")
        logging.error(f"/prophet failed: {ex}")


@bot.message_handler(commands=["help"])
def HelpCmd(_message, _cascade: bool = False):
    bot.send_message(
        _message.chat.id,
        "/prophet {глава} {строка}\n\n"
        " - введите после названия команды 2 числа через пробел: "
        "номер главы и номер строки\n"
        "Некоторые строки являются таблицами, "
        "поэтому предсказание осуществимо не всегда!\n\n"
        "/random\n\n"
        " - даёт вам случайную строку",
    )
    if not _cascade:
        logging.info("/help executed")


@bot.message_handler(commands=["start"])
def StartCmd(_message):
    bot.send_message(
        _message.chat.id,
        'Этот бот гадает на "Капитале" К. Маркса'
    )
    logging.info("/start executed")
    HelpCmd(_message=_message, _cascade=True)


if __name__ == "__main__":
    logging.info("polling started")
    bot.polling(none_stop=True)
