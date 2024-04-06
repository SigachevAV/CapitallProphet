import requests
import telebot
from bs4 import BeautifulSoup
import random
import re
import os
def Req(_page : int, _st : int):
    if(_page>66):
        _page=66
    elif(_page<1):
        _page=1
    if(_page<10):
        _page="0"+str(_page)
    res = requests.get("https://www.marxists.org/russkij/marx/1867/capital_vol1/"+ str(_page) + ".htm")
    html = BeautifulSoup(res.content, "lxml")
    list = []
    i = 2
    for element in html.findAll("p"):
        if(i>0):
            i-=1
            continue
        if(element.text == '\xa0'):
            continue
        list.append(element.text)
    _st-=1
    if(_st < 0):
        _st = 0
    elif(_st>len(list)):
        _st=len(list)-1
    if(len(list[_st])>4090):
        list[_st]=len[_st][0:4090]
    return list[_st]

bot = telebot.TeleBot(os.environ["TELEGRAM_TOKEN"])

@bot.message_handler(commands=['random'])
def randomProphet(message):
    try:
        bot.send_message(message.chat.id, Req(random.randint(1, 66), random.randint(0, 100)))
    except:
        bot.send_message(message.chat.id, "Будущеее туманно")

@bot.message_handler(commands=['prophet'])
def prophet(message):
    text =re.findall('[0-9]*', message.text)
    page = 0
    stringg = 0
    try:
        stringg=int(text[11])
        page=int(text[9])
    except:
        bot.send_message(message.chat.id, "Запрос задан неверно")
        return
    try:
        bot.send_message(message.chat.id, Req(page, stringg))
    except:
         bot.send_message(message.chat.id, "Боюсь на эту часть книги пролили кофе")   
            
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, "/prophet {глава} {строка}\nвведите после команды 2 числа через пробел которые будут означать главу капиталла (от 1 до 66) и строку в ней\nНекоторые строки являються таблицами и по этому предсказания по ним не будет.\n/random\nдаёт вам случайную строку")
         
@bot.message_handler(command=['start'])
def start(message):
    bot.send_message(message.chat.id, "Этот бот будет гадать на капиталле")
    help(message=message)

bot.polling(none_stop=True)
